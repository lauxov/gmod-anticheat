import psutil

# Kill processes by name
def kill_processes(process_names):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in process_names:
            proc.kill()