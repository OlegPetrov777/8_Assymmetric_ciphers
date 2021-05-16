import random
import socket
import datetime
import time
from encryption import Encryption


def save_log(text):
    print(text)
    log = open("logs.txt", "a")  # запись логов
    now = datetime.datetime.now()  # текущее время
    log.write('<<' + str(now) + '>> ' + text + '\n')
    log.close()


class Keys:
    """ КЛЮЧИ ШИФРОВАНИЯ """
    def __init__(self):
        self.b = random.randint(100, 100000)
        self.g = 0
        self.p = 0
        self.A = 0
        self.status = True

    def get_B(self):
        B = self.g ** self.b % self.p
        return B

    def get_K(self):
        K = self.A ** self.b % self.p
        return K

key = Keys()
enc = Encryption()  # шифр


""" СТАРТ СЕРВЕРА """
sock = socket.socket()
save_log('Server is starting.')

port = input('Enter port: ')  # вводим порт
sock.bind(('', int(port)))


""" ОСНОВНОЙ ЦИКЛ """
while True:

    """ ПРОСЛУШКА ПОРТА """
    sock.listen(1)
    save_log(f"Listening to the port ({port})")


    """ НОВЫЙ СОКЕТ И АДРЕС КЛИЕНТА """
    conn, addr = sock.accept()
    save_log(f"Connected to {addr[0]}:{addr[1]}")
    print()
    key.status = True

    while True:
        # ОТПРАВКА ОТКРЫТОГО КЛЮЧА
        if key.A != 0 and key.p != 0 and key.g != 0 and key.status:  # если получили все открытые ключи Клиента
            print(f'send: key-B = {key.get_B()}')
            print(f'key-K: {key.get_K()}')
            key.status = False
            time.sleep(0.25)
            conn.send(f'key-B: {key.get_B()}'.encode())  # отправляем открытый ключ В от Сервера

        # ПОЛУЧЕНИЕ СООБЩЕНИЯ ОТ КЛИЕНТА
        try:
            data = conn.recv(1024).decode("utf8")
        except ConnectionResetError as e:
            save_log(f"ERROR: {e}")
            break

        # ПОЛУЧЕНИЕ КЛЮЧЕЙ ШИФРОВАНИЯ КЛИЕНТА
        if data[:5] == 'key-A':
            print(data)
            key.A = int(data.split(' ')[1])
        elif data[:5] == 'key-g':
            print(data)
            key.g = int(data.split(' ')[1])
        elif data[:5] == 'key-p':
            print(data)
            key.p = int(data.split(' ')[1])
        else:

            # СООБЩЕНИЯ
            old_data = data  # зашифрованное сообщение
            data = enc.Bytes_Msg(data, key.get_K())  # расшифрованное
            new_data = enc.Msg_Bytes(data + '!!!', key.get_K())  # новое

            # ВЫХОД КЛИЕНТА
            if data == "" or data == "exit":
                save_log(f"Client disconnected.")
                break
            elif data == "stop":
                break
            else:

                # ОБРАТНАЯ ОТПРАВКА СООБЩЕНИЯ
                conn.send(new_data.encode())

                # ЛОГИ
                save_log(f"Accepting old-data: {old_data}")
                save_log(f"Accepting data: {data}")
                save_log(f"Sending new-data: {new_data}")
                print()
    if data == "stop":
        break

save_log('Closing connection.')
conn.close()
