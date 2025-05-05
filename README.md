## Before You Begin
Make sure that you have python installed on both machines. If not, install them from https://www.python.org/.

## Database
Create an account on Neon if you haven't already (https://console.neon.tech). Once done, create a database, grab
the connection string, and paste the connection string in a .env file in the local folder where echo_client.py
and echo_server.py are stored. Afterwards, populate the database with data by turning on all the switches to
generate data on Dataniz (follow the instructions listed on Dataniz).

## Run Server
Type in "cmd" in the window taskbar (assuming you are working on a Windows machine) and open the "Command Prompt".
Use the "cd" command to navigate to the directory storing echo_server.py. Type:
```python ./echo_server.py (insert IP address here) (insert port number here)``` and hit enter. If the .env file
specified earlier exists in the same folder and has the correct database connection string, the server should
connect.

## Client
Type in "cmd" in the window taskbar (assuming you are working on a Windows machine) and open the "Command Prompt".
Use the "cd" command to navigate to the directory storing echo_client.py. Next, type "ipconfig"
and look for the IP address listed under IPv4. Once obtained, in that same Command Prompt type: 
```python ./echo_client.py (insert IP address here) (insert port number here)``` and hit enter. The client should
then start running. If the server is already up and running it should connect promptly. Once connected, type in 
numbers 1-3 to query a response from the server.
