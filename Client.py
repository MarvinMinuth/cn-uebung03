import socket
import threading
import os


def client():
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect(('127.0.0.1', 4242))

    def receive():
        while True:
            message = c_sock.recv(255).decode('utf-8')
            print(message)
            if message.startswith("STATUS: OK"):
                print('Close...')
                write_thread.join()
                print(write_thread.is_alive())
                receive_thread.join()
                print(receive_thread.is_alive())
                c_sock.close()
                exit(0)

    def write():
        while True:
            message = f'{input("")}'
            if message.startswith('PUT'):
                put(message)
            # elif message.startswith('GET'):
            #     get()
            else:
                print('Options: "PUT {filename}" or "GET {filename}"')

    def put(message):
        # filename = message[4:]
        filename = '2022S_CN04_Ethernet.pdf'
        try:
            file_size = os.path.getsize(filename)
            file = open(filename, 'rb')
            print(f'Content-Length: {file_size}\n')
            c_sock.send(f'PUT {filename}\n{file_size}\n\n'.encode('UTF-8'))
            data = file.read(1024)
            while data:
                c_sock.send(data)
                data = file.read(1024)
            file.close()
        except:
            print("File not found!")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


def main():
    client()


if __name__ == '__main__':
    main()
