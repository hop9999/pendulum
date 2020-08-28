import threading
import time

def f():
    print("hello world")  # your code here
    #myThread.run()

if __name__ == '__main__':
    myThread = threading.Timer(0.004, f)  # timer is set to 3 seconds
    myThread.start()
    time.sleep(5)  # it can be loop or other time consuming code here
    if myThread.is_alive():
        myThread.cancel()