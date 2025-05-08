## Before You Begin
Make sure that you have Python installed on both machines. If not, install them from [python.org](https://www.python.org/).
Once Python is installed, type in ```cmd``` in Windows Search (assuming you are working on a Windows machine) and open "Command Prompt". Then run the following command(s) to install various dependencies:
```
pip install pytz
pip install dotenv
pip install psycopg2
```

## Database
Create an account on [Neon](https://console.neon.tech) if you haven't already. Once done, create a database and grab
the connection string. Create a file named ```.env``` containing this connection string in the following format:
```
DATABASE_CONNECTION_STRING=paste_connection_string_here
```
The ```.env``` file must be stored in the same folder as ```echo_server.py```. Afterwards, populate the database with generated data by turning on all the switches in Dataniz (Follow the instructions listed on Dataniz).

## Run Server
Type in ```cmd``` in Windows Search (assuming you are working on a Windows machine) and open "Command Prompt".
Use the ```cd``` command to navigate to the directory storing ```echo_server.py```. Then run the command:
```
python ./echo_server.py <insert server IP address here> <insert port number here>
```
If the ```.env``` file specified earlier exists in the same folder and contains the correct database connection string, the server should
be able to establish a connection with the database.

## Client
Type in ```cmd``` in Windows Search (assuming you are working on a Windows machine) and open "Command Prompt".
Use the ```cd``` command to navigate to the directory storing ```echo_client.py```. Then run the command: 
```
python ./echo_client.py <insert server IP address here> <insert port number here>
```
The client should then start running. If the server is already up and running it should connect properly. Once connected, type in ```1```, ```2```, or ```3``` to request some information from the server.
