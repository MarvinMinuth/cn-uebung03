import socket
import sys
import os


def client():
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect(('127.0.0.1', 4242))
    close = True

    def put(command, close_command="close"):
        # file_name = command[3:]
        file_name = '2022S_CN04_Ethernet.pdf'
        try:
            file_size = os.path.getsize(file_name)
            file = open(file_name, 'rb')
            print(f'Content-Length: {file_size}\n')
            c_sock.send(f'PUT {file_name}\n{file_size}\n{close_command}\n\n'.encode('UTF-8'))
            data = file.read(1024)
            while data:
                c_sock.send(data)
                data = file.read(1024)
            file.close()
        except:
            print("File not found!")

    def get(command, close_command="close"):
        # filename = command[3:]
        file_name = '2022S_CN04_Ethernet.pdf'
        c_sock.send(f'GET {file_name}\n{close_command}\n'.encode('UTF-8'))

        answer = c_sock.recv(1024).decode('utf-8')
        print(answer)
        if answer.startswith('STATUS: FILE NOT FOUND'):
            return

        file_size = int(answer.split()[3])
        file_path = './get/' + file_name
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

    while True:
        confirmation = c_sock.recv(255).decode('utf-8')
        if confirmation.startswith('STATUS: OK'):
            if close:
                c_sock.close()
                exit(0)
        print(confirmation)

        command = f'{input("")}'
        if command.startswith('PUT'):
            close_command = f'{input("Connection: ")}'
            if close_command == "keep-alive":
                close = False
            else:
                close = True
            put(command, close_command)
        elif command.startswith('GET'):
            close_command = f'{input("Connection: ")}'
            if close_command == "keep-alive":
                close = False
            else:
                close = True
            get(command, close_command)
        else:
            print("Usage: PUT [filename] or GET [filename]")


def main():
    client()


if __name__ == '__main__':
    main()
