import logging
import threading
import time
import datetime
from pynput import keyboard


def on_press(key):
    try:
        print("alphanumeric key {0} pressed".format(key.char))
    except AttributeError:
        print("special key {0} pressed".format(key))


def on_release(key):
    # print("{0} released".format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def stop_threads():
    global doloop1, doloop2
    doloop1 = False
    doloop2 = False


def thread_function1(name):
    global doloop1
    logging.info("Thread %s: starting", name)
    print("This thread shows the time every 5 seconds...")
    doloop1 = True
    while doloop1:
        tim = datetime.datetime.now()
        print(f"Thread 1 Time: {tim:%X}")
        time.sleep(5)
    logging.info("Thread %s: finishing", name)


def thread_function2(name):
    global doloop2
    logging.info(f"Thread {name}: Starting")
    print("This thread shows the time every 10 seconds...")
    doloop2 = True
    while doloop2:
        tim = datetime.datetime.now()
        print(f"Thread 2 Time: {tim:%X}")
        time.sleep(10)
    logging.info("Thread %s: finishing", name)


def mainloop():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    t1 = threading.Thread(target=thread_function1, args=(1,), daemon=True)
    t2 = threading.Thread(target=thread_function2, args=(2,), daemon=True)
    logging.info("Main    : before running thread")
    print("Press the <Esc> key to exit...")
    t1.start()
    t2.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    logging.info("Main    : wait for the thread to finish")
    stop_threads()
    logging.info("Main    : all done")
    logging.info("Ending Program!")


if __name__ == "__main__":
    mainloop()
