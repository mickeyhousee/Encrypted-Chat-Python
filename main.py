# READ README.md

import os
from dotenv import load_dotenv
import socket
import threading

import rsa

load_dotenv('.env')
ip = os.getenv('IPADRESS')
port = int(os.getenv('PORT'))

choise = input('Do you want to Host (1) or to connect (2): ')

if choise == '1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    client, _ = server.accept()
elif choise == '2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.78", 9999))

else:
    exit()

def sending_messages(c):
    while True:
        message = input("")
        c.send(message.encode())
        print ('You: ' + message)

def receiving_messages(c):
    while True:
        print ('Partner: ' + c.recv(1024).decode())


threading.Thread(target=sending_messages, args=(client, )).start()
threading.Thread(target=receiving_messages, args=(client, )).start()