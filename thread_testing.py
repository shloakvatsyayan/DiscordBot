import threading
import time


def thread_function():
    while True:
        print("Hello")
        time.sleep(1)


class Hello:
    def __init__(self, name):
        self.name = name

    def say_hello_forever(self):
        while True:
            print("Hello {}".format(self.name))
            time.sleep(1)


if __name__ == '__main__':
    shloak  = Hello("Shloak")
    mama = Hello("Mama")
    shloak_thread  = threading.Thread(target=shloak.say_hello_forever)
    mama_thread  = threading.Thread(target=mama.say_hello_forever)
    #shloak_thread.start()
    #mama_thread.start()
    #mama_thread.join()