import socket
import psycopg2
import sys
import os
from dotenv import load_dotenv

VALID_QUERIES = ["What is the average moisture inside my kitchen fridge in the past three hours?",
                 "What is the average water consumption per cycle in my smart dishwasher?",
                 "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"]

FIRST_FRIDGE_ID = "id4-6e4-ls8-f7q"
DISHWASHER_ID = "7pz-ybr-8s0-6h3"
SECOND_FRIDGE_ID = "27a451a2-eac4-471d-8cf7-de13d8900eaf"

def get_client_requested_data(query_index):
    # Fetches data from Neon database
    cursor.execute('select PAYLOAD from "Assignment #8 Destination Table_virtual"')
    selected_rows = cursor.fetchall()

    if query_index == 0:
        moisture_measurements = []
        for row in selected_rows:
            current_payload = row[0]
            if current_payload["parent_asset_uid"] == FIRST_FRIDGE_ID:
                moisture_measurement = current_payload["Moisture Meter - Moisture Meter (Fridge)"]
                moisture_measurement = float(moisture_measurement)
                moisture_measurements.append(moisture_measurement)

        average_moisture_inside_first_fridge_in_past_three_hours = sum(moisture_measurements) / len(moisture_measurements)
        client_requested_data = f"Average moisture inside my kitchen fridge in the past three hours: {average_moisture_inside_first_fridge_in_past_three_hours:.3f}% Relative Humidity"

    elif query_index == 1:
        raise NotImplementedError

    elif query_index == 2:
        raise NotImplementedError

    else:
        assert False
        # raise ValueError

    return client_requested_data

# Obtains access to connection string safely
load_dotenv()
DATABASE_CONNECTION_STRING = psycopg2.connect(os.getenv("DATABASE_CONNECTION_STRING"))

# Tests connection to Neon
if DATABASE_CONNECTION_STRING:
    print("Connection with Neon successful!")
else:
    print("Nothing happened...")

cursor = DATABASE_CONNECTION_STRING.cursor()

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

    try:
        query_index = VALID_QUERIES.index(message_from_client)
        server_message = get_client_requested_data(query_index)
    except:
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
DATABASE_CONNECTION_STRING.close()
print("Shutting down connection with Neon...")
