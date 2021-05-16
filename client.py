import random
import socket
import time
from encryption import Encryption

class Keys:
    """ КЛЮЧИ ШИФРОВАНИЯ """
    def __init__(self):
        self.a = random.randint(100, 100000)
        self.g = random.randint(50000, 100000)
        self.p = random.randint(100, 49999)
        self.A = self.g ** self.a % self.p
        self.B = 0
        self.status = True

    def get_K(self):
        K = self.B ** self.a % self.p
        return K

key = Keys()
enc = Encryption()  # шифр

""" АДРЕС И ПОРТ СЕРВЕРА """
sock = socket.socket()
server = input('Enter Server: ')  # 'localhost'
port = input('Enter Port: ')  # 9090
print()


""" ПОДКЛЮЧЕНИЕ К СЕРВЕРУ """
try:
    sock.connect((server, int(port)))
    # server
    print(f"Server IP: {server}; Port: {port}")

    # client
    host = sock.getsockname()
    print(f"Client IP: {host[0]}; Port: {host[1]}")
except ConnectionRefusedError as c:
    print(f"ERROR: {c}")


""" ОСНОВНОЙ ЦИКЛ """
while True:
    if key.status:
        # ОТПРАВКА КЛЮЧЕЙ ШИФРОВАНИЯ СЕРВЕРУ
        sock.send(f'key-A: {key.A}'.encode())
        time.sleep(0.25)  # небольшая задержка, чтобы сервер успел обработать сообщение
        sock.send(f'key-g: {key.g}'.encode())
        time.sleep(0.25)
        sock.send(f'key-p: {key.p}'.encode())
        time.sleep(0.25)
        print(f'key-A: {key.A}\nkey-g: {key.g}\nkey-p: {key.p}')

        # ЦИКЛ ДЛЯ ШИФРОВАНИЯ
        while True:
            data = sock.recv(1024).decode("utf8")
            if data[:5] == 'key-B':
                key.B = int(data.split(' ')[1])
                print(key.a)
                print(f'key-B: {key.B}')
                print(f'key-K: {key.get_K()}')
            if key.B != 0:
                break
        key.status = False

    # СООБЩЕНИЕ КЛИЕНТА
    msg = input("\nYou: ")
    new_msg = enc.Msg_Bytes(msg, key.get_K())
    sock.send(new_msg.encode())

    # ОТКЛЮЧЕНИЕ ОТ СЕРВЕРА
    if len(msg) == 0 or msg.lower() == 'stop' or msg.lower() == 'exit':
        print("You disconnected.")
        break

    # СООБЩЕНИЕ СЕРВЕРА
    try:
        old_data = sock.recv(1024).decode("utf8")
        data = enc.Bytes_Msg(old_data, key.get_K())
        print(f"\nServer: {data}")
    except ConnectionResetError as e:
        print(f"ERROR: {e}")
        break

sock.close()
