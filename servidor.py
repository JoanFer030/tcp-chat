from socket import *
from threading import Thread
import os

class ServerChat:
    def __init__(self, server_port):
        self.users = {}
        self.chat_name = "Prueba de chat TCP"
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        self.server_socket.bind(("", server_port))
        self.server_socket.listen()

    def send_to_all(self, msg, cs):
        print(msg)
        for client in self.users:
            if client != cs:
                client.send(msg.encode())

    def welcome(self):
        while True:
            connection_socket, address = self.server_socket.accept()
            print(f"> Nuevo usuario con dirección: {address}")
            listen_thread = Thread(target=self.listen, args=(connection_socket, ))
            listen_thread.start()

    def listen(self, connection_socket):
        while True:
            msg = connection_socket.recv(1024).decode()
            if msg.startswith("/nick") and msg[5:] not in self.users.values():
                nick = msg[5:]
                self.users[connection_socket] = nick
                connection_socket.send(f"OK-Bienvenido a {self.chat_name}".encode())
                self.send_to_all(f"> Nuevo usuario '{nick}'", connection_socket)
            elif msg.startswith("/nick") and msg[5:] in self.users.values():
                connection_socket.send("NO".encode())
            else:
                msg = "> " + self.users[connection_socket] + ": " + msg
                self.send_to_all(msg, connection_socket)


chat = ServerChat(12000)
os.system("cls||clear")
print("El servidor está listo para recibir")
chat.welcome()