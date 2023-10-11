import csv
import decimal
import psutil
import time
import subprocess
import threading
import os
import re
import shlex

# This is how often the CPU/memory measurements are made in
# seconds. It's recommended as per psutil's documentation that this
# value should not be below 0.1
INTERVAL=1.0

# This dictionary is used to look up which script to run for which
# language.  shlex is used as a convenicence to split up the commands
# the way subprocess.Popen expects them.
launch_scripts = {
    "java": shlex.split("mvn -B test"),
    "java_comp": shlex.split("mvn -B clean test"),
    "c_sharp": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "c_sharp_comp": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "js": shlex.split("npm --prefix src/test/JavaScript test"),
    "python": shlex.split("pipenv run pytest src/test/python/CommerceTest.py"),
    "ruby": shlex.split("ruby src/test/Ruby/CommerceTest.rb")
}

perf_data = []

# This function runs in a separate thread in order to monitor the
# overall CPU and memory usage.
def monitor(pid):
    while psutil.pid_exists(pid):
        cpu_percent = psutil.cpu_percent(interval=INTERVAL)
        sw_mem_info = psutil.swap_memory()
        virt_mem_info = psutil.virtual_memory()

        perf_data.append({
            'cpu': cpu_percent,
            'memory_swap': sw_mem_info.percent,
            'memory_virtual': virt_mem_info.percent,
            'timestamp': int(time.time())
        })

def parse_test_execution_time(language, stdout_text):
    result = 0

    # TODO: extract java, python and ruby logic into a separate function

    if language == "java" or language == "java_comp":
        # Need to match `[INFO] Total time:  37.212 s`
        pattern = re.compile(r"Total time:\s+(\d+\.\d+) s")
        matches = re.search(pattern, stdout_text)
        if matches:
            extracted_text = matches.group(1)
            ex_ms = decimal.Decimal(extracted_text) * 1000
            result = int(ex_ms)
        else:
            print(f"WARNING: There was an issue with parsing the output of {language} test")
    elif language == "c_sharp" or language == "c_sharp_comp":
        # TODO: implement this
        result = 0
    elif language == "js":
        # Not using decimal because the results are given in ms anyway
        pattern = re.compile(r"\((\d+)ms\)")
        matches = re.findall(pattern, stdout_text)
        if matches:
            ms_list = [int(item) for item in matches]
            result = sum(ms_list)
        else:
            print(f"WARNING: There was an issue with parsing the output of {language} test")
    elif language == "python":
        pattern = re.compile(r"\d+ passed in (\d+\.\d+)s")
        matches = re.search(pattern, stdout_text)
        if matches:
            extracted_text = matches.group(1)
            ex_ms = decimal.Decimal(extracted_text) * 1000
            result = int(ex_ms)
        else:
            print(f"WARNING: There was an issue with parsing the output of {language} test")
    elif language == "ruby":
        pattern = re.compile(r"Finished in (\d+\.\d+) seconds\.")
        matches = re.search(pattern, stdout_text)
        if matches:
            extracted_text = matches.group(1)
            ex_ms = decimal.Decimal(extracted_text) * 1000
            result = int(ex_ms)
        else:
            print(f"WARNING: There was an issue with parsing the output of {language} test")
    else:
        raise ValueError("Incorrect language specified!")

    return result

# We get the language to run from the environment varables. This
# makes configuration from the pipeline side trivially easy.
target_language = os.environ["TARGET_LANGUAGE"]
launch_script = launch_scripts[target_language]

# This is necessary, because dotnet CLI does not seem to have an
# option to forcefully recompile the code, so I am deleting the
# bin and obj folders by hand.
if target_language == "c_sharp_comp":
    subprocess.run("rm -r src/test/C\\#/bin && rm -r src/test/C\\#/obj", shell=True)

start_time = time.time()

# Start the process of the test and store its PID. We will then pass
# this PID to the monitor function defined above so that we only run
# the monitoring while the process is active. subprocess.Popen is used
# because we don't want to wait for the process to finish, like it is
# with run().
external_process = subprocess.Popen(launch_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
pid = external_process.pid
print(pid)

# Start the monitoring function in another thread
monitor_thread = threading.Thread(target=monitor, args=[pid])
monitor_thread.start()
stdout, stderr = external_process.communicate()

# Order the main thread to wait for the test launch process to
# finish.
external_process.wait()
external_process.terminate()

# Join the forked thread.
monitor_thread.join()

end_time = time.time()

script_elapsed_time = end_time - start_time
script_elapsed_time_ms = int(script_elapsed_time * 1000)

end_timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime(end_time))

print(f"LAUNCH SCRIPT MEASURED TIME: {script_elapsed_time:.2f} seconds")

with open(f"{target_language}-tr-{end_timestamp}.csv", "w", newline = "") as csv_file:
    fieldnames = perf_data[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in perf_data:
        writer.writerow(row)

parsed_exec_time = parse_test_execution_time(target_language, stdout)

print(f"PARSED TIME: {parsed_exec_time} ms")

# with open(f"{target_language}-et-{end_timestamp}.csv", "w", newline = "") as csv_file:
#     fieldnames = ["script_measured_time", "launcher_parsed_time"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow({"script_measured_time": round(script_elapsed_time * 1000),
#                      "launcher_parsed_time": parsed_exec_time})

# Print out the process's stdout so we can see how the test run
# went.
print(stdout)

# Print out the process's stderr if there is anything in there.
if stderr:
    print(stderr)
