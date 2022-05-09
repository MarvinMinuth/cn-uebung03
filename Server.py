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

    def client_put(file_name, file_size, close_command):
        print(f'\nPUT {file_name}\nContent-Length:{file_size}\nConnection: {close_command}\n\n')
        file_path = './put/' + file_name
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
        answer_message = 'STATUS: OK\n\n'
        answer_length = len(answer_message)
        answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
        c_sock.send(answer)
        print('\nSTATUS: OK')

    def client_get(file_name, close_command):
        print(f"GET {file_name}\nConnection: {close_command}")
        try:
            file_size = os.path.getsize(file_name)
            file = open(file_name, 'rb')
            answer_message = f'STATUS: OK\nContent-Length: {file_size}\n'
            answer_length = len(answer_message)
            answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
            c_sock.send(answer)
            data = file.read(1024)
            while data:
                print(bin(int.from_bytes(data, byteorder=sys.byteorder)))
                c_sock.send(data)
                data = file.read(1024)
            file.close()

        except:
            answer_message = "STATUS: FILE NOT FOUND"
            answer_length = len(answer_message)
            answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
            c_sock.send(answer)
            print("STATUS: FILE NOT FOUND")
            return

        answer_message = 'STATUS: OK\n\n'
        answer_length = len(answer_message)
        answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
        c_sock.send(answer)
        print('STATUS: OK')

    while True:
        if not connected:
            c_sock, c_addr = s_sock.accept()
            print('Client connected')
            answer_message = "Connected to server."
            answer_length = len(answer_message)
            answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
            c_sock.send(answer)
            connected = True
        if close:
            c_sock.close()
            s_sock.close()
            exit(0)
        length = int.from_bytes(c_sock.recv(1), 'big')
        message = c_sock.recv(length).decode('utf-8')
        command = message[:3]
        file_name = message.split('\n')[0][4:]

        close_command = 'close'
        file_size = 0
        for line in message.split('\n'):
            if line.startswith('Content-Length:'):
                file_size = int(line.split()[1])
            if line.startswith('Connection:'):
                close_command = line.split()[1]
        if close_command != 'keep-alive':
            close = True

        if command == 'PUT':
            if file_size == 0:
                print('ERROR: NO FILE SIZE GIVEN')
                answer_message = "ERROR: NO FILE SIZE GIVEN"
                answer_length = len(answer_message)
                answer = answer_length.to_bytes(1, 'big') + answer_message.encode('utf-8')
                c_sock.send(answer)
            else:
                client_put(file_name, file_size, close_command)
        elif command == 'GET':
            client_get(file_name, close_command)


def main():
    server()


if __name__ == '__main__':
    main()
