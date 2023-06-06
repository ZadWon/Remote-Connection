# **BlackDoor**

BlackDoor is a Python script designed as a backdoor utility that utilizes the **`pypsexec`** and **`smbclient`** libraries to perform operations on remote Windows systems. It uploads an executable to a remote SMB share, schedules a task to run the uploaded file with SYSTEM privileges, and opens a listener for the outbound connection.

## **Dependencies**

This script depends on several Python libraries including:

- pypsexec
- argparse
- smbclient
- subprocess
- datetime
- socket
- threading
- random

You can install these using pip:

```
pip install pypsexec argparse smbclient subprocess datetime socket threading random
```

## **Usage**

You can use the script as follows:

```
python OrangeExec.py -u <username> -p <password> -ip <IP address> [-port <SMB port>] [-smbpath <SMB share path>] [-exe <executable filename>]
```

Where:

- **`<username>`** is the admin username for the remote machine.
- **`<password>`** is the admin password for the remote machine.
- **`<IP address>`** is the IP address of the remote machine.
- **`<SMB port>`** (optional) is the port for SMB, default is 445.
- **`<SMB share path>`** (optional) is the path for the SMB share, default is 'C$'.
- **`<executable filename>`** (optional) is the name of the executable file to be uploaded and executed, default is 'BlackDoor.exe'.

The script will attempt to connect to the specified remote machine using the provided credentials. If successful, it will upload the specified executable to the provided SMB share path, schedule it to run as a task on the remote machine with SYSTEM privileges, and open a netcat listener for the outbound connection from the remote machine.

After this, you can input commands in the console which will be executed on the remote machine. Type 'exit' to end the script.

## **Disclaimer**

Please note that this tool is designed for educational purposes and should only be used on systems you have permission to access.
