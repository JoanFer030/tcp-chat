from socket import *
from threading import Thread
import os

class ServerChat:
    def __init__(self, server_port):
        self.users = {}
        self.commands_dict = {
            "/users" : "lista los usuarios actuales",
            "/kick <user>" : "expulsa al usuario, user, del chat",
            "/info" : "información del servidor",
        }
        self.chat_name = "Prueba de chat TCP"
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        self.server_socket.bind(("", server_port))
        self.server_socket.listen()

    def send_to_all(self, msg, cs=""):
        for client in self.users:
            if client != cs:
                client.send(msg.encode())

    def welcome(self):
        while True:
            connection_socket, address = self.server_socket.accept()
            listen_thread = Thread(target=self.listen, args=(connection_socket, address))
            listen_thread.start()

    def listen(self, connection_socket, address):
        while True:
            try:
                msg = connection_socket.recv(1024).decode()
                if msg.startswith("/nick") and msg[5:] not in self.users.values():
                    nick = msg[5:]
                    self.users[connection_socket] = (nick, address)
                    connection_socket.send(f"OK-Bienvenido a {self.chat_name}".encode())
                    self.send_to_all(f"> Nuevo usuario '{nick}'", connection_socket)
                    print(f"server > Nuevo usuario con dirección: {address[0]} y nick: {nick}")
                elif msg.startswith("/nick") and msg[5:] in self.users.values():
                    connection_socket.send("NO".encode())
                else:
                    msg = "> " + self.users[connection_socket] + ": " + msg
                    print(msg)
                    self.send_to_all(msg, connection_socket)
            except:
                msg = f"> {self.users[connection_socket]} abandono el chat"
                print(msg)
                self.send_to_all(msg, connection_socket)
                connection_socket.close()
                del self.users[connection_socket]
                break

    def commands(self):
        while True:
            command = input("")
            if command == "/users":
                print("\nUsuario", " "*8, "Dirección")
                print("-"*50)
                for client, info in self.users.items():
                    n = 15-len(info[0])
                    print(info[0], " "*n, info[1])
            elif command.startswith("/kick"):
                nick = command[5:]
                
            elif command == "/help":
                print("\nComando", " "*8, "Descripción")
                print("-"*50)
                for name, description in self.commands_dict.items():
                    n = 15-len(name)
                    print(name, " "*n, description)
            elif command == "/info":
                print("\nInformación")
                print("-"*50)
            else:
                print("server > Comando no existente")
            
            


chat = ServerChat(12000)
os.system("cls||clear")
print("El servidor está listo para recibir")
commands_thread = Thread(target=chat.commands)
commands_thread.start()
welcome_thread = Thread(target=chat.welcome)
welcome_thread.start()
