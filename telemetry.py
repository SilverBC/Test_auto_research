import psutil
import time
import subprocess
import json
import threading
import os
import shlex

launch_scripts = {
    "java": shlex.split("mvn -B test"),
    "java_comp": shlex.split("mvn -B clean test"),
    "c#": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "c#_comp": shlex.split("dotnet test src/test/C\\#/packages.csproj"),
    "js": shlex.split("npm --prefix src/test/JavaScript test"),
    "python": shlex.split("pytest src/test/python/CommerceTest.py"),
    "ruby": shlex.split("ruby src/test/Ruby/CommerceTest.rb")
}

def monitor(pid):
    perf_data = []

    while psutil.pid_exists(pid):
        # Purposefully ignoring the intial 0.0 read.
        psutil.cpu_percent(interval=None)
        cpu_percent = psutil.cpu_percent(interval=None)
        sw_mem_info = psutil.swap_memory()
        virt_mem_info = psutil.virtual_memory()

        perf_data.append({
            'cpu_percent': cpu_percent,
            'memory_swap': sw_mem_info.percent,
            'memory_virtual': virt_mem_info.percent
            'timestamp': int(time.time())
        })

        time.sleep(1)  # Wait for 1 second between measurements

    print(json.dumps(perf_data))

def run():
    target_language = os.environ["TARGET_LANGUAGE"]
    launch_script = launch_scripts[target_language]
    external_process = subprocess.Popen(launch_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pid = external_process.pid
    print(pid)
    monitor_thread = threading.Thread(target=monitor, args=[pid])
    monitor_thread.start()
    stdout, stderr = external_process.communicate()
    external_process.wait()
    external_process.terminate()
    monitor_thread.join()
    print(stdout)

if __name__ == "__main__":
    run()
