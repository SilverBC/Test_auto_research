import psutil
import time
import subprocess
import json
import threading

def monitor(pid):
    perf_data = []

    # Purposefully ignoring the intial 0.0 read.
    psutil.cpu_percent(interval=None)

    while psutil.pid_exists(pid):
        cpu_percent = psutil.cpu_percent(interval=None)
        sw_mem_info = psutil.swap_memory()
        virt_mem_info = psutil.virtual_memory()

        perf_data.append({
            'cpu_percent': cpu_percent,
            'memory': {
                'swap_percent': sw_mem_info.percent,
                'virtual_percent': virt_mem_info.percent
            },
            'timestamp': int(time.time())
        })

        time.sleep(1)  # Wait for 1 second between measurements

    print(json.dumps(perf_data))

def run():
    external_process = subprocess.Popen(['/usr/bin/mvn', '-B', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
