from socket import *
import os
from threading import Thread
from time import sleep

class ClientChat:
    def __init__(self, server_name, server_port):
        self.cs = socket(AF_INET, SOCK_STREAM)
        self.cs.connect((server_name, server_port))
        self.stop = True
        
    def set_nick(self):
        prov_nick = "/nick" + input("Introduzca nombre de usuario: ")
        self.cs.send(prov_nick.encode())
        server_ans = self.cs.recv(1024).decode().split("-")
        if server_ans[0] == "OK":
            os.system("cls||clear")
            print(server_ans[1])
            print("-"*len(server_ans[1]))
        else:
            print("Nombre de usuario ya existente.")
            self.set_nick()

    def send_message(self):
        while self.stop:
            msg = input("")
            if msg == "/exit":
                self.exit()
                self.stop = False
                break
            self.cs.send(msg.encode())

    def receive_messages(self):
        while self.stop:
            message = self.cs.recv(1024).decode()
            if message == "/kick":
                self.exit()
                self.stop = False
                break
            print(message)

    def exit(self):
        self.cs.send("/exit".encode())
        print("Saliste del Chat")


while True:
    try:
        os.system("cls||clear")
        ip = input("Introducir IP del chat: ")
        port = int(input("Introducir puerto del chat: "))
        chat = ClientChat(ip, port)
        print("Entrando al chat...")
        sleep(1)
        chat.set_nick()
        break
    except:
        print("IP o puerto erroneos.")
        sleep(3)

receive_thread = Thread(target=chat.receive_messages)
receive_thread.start()
send_thread = Thread(target=chat.send_message)
send_thread.start()