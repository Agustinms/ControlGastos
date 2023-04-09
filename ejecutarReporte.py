import multiprocessing
import time
import os
import threading


def ejecutar_plot():
    os.system("python plotply_script.py")

def ejecutar_browser():
    os.system("python browser.py") 



if __name__ == '__main__':
    p1 = multiprocessing.Process(target=ejecutar_plot)
    p2 = multiprocessing.Process(target=ejecutar_browser)

 
    p1.start()
    p2.start()
    time.sleep(3)
    p1.terminate()
    p1.join()
    p2.terminate()
    p2.join()