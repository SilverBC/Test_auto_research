import psutil
import time
import subprocess
import json
import threading
import os
import shlex

# This is how often the CPU/memory measurements are made in
# seconds. It's recommended as per psutil's documentation that this
# value should not be below 0.1
INTERVAL=1.0

# This dictionary is used to look up which script to run for which language
launch_scripts = {
    "java": shlex.split("mvn -B test"),
    "java_comp": shlex.split("mvn -B clean test"),
    "c_sharp": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "c_sharp_comp": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "js": shlex.split("npm --prefix src/test/JavaScript test"),
    "python": shlex.split("pytest src/test/python/CommerceTest.py"),
    "ruby": shlex.split("ruby src/test/Ruby/CommerceTest.rb")
}

# This function runs in a separate thread in order to monitor the
# overall CPU and memory usage.
def monitor(pid):
    perf_data = []

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

    print(json.dumps(perf_data))

def run():
    # We get the language to run from the environment varables. This
    # makes configuration from the pipeline side trivially easy.
    target_language = os.environ["TARGET_LANGUAGE"]
    launch_script = launch_scripts[target_language]

    # This is necessary, because dotnet CLI does not seem to have an
    # option to forcefully recompile the code, so I am deleting the
    # bin and obj folders by hand.
    if target_language == "c_sharp_comp":
       subprocess.run("rm -r src/test/C\\#/bin && rm -r src/test/C\\#/obj", shell=True)

    # Start the process of the test and store its PID. We will then
    # pass this PID to the monitor function defined above so that we
    # only run the monitoring while the process is active.
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

    # Print out the process's stdout so we can see how the test run
    # went.
    print(stdout)

    # Print out the process's stderr if there is anything in there.
    if stderr:
        print(stderr)

if __name__ == "__main__":
    run()
