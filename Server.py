# 1077466 - Marvin Minuth
import socket
import sys
import os


def server():
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind(('127.0.0.1', 4242))
    s_sock.listen()
    connected = False
    close = False

    def client_put(message):
        file_name = message.split()[1]
        file_path = './put/'+file_name
        file_size = int(message.split()[2])
        file = open(file_path, 'wb')
        while file_size > 0:
            if file_size >= 1024:
                data = c_sock.recv(1024)
                file_size -= 1024
            else:
                data = c_sock.recv(file_size)
                file_size = 0
            print(bin(int.from_bytes(data, byteorder=sys.byteorder)))
            file.write(data)
        file.close()
        c_sock.send('STATUS: OK\n\n'.encode('UTF-8'))

    def client_get(message, close_command):
        file_name = message.split()[1]
        print(f"GET {file_name}\nConnection: {close_command}")
        try:
            file_size = os.path.getsize(file_name)
            print(f"Content-Length: {file_size}")
            file = open(file_name, 'rb')
            c_sock.send(f'STATUS: OK\nContent-Length: {file_size}\n\n'.encode('UTF-8'))
            data = file.read(1024)
            while data:
                c_sock.send(data)
                data = file.read(1024)
            file.close()

        except:
            c_sock.send("STATUS: FILE NOT FOUND".encode('utf-8'))
            return

        c_sock.send('STATUS: OK\n\n'.encode('UTF-8'))


    while True:
        if not connected:
            c_sock, c_addr = s_sock.accept()
            print('Client connected')
            c_sock.send("Connected to server.".encode('utf-8'))
            connected = True
        if close:
            c_sock.close()
            s_sock.close()
            exit(0)
        message = c_sock.recv(1024).decode('utf-8')
        command = message[:3]
        if command == 'PUT':
            try:
                close_command = message.split()[3]
            except:
                close_command = "close"
            if close_command != 'keep-alive':
                close = True
            client_put(message)
        elif command == 'GET':
            try:
                close_command = message.split('\n')[1]
            except:
                close_command = "close"
            if close_command != 'keep-alive':
                close = True
            client_get(message, close_command)



def main():
    server()


if __name__ == '__main__':
    main()
