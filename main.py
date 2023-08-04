# Import necessary libraries
import os
from dotenv import load_dotenv
import socket
import threading
import rsa

# Generate RSA key pair (public_key, private_key) with 1024-bit length
public_key, private_key = rsa.newkeys(1024)
public_partner = None

# Load environment variables from '.env' file
load_dotenv('.env')
ip = os.getenv('IPADRESS')  # Get IP address from environment variable
port = int(os.getenv('PORT'))  # Get port number from environment variable

# Ask user to choose hosting or connecting
choise = input('Do you want to Host (1) or to connect (2): ')

# Hosting logic
if choise == '1':
    # Create a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))  # Bind the socket to the specified IP and port
    server.listen()  # Listen for incoming connections
    client, _ = server.accept()  # Accept a client connection
    client.send(public_key.save_pkcs1("PEM"))  # Send the server's public key to the client
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))  # Receive and load the client's public key

# Connecting logic
elif choise == '2':
    # Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))  # Connect to the server
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))  # Receive and load the server's public key
    client.send(public_key.save_pkcs1("PEM"))  # Send the client's public key to the server

else:
    exit()  # Exit the program if an invalid choice is made

# Function to send messages to the partner
def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))  # Encrypt and send the message
        print('You: ' + message)

# Function to receive messages from the partner
def receiving_messages(c):
    while True:
        print('Partner: ' + rsa.decrypt(c.recv(1024), private_key).decode())  # Decrypt and print the received message

# Start two threads for sending and receiving messages
threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
