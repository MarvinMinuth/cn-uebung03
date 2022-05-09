# 1077466 - Marvin Minuth
import socket
import sys
import os


def client():
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect(('127.0.0.1', 4242))
    close = True
    error_raised = False

    def put(file_name, close_command="close"):
        try:
            file_size = os.path.getsize(file_name)
            file = open(file_name, 'rb')
            command_message = f'PUT {file_name}\nContent-Length: {file_size}\nConnection: {close_command}\n\n'
            print(command_message)
            command_length = len(command_message)
            command = command_length.to_bytes(1, 'big') + command_message.encode('utf-8')
            c_sock.send(command)
            data = file.read(1024)
            while data:
                c_sock.send(data)
                data = file.read(1024)
            file.close()
            return True
        except:
            print("File not found!")
            return False

    def get(file_name, close_command="close"):
        command_message = f'GET {file_name}\nConnection: {close_command}\n\n'
        print(command_message)
        command_length = len(command_message)
        command = command_length.to_bytes(1, 'big') + command_message.encode('utf-8')
        c_sock.send(command)

        answer_length = int.from_bytes(c_sock.recv(1),'big')
        answer = c_sock.recv(answer_length).decode('utf-8')
        print(answer)
        if answer.startswith('STATUS: FILE NOT FOUND'):
            return False

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
        return True

    def wait_for_server(close):
        answer_length = int.from_bytes(c_sock.recv(1), 'big')
        answer = c_sock.recv(answer_length).decode('utf-8')
        print(answer)
        if answer.startswith('STATUS: OK'):
            if close:
                c_sock.close()
                exit(0)

    while True:
        if not error_raised:  # wait for server if no error occurred
            wait_for_server(close)
        error_raised = False
        while True:  # loop until given input can be worked with
            command_line = f'{input("")}'
            try:
                command = command_line.split()[0]
                file = command_line.split()[1]
                if command == 'PUT' or command == 'GET':
                    break
                else:
                    print("Usage: PUT [filename] or GET [filename]")
            except:
                print("Usage: PUT [filename] or GET [filename]")

        # close_command may be None, 'close' or 'keep-alive'
        if len(command_line.split()) == 2:
            close_command = 'close'
        else:
            if 'keep-alive' in command_line:
                close_command = 'keep-alive'
            elif 'close' in command_line:
                close_command = 'close'
            else:
                close_command = f'{input("Connection: ")}'
        while close_command != "" and close_command != 'keep-alive' and close_command != 'close':
            print("Please enter 'keep-alive', 'close' or nothing")
            close_command = f'{input("Connection: ")}'
        if close_command == "keep-alive":
            close = False
        else:
            close = True

        if command == 'PUT':
            if not put(file, close_command):  # put() returns false if an error occurs
                error_raised = True
        elif command == 'GET':
            if not get(file, close_command):
                error_raised = True
                if close:
                    c_sock.close()
                    exit(0)
        else:
            print("Usage: PUT [filename] or GET [filename]")


def main():
    client()


if __name__ == '__main__':
    main()
