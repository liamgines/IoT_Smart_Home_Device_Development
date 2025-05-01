import socket
import psycopg2
import sys
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

THREE_HOURS = 3
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
SECONDS_PER_THREE_HOURS = THREE_HOURS * MINUTES_PER_HOUR * SECONDS_PER_MINUTE

VALID_QUERIES = ["What is the average moisture inside my kitchen fridge in the past three hours?",
                 "What is the average water consumption per cycle in my smart dishwasher?",
                 "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"]

FIRST_FRIDGE_ID = "id4-6e4-ls8-f7q"
DISHWASHER_ID = "7pz-ybr-8s0-6h3"
SECOND_FRIDGE_ID = "27a451a2-eac4-471d-8cf7-de13d8900eaf"

def get_client_requested_data(query_index):
    # Fetches data from Neon database
    cursor.execute('select PAYLOAD, TIME from "Assignment #8 Destination Table_virtual"')
    selected_rows = cursor.fetchall()

    if query_index == 0:
        moisture_measurements = []

        for row in selected_rows:
            current_payload = row[0]
            current_creation_time = row[1]
            if current_payload["parent_asset_uid"] == FIRST_FRIDGE_ID:
                time_diff = datetime.now(timezone.utc) - current_creation_time
                # Skips; doesn't account for data not within the past 3 hours
                if time_diff.seconds > SECONDS_PER_THREE_HOURS:
                    continue
                moisture_measurement = current_payload["Moisture Meter - Moisture Meter (Fridge)"]
                moisture_measurement = float(moisture_measurement)
                moisture_measurements.append(moisture_measurement)

        if moisture_measurements:
            average_moisture_inside_first_fridge_in_past_three_hours = sum(moisture_measurements) / len(moisture_measurements)
            client_requested_data = f"Average moisture inside my kitchen fridge in the past three hours: {average_moisture_inside_first_fridge_in_past_three_hours:.2f}% Relative Humidity"

        else:
            client_requested_data = f"Fridge did not produce any moisture data within the past three hours"

    elif query_index == 1:
        water_consumption_measurements = []

        for row in selected_rows:
            current_payload = row[0]
            if current_payload["parent_asset_uid"] == DISHWASHER_ID:
                water_consumption_measurement = current_payload["YF-S201 - Water Consumption Sensor (Dishwasher)"]
                water_consumption_measurement = float(water_consumption_measurement)
                water_consumption_measurements.append(water_consumption_measurement)

        if water_consumption_measurements:
            average_water_consumption_per_cycle_in_dishwasher = sum(water_consumption_measurements) / len(water_consumption_measurements)
            client_requested_data = f"Average water consumption per cycle in my smart dishwasher: {average_water_consumption_per_cycle_in_dishwasher:.2f} gallons"

        else:
            client_requested_data = f"Smart Dishwasher did not produce any water consumption data yet"

    elif query_index == 2:
        client_requested_data = f"Functionality not implemented yet"

    else:
        client_requested_data = f"Functionality not implemented yet"

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

    if message_from_client in VALID_QUERIES:
        query_index = VALID_QUERIES.index(message_from_client)
        server_message = get_client_requested_data(query_index)
    else:
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
