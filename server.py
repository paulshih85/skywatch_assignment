import argparse
from multiprocessing import Lock, Pipe, Process, Array, Value
import os
import pickle
import socket
import time
from typing import List, Literal, Union

from client.client2 import client2
from client.client3 import client3


def send_socket(skt: socket.socket, nums: Union[List[int], Literal['Q']]):
    if skt is None:
        return None
    try:
        skt.send(pickle.dumps(nums))
    except Exception as ex:
        print(f"Fail to send nums to Client1: {ex}")


def send_pipe(pipe: Pipe, nums: Union[List[int], Literal['Q']]):
    if pipe is None:
        return None
    try:
        pipe.send(nums)
    except Exception as ex:
        print(f"Fail to send nums to Client2: {ex}")


def send_shm(shm_length: Value, shm: Array, pos: int, nums: List[int]):
    if shm is None:
        return None
    shm_length.value = pos
    if pos > 0:
        shm[:pos] = nums


def server(lock, skt=None, pipe=None, shm_length=None, shm=None):
    while True:
        with lock:
            nums = input('Server is ready. You can type intergers and then click [ENTER].'
                         'Clients will show the mean, median, and mode of the input values.\n')

            if nums == 'Q':
                send_socket(skt, nums)
                send_pipe(pipe, nums)
                send_shm(shm_length, shm, -1, [])
                break

            try:
                if not nums.strip():
                    print('Empty input. Please provide integers')
                    continue
                nums = [int(n) for n in nums.split()]
            except ValueError:
                print('Invalid input format. Please provide integers only')
            else:
                send_socket(skt, nums)
                send_pipe(pipe, nums)
                send_shm(shm_length, shm, len(nums), nums)
        time.sleep(1) # Switch to Client3

    if skt:
        skt.close()
    if pipe:
        pipe.close()


def create_socket():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((os.environ['HOST'], int(os.environ['PORT'])))
        return client
    except Exception as ex:
        print(f"Fail to connect to socket server: {ex}")
        return None


def main():
    '''
    If failing to connect to any of the clients, it just returns
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--client1', action='store_true', help='get mean')
    parser.add_argument('--client2', action='store_true', help='get median')
    parser.add_argument('--client3', action='store_true', help='get modes')
    args = parser.parse_args()

    process_list = []
    lock = Lock()
    server_kwargs = {'lock': lock}

    if args.client1:
        client_socket = create_socket()
        if client_socket:
            server_kwargs['skt'] = client_socket
        else:
            return

    if args.client2:
        r_pipe, w_pipe = Pipe()
        proc = Process(target=client2, args=(r_pipe,))
        proc.start()
        process_list.append(proc)

        server_kwargs['pipe'] = w_pipe
        print('Client2 is ready')

    if args.client3:
        shm = Array('i', 4096)
        length = Value('i', 0)
        proc = Process(target=client3, args=(length, shm, lock))
        proc.start()
        process_list.append(proc)

        server_kwargs['shm'] = shm
        server_kwargs['shm_length'] = length
        print('Client3 is ready')

    server(**server_kwargs)

    for process in process_list:
        process.join()


if __name__ == '__main__':
    main()
