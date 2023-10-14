from datetime import datetime
from dateutil.parser import isoparse
import csv
import decimal
import os
import psutil
import re
import shlex
import subprocess
import threading
import time
import xml.etree.ElementTree as ET

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
    "c_sharp": shlex.split("dotnet test --logger \"trx;LogFileName=testResults.trx\" src/test/C\\#/packages.csproj"),
    "c_sharp_comp": shlex.split("dotnet test --logger \"trx;LogFileName=testResults.trx\" src/test/C\\#/packages.csproj"),
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

def parse_seconds_via_regexp(regexp, input_str):
    pattern = re.compile(regexp)
    matches = re.search(pattern, input_str)
    if matches:
        extracted_text = matches.group(1)
        ex_ms = decimal.Decimal(extracted_text) * 1000
        return int(ex_ms)
    else:
        return -1

def parse_ms_via_regexp(regexp, input_str):
    pattern = re.compile(regexp)
    matches = re.findall(pattern, input_str)
    if matches:
        ms_list = [int(item) for item in matches]
        return sum(ms_list)
    else:
        return -1

def parse_test_run_xml():
    xml_tree = ET.parse("src/test/C#/TestResults/testResults.trx")
    # For some bizarre reason, this expression works instead of
    # "./TestRun/Times".
    times_node = xml_tree.find("./")
    if times_node is not None:
        start_time_str = times_node.get("start")
        end_time_str = times_node.get("finish")
        if start_time_str and end_time_str:
            start_time = isoparse(start_time_str)
            end_time = isoparse(end_time_str)
            duration_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )
            return duration_ms
    else:
        print(f"WARNING: could not parse testResults.trx file!")
        return -1

def parse_test_execution_time(language, stdout_text):
    result = -1

    if language == "java" or language == "java_comp":
        parse_result = parse_seconds_via_regexp(r"Total time:\s+(\d+\.\d+) s", stdout_text)
        result = parse_result
    elif language == "c_sharp" or language == "c_sharp_comp":
        parse_result = parse_test_run_xml()
        result = parse_result
    elif language == "js":
        parse_result = parse_ms_via_regexp(r"\((\d+)ms\)", stdout_text)
        result = parse_result
    elif language == "python":
        parse_result = parse_seconds_via_regexp(r"\d+ passed in (\d+\.\d+)s", stdout_text)
        result = parse_result
    elif language == "ruby":
        parse_result = parse_seconds_via_regexp(r"Finished in (\d+\.\d+) seconds\.", stdout_text)
        result = parse_result
    else:
        raise ValueError("Incorrect language specified!")

    if result == -1:
        print(f"WARNING: There was an issue with parsing the output of {language} test")

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

# Start measuring the start time just before the subprocess is
# launched
start_time = time.time()

# Start the process of the test and store its PID. We will then pass
# this PID to the monitor function defined above so that we only run
# the monitoring while the process is active. subprocess.Popen is used
# because we don't want to wait for the process to finish, like it is
# with run().
external_process = subprocess.Popen(launch_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
pid = external_process.pid

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

# Stop measuring the time just after the subprocess is over.
end_time = time.time()

# If the process exited with an error code, warn the user about it.
if external_process.returncode != 0:
    print("WARNING: there was an error in the test launch!")

script_elapsed_time = end_time - start_time
script_elapsed_time_ms = int(script_elapsed_time * 1000)

# Format the end timestamp.
end_timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime(end_time))

# Print out the process's stdout so we can see how the test run
# went.
print(stdout)

# Print out the process's stderr if there is anything in there.
if stderr:
    print(stderr)

# Write the performance measurements in a CSV file. 
with open(f"{target_language}-tr-{end_timestamp}.csv", "w", newline = "") as csv_file:
    fieldnames = perf_data[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in perf_data:
        writer.writerow(row)

parsed_exec_time = parse_test_execution_time(target_language, stdout)

print(f"LAUNCH SCRIPT MEASURED TIME: {script_elapsed_time:.2f} seconds")
print(f"PARSED TIME: {parsed_exec_time} ms")

# Write the execution times in a a CSV file.
with open(f"{target_language}-et-{end_timestamp}.csv", "w", newline = "") as csv_file:
    fieldnames = ["script_measured_time", "launcher_parsed_time"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"script_measured_time": script_elapsed_time_ms,
                     "launcher_parsed_time": parsed_exec_time})

exit(0)
