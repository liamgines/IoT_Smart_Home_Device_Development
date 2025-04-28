import socket
import psycopg2
import sys
import os
from dotenv import load_dotenv

# Obtains access to connection string safely
load_dotenv()
db_connection_str = psycopg2.connect(os.getenv("DATABASE_CONNECTION_STRING"))

# Tests connection to Neon
if db_connection_str:
    print("Connection with Neon successful!")
else:
    print("Nothing happened...")


# Fetches data from Neon database
cursor = db_connection_str.cursor()
cursor.execute('select PAYLOAD from "Assignment 7 Demo Table_virtual"')
queries = cursor.fetchall()

for query in queries:
    print(query)

print("\nRunning server...")
# Creates socket for network communication using IPV4 and TCP
my_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port_num = str(sys.argv[1]), int(sys.argv[2])
#  Tells the socket to associate itself with all possible host addresses and the provided port number
my_tcp_socket.bind((host, port_num))
# Listens to port for a response
my_tcp_socket.listen(5)
# Extracts info from the first client connection established
client, client_address = my_tcp_socket.accept()
print("Connection established!")

while True:

    # Recieves data (of max size of 1024 bytes) from client
    message_from_client = str((client.recv(1024)).decode())
    print(f"Message from Client: {message_from_client}")

    # Modifies the client message received to be all uppercased
    server_message = message_from_client.upper()

    # Indicates Server-Client communication should cease
    if message_from_client == "":
        break

    # Replies to client by sending it an uppercased version of client's sent message
    client.send(bytearray(str(server_message), encoding='utf-8'))
    
# Closes connection with Client
client.close()
print("Shutting down communications on server side...")

# Closes connection with Neon database
db_connection_str.close()
print("Shutting down connection with Neon...")