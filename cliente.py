from socket import *
import os
from threading import Thread
from time import sleep
from cryptography.fernet import Fernet

class ClientChat:
    def __init__(self, server_name, server_port):
        self.cs = socket(AF_INET, SOCK_STREAM)
        self.cs.connect((server_name, server_port))
        self.stop = True
        self.fernet = None

    def decrypt_msg(self,enc_msg):
        msg = self.fernet.decrypt(enc_msg).decode()
        return msg

    def encrypt_msg(self,msg):
        enc_msg = self.fernet.encrypt(msg.encode())
        return enc_msg

    def set_key(self):
        message = self.cs.recv(1024)
        if message.decode().startswith("/key"):
            key = message.decode().replace("/key", "").encode()
            self.fernet = Fernet(key)
            self.cs.send(self.encrypt_msg("key-ok"))
            message = self.decrypt_msg(self.cs.recv(1024))
            if message != "ok":
                print("Clave de encriptado no recibida correctamente.")
        
    def set_nick(self):
        prov_nick = input("Introduzca nombre de usuario: ")
        self.cs.send(self.encrypt_msg(prov_nick))
        server_ans = self.cs.recv(1024)
        server_ans = self.decrypt_msg(server_ans).split("-")
        if server_ans[0] == "OK":
            os.system("cls||clear")
            n = 50 - len(server_ans[1])
            print(server_ans[1]," "*n, "Usuario: ", prov_nick[5:])
            print("-"*70)
        else:
            print("Nombre de usuario ya existente.")
            self.set_nick()

    def send_message(self):
        while self.stop:
            msg = input("")
            if msg == "/exit":
                check = input("Seguro que desea abandonar el chat, se borrarán todos los mensajes, (0/1): ")
                if check == "1":
                    self.exit()
                    self.stop = False
                    break
                else:
                    continue
            self.cs.send(self.encrypt_msg(msg))

    def receive_messages(self):
        while self.stop:
            message = self.cs.recv(1024)
            message = self.decrypt_msg(message)
            if message == "/kick":
                self.exit()
                self.stop = False
                break
            print(message)

    def exit(self):
        self.cs.send(self.encrypt_msg("/exit"))
        os.system("cls||clear")
        print("Saliste del Chat")



os.system("cls||clear")
ip = input("Introducir IP del chat: ")
port = int(input("Introducir puerto del chat: "))
chat = ClientChat(ip, port)
print("Entrando al chat...")
chat.set_key()
sleep(1)
chat.set_nick()

receive_thread = Thread(target=chat.receive_messages)
receive_thread.start()
send_thread = Thread(target=chat.send_message)
send_thread.start()

