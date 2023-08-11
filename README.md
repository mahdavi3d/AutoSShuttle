# AutoSShuttle
This Python code provides a somewhat simplistic and not-very-secure approach (In terms of handling credentials) to easily and effortlessly establish a Secure VPN-like connection over SSH using SSHuttle on Debian/Ubuntu. While it's advisable to utilize SSH keys for enhanced security, let's assume you're looking for a username and password method due to convenience. You might be reluctant to repeatedly copy and paste the credentials within your terminal. This Python script accomplishes that objective.

There are two key files of concern: a configuration file named "AutoSShuttle.conf" and the main code component named "AutoSShuttle.py."



Please edit the configuration file and populate the entries with the necessary data using any text editor you prefer. The required information includes:

    Name*: Choose a name for the remote server (you can use any name you like).
    IP address: Provide the IP address of the remote server for establishing the SSH tunnel.
    SSH port: Specify the SSH port used by the remote server.
    Username: Enter the username for accessing the remote server.
    Password: Provide the password for the username on the remote server.
    Local system password: Enter the password for the local system.

Note*: The name of the remote server can be any text of your choice; there are no restrictions on naming.

If you have only one server or if you have more than two servers to add, you can manage them by adding or removing blocks in the "Server configurations" section of the config file. To do this, you can either delete existing blocks or use the copy-paste method to add new ones. Please be cautious not to alter the overall structure of the config file.

After populating the configuration file with the required information, save the changes. 



Next, follow these steps to place the config file in the specified path:
Use the following command to create the AutoSShuttle folder in the /etc directory: sudo mkdir /etc/AutoSShuttle
Move the AutoSShuttle.conf file to the newly created folder using the following command: sudo mv /path/to/AutoSShuttle.conf /etc/AutoSShuttle/
Remember to replace /path/to/AutoSShuttle.conf with the current path to your AutoSShuttle.conf file.
This will properly organize your configuration file in the designated directory for AutoSShuttle.
The final path sould be like this: /etc/AutoSShuttle/AutoSShuttle.conf



The final step involves compiling the main code and creating an executable. To begin, ensure that you have the required packages installed on your system. Follow these instructions:

For packages requiring sudo apt install:
sudo apt install python3 python3-pip python-is-python3 sshuttle

For packages requiring pip install: 
pip install python3-pexpect

To install pyinstaller: 
pip install pyinstaller

Once you have the necessary packages installed, you can proceed with compiling the main code and creating the executable. Navigate to the directory containing the AutoSShuttle.py file and execute the following command:
pyinstaller --onefile AutoSShuttle.py

This command will create a standalone executable in the dist directory within the same directory as your AutoSShuttle.py file. This executable can be run without needing to invoke Python explicitly.

In the terminal navigate to the path where the executable is located (inside the "dist" folder).
Run the executable by typing the following command:
./AutoSShuttle

This will launch the script. You can then select the server you want to connect to by typing the corresponding number from the list and pressing Enter. If all steps are completed correctly, you should see the message "Connected to server" once the connection is established.


Move the executable to a any convenient spot within your system and run ./AutoSShuttle from that location to establish a connection hassle-free. No more copying, pasting, or password typing required. Happy tunneling!
