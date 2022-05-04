# 1077466 - Marvin Minuth
import socket
import threading


def server():
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind(('127.0.0.1', 123))
    s_sock.listen()

    def client_put(message):
        file_name = message.strip[1]
        file_path = 'put/'+file_name
        file_size = message.strip[2]
        file = open(file_name, 'wb')
        while file_size > 0:
            if file_size >= 1024:
                data = c_sock.recv(1024)
                file_size -= 1024
            else:
                data = c_sock.recv(file_size)
                file_size = 0
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(data)
            file.write(data)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        file.close()
        print("File closed")
        c_sock.send('STATUS: OK\n\n'.encode('UTF-8'))
        c_sock.close()
        print("Socket closed")
        s_sock.close()
        print("Server closed")

    while True:
        c_sock, c_addr = s_sock.accept()
        print('Client connected')
        c_sock.send("Connected to server.".encode('utf-8'))
        message = c_sock.recv(1024).decode('utf-8')
        print(message)
        command = message[:3]
        if command == 'PUT':
            client_put(message)


def main():
    server()


if __name__ == '__main__':
    main()
