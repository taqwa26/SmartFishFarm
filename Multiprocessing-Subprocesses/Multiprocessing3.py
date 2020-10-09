import multiprocessing
import time

class MyProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            pass
        print ("You exited!")

    def shutdown(self):
        print ("Shutdown initiated")
        self.exit.set()


if __name__ == "__main__":
    process = MyProcess()
    process.start()
    print ("Waiting for a while")
    time.sleep(3)
    process.shutdown()
    time.sleep(3)
    print ("Child process state: %d" % process.is_alive())