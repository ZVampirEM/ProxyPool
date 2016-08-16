import threading
import time
from Lock import ThreadLock

is_to_exit = False

def show():
    global is_to_exit
    print ThreadLock.global_lock
    print "To Lock"
    ThreadLock.global_lock.Lock()
    while not is_to_exit:
        print "thread1 Lock Success!"
        time.sleep(5)
    ThreadLock.global_lock.UnLock()


def test_main():
    global is_to_exit
    t = threading.Thread(target=show)
    t.start()
    while True:
        input_info = raw_input()
        if input_info == 'exit':
            is_to_exit = True
            break

if __name__ == '__main__':
    test_main()
