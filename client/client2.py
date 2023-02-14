'''
Through a pipe, this client prints the median of a list of numbers provided by server.
'''
from typing import List, Union
from multiprocessing import connection


def client2(conn: connection) -> None:
    while True:
        data = conn.recv()
        if data == 'Q':
            conn.close()
            break

        data.sort()
        idx, mod = divmod(len(data), 2)

        median = data[idx]
        if mod == 0:
            median = (median + data[idx-1]) / 2

        print('Median is ' + str(median))
