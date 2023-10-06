import psutil
import time
import subprocess
import json
import threading

def monitor(pid):
    perf_data = []

    try:
        while psutil.pid_exists(pid):
            print("we are in bois")
            cpu_percent = psutil.cpu_percent(interval=None)
            sw_mem_info = psutil.swap_memory()
            virt_mem_info = psutil.virtual_memory()

            perf_data.append({
                'cpu_percent': cpu_percent,
                'memory_info': {
                    'swap_percent': sw_mem_info.percent,
                    'virtual_percent': virt_mem_info.percent
                },
                'timestamp': int(time.time())
            })

            time.sleep(1)  # Wait for 1 second between measurements
    except KeyboardInterrupt:
        pass
    print(json.dumps(perf_data))

def run():
    external_process = subprocess.Popen(['/usr/bin/mvn', '-B', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # TODO: why does python keep the external process alive???
    pid = external_process.pid
    print(pid)
    monitor_thread = threading.Thread(target=monitor, args=[pid])
    monitor_thread.run()
