import socket
import ipaddress

# Loop to ensure that the user inputs a valid IP address for the Server
while True:
    try:
        server_ip_address = str(ipaddress.IPv4Address(input("\nInput the IP Address of the Server: ")))
    except ipaddress.AddressValueError:
        print("Invalid IP Address inputted.")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * *")
        continue
    print("* * * * * * * * * * * * * * * * * * * * * * * * * *")
    break

# Ensures that the user acting as Client inputs a valid port number to communicate with Server
while True:
    try:
        # User inputs port number
        server_port_num = int(input("Input the Port Number of the Server: "))
        # Ensures that the port number inputted is not invalid
        if server_port_num not in range(1, 65536):
            raise ValueError

        # Creates socket for network communication using IPV4 and TCP
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip_address, server_port_num))
    # Catches any errors associated with the port number
    except ValueError:
        print("Invalid Port Number inputted. Should be between 1-65,535.")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * *")
        continue
    except Exception as e:
        print("Unexpected Error:", e)
        print("* * * * * * * * * * * * * * * * * * * * * * * * * *")
        continue
    print("* * * * * * * * * * * * * * * * * * * * * * * * * *")
    break

# Loop for client to repeatedly send and receive messages between itself and the Server
while True:
    # User inputs a message to send to the server
    message = input("Input a Message to Send to the Server: ")
    # Sends message to Server over communication link
    client.send(bytearray(str(message), encoding="utf-8"))

    # Indicates whether Server-Client communication should cease
    if message == "":
        break

    # Receives message (of max size of 1024 bytes) from server
    server_response = client.recv(1024).decode()

    # Displays server replay
    print('Client Received:', server_response)
    print("* * * * * * * * * * * * * * * * * * * * * * * * * *")

# Closes connection with Server
client.close()
print("Shutting down communications on client side...")
