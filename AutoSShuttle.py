import subprocess
import pexpect
import os

def check_packages(packages):
    missing_packages = [pkg for pkg in packages if subprocess.call(["dpkg", "-l", pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0]
    return missing_packages

def check_internet_connectivity():
    servers = ["8.8.8.8", "9.9.9.9", "1.1.1.1", "1.0.0.1"]
    
    for server in servers:
        command = ["ping", "-c", "1", "-W", "5", server]
        try:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=5)
            return True
        except subprocess.CalledProcessError:
            continue
        except subprocess.TimeoutExpired:
            continue

    return False

required_packages = ["python3", "python3-pip", "python-is-python3", "sshuttle", "python3-pexpect"]
## Also you need To install pyinstaller. Please refer to README for more INFO.

if check_internet_connectivity():
    missing_packages = check_packages(required_packages)

    if len(missing_packages) == 0:
        print("Internet is connected.")
        print("All required packages are present.")
        
        try:
            print("loading configurations")
            print("/etc/AutoSShuttle/AutoSShuttle.conf")
            CONFIG_FILE_PATH = '/etc/AutoSShuttle/AutoSShuttle.conf'

            def load_configurations(file_path):
                config = {}
                try:
                    with open(file_path, 'r') as config_file:
                        exec(config_file.read(), config)
                    return config.get('servers', []), config.get('system_password', '')
                except FileNotFoundError:
                    print(f"Config file not found at {file_path}")
                    return [], ''
                except Exception as e:
                    print("Error loading configurations:", str(e))
                    return [], ''

            def connect_to_server(server, system_password):
                ssh_command = f"sudo sshuttle --dns -r {server['username']}@{server['ip']}:{server['port']} -x {server['ip']} 0/0"

                child = pexpect.spawn(ssh_command)

                try:
                    index = child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=10)

                    if index == 0:
                        print("Command exited unexpectedly.")
                    elif index == 1:
                        child.sendline(system_password)
                        password_index = child.expect(['password:', pexpect.EOF, pexpect.TIMEOUT])

                        if password_index == 0:
                            child.sendline(server['password'])
                            server_password_index = child.expect(['c : Connected to server.', 'Permission denied', pexpect.EOF, pexpect.TIMEOUT])

                            if server_password_index == 0:
                                print("Connected to server.")
                            elif server_password_index == 1:
                                print("Permission denied. Server password is incorrect.")
                            else:
                                print("Error occurred during server password input.")
                        else:
                            print("Error occurred during system password input.")

                    child.interact()

                except Exception as e:
                    print("An error occurred:", str(e))

            servers, system_password = load_configurations(CONFIG_FILE_PATH)

            if not servers:
                print("No server configurations found.")
            else:
                print("List of available servers:")
                for index, server in enumerate(servers, start=1):
                    print(f"{index}. {server['name']}")

                choice = input("Select a server (enter the number): ")

                try:
                    choice = int(choice)
                    if 1 <= choice <= len(servers):
                        connect_to_server(servers[choice - 1], system_password)
                    else:
                        print("Invalid choice. Please select a valid server number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        except ImportError:
            print("Some packages are missing. Please make sure the required packages are installed.")
    else:
        print("Please make sure these packages are installed:", ", ".join(missing_packages))
else:
    print("No Internet connectivity. Please try again")
