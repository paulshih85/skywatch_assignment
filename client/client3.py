'''
Through shared memory, this client prints the modes of a list of numbers provided by server.
'''
from collections import Counter
import time
from multiprocessing import Array, Lock, Value


def client3(length: Value, shm: Array, lock: Lock):
    while True:
        with lock:
            if length.value == -1:
                break

            if length.value > 0:
                nums = shm[:length.value]
                cnter = Counter(nums)
                modes = [k for k, v in cnter.items()
                         if v == cnter.most_common(1)[0][1]]
                text = "Modes are"
                if len(modes) == 1:
                    modes = modes[0]
                    text = "Mode is"

                print(f"{text} {modes}")
                length.value = 0
        time.sleep(1) # Switch to Server
