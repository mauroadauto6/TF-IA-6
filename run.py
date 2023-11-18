import sys
import webbrowser
import multiprocessing
from os.path import dirname, abspath

wspace_path = abspath(dirname(dirname(__file__)))
sys.path.append(wspace_path)

from wspace.main import app as mainAPP
from wspace2.monitor import app as monitorAPP

def run_main():
    mainAPP.run(port=5000)

def run_monitor():
    monitorAPP.run(port=5001, threaded=True)
    
if __name__ == "__main__":
    main_process = multiprocessing.Process(target=run_main)
    monitor_process = multiprocessing.Process(target=run_monitor)
    
    webbrowser.open('http://127.0.0.1:5000')
    webbrowser.open('http://127.0.0.1:5001')
    
    main_process.start()
    monitor_process.start()
    
    main_process.join()
    monitor_process.join()
