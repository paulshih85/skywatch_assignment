'''
Through a socket, this client prints the mean of a list of numbers provided by server.
'''
import os
import pickle
import socket


def client1() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # To reuse the same address immediately
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((os.environ['HOST'], int(os.environ['PORT'])))
        server.listen(10)
        print('Client1 is ready')
    except Exception as ex:
        print(f"Someting wrong while initiating Client1: {ex}")
        return

    conn, _ = server.accept()
    while True:
        data = conn.recv(4096)
        data = pickle.loads(data)

        if data == 'Q':
            conn.close()
            break

        print('Mean is ' + str(sum(data) / len(data)))

if __name__ == '__main__':
    client1()
