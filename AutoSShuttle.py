import subprocess
import pexpect
import os
import configparser
from cryptography.fernet import Fernet

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
## Make sure that you have cryptography.  Please refer to README for more INFO.

def main():
    if check_internet_connectivity():
        missing_packages = check_packages(required_packages)

        if len(missing_packages) == 0:
            print("Internet is connected.")
            print("All required packages are present.")

            try:
                print("Loading configurations")
                config_file_path = '/tmp/AutoSShuttle_tmp.conf'

                # Code A: Define paths
                config_file_path = "/etc/AutoSShuttle/AutoSShuttle.conf"
                encrypted_config_path = "/etc/AutoSShuttle/Encry.conf"
                encryption_key_path = "/etc/PJZZgTF4aAM7g6GsNytWqMnHONuHb.key"

                # Code A: Define functions
                def read_sudo_password():
                    config = configparser.ConfigParser()
                    config.read(config_file_path)
                    return config.get('System', 'system_password', fallback='')

                def save_encryption_key(key, sudo_password):
                    try:
                        subprocess.run(f'echo "{sudo_password}" | sudo -S bash -c "echo \'{key.decode("latin-1")}\' > {encryption_key_path}"', shell=True, check=True)
                        print("Encryption key saved successfully")
                    except subprocess.CalledProcessError as e:
                        print("Failed to save encryption key:", e)

                def read_encryption_key():
                    with open(encryption_key_path, "rb") as key_file:
                        return key_file.read()

                def encrypt_content(content, encryption_key):
                    fernet = Fernet(encryption_key)
                    return fernet.encrypt(content)

                def decrypt_content(encrypted_content, encryption_key):
                    fernet = Fernet(encryption_key)
                    return fernet.decrypt(encrypted_content)

                # Code A: Rest of main function
                sudo_password = read_sudo_password()

                if os.path.exists(encrypted_config_path):
                    print("The encrypted config file found.")
                else:
                    print("The encrypted config file NOT found. Encrypting started")

                if os.path.exists(encryption_key_path):
                    print("The encryption key found.")
                    encryption_key = read_encryption_key()
                else:
                    print("The encryption key NOT found. Generating the encryption key ...")
                    encryption_key = Fernet.generate_key()
                    save_encryption_key(encryption_key, sudo_password)

                if not os.path.exists(encrypted_config_path) and not os.path.exists(encryption_key_path):
                    print("Something is horribly wrong. Please make a clean build from scratch.")

                if not os.path.exists(encrypted_config_path):
                    with open(config_file_path, "rb") as config_file:
                        config_content = config_file.read()

                    try:
                        fernet = Fernet(encryption_key)
                        encrypted_config = fernet.encrypt(config_content)

                        with open("temp_encry.conf", "wb") as encrypted_file:
                            encrypted_file.write(encrypted_config)

                        try:
                            subprocess.run(f'echo "{sudo_password}" | sudo -S bash -c "mv temp_encry.conf {encrypted_config_path}"', shell=True, check=True)
                            print("The encrypted config file created successfully")
                        except subprocess.CalledProcessError as e:
                            print("Failed to create the encrypted config file:", e)
                    except Exception as e:
                        print("Failed to create the encrypted config file:", e)

                if os.path.exists(encrypted_config_path):
                    with open(encrypted_config_path, "rb") as encrypted_file:
                        encrypted_content = encrypted_file.read()

                    try:
                        fernet = Fernet(encryption_key)
                        decrypted_config = fernet.decrypt(encrypted_content)

                        config = configparser.ConfigParser()
                        config.read_string(decrypted_config.decode())

                        for section in config.sections():
                            for option in config.options(section):
                                if "password" in option.lower():
                                    config.set(section, option, "*****")

                        # Use sudo to write the updated config file
                        with open("temp_AutoSShuttle.conf", "w") as config_file:
                            config.write(config_file)

                        try:
                            subprocess.run(f'echo "{sudo_password}" | sudo -S bash -c "mv temp_AutoSShuttle.conf {config_file_path}"', shell=True, check=True)
                            print("AutoSShuttle.conf updated with masked passwords")
                        except subprocess.CalledProcessError as e:
                            print("Failed to update AutoSShuttle.conf:", e)
                    except Exception as e:
                        print("Failed to update AutoSShuttle.conf:", e)

                if os.path.exists(encrypted_config_path):
                    with open(encrypted_config_path, "rb") as encrypted_file:
                        encrypted_content = encrypted_file.read()

                    try:
                        decrypted_content = decrypt_content(encrypted_content, encryption_key)

                        with open("/tmp/AutoSShuttle_tmp.conf", "wb") as decrypted_file:
                            decrypted_file.write(decrypted_content)

                        print("__________")
                    except Exception as e:
                        print("Failed to decrypt Encry.conf:", e)

                # Code B: Define paths
                config_file_path = "/tmp/AutoSShuttle_tmp.conf"

                # Code B: Define functions
                def load_configurations(file_path):
                    config = configparser.ConfigParser(interpolation=None)
                    config.read(file_path)
                    
                    servers = []
                    system_password = ''
                    
                    for section in config.sections():
                        if section.startswith('Server'):
                            server = config[section]
                            servers.append({
                                'name': server['name'],
                                'ip': server['ip'],
                                'port': server['port'],
                                'username': server['username'],
                                'password': server['password']
                            })
                    
                    if 'System' in config:
                        system_password = config['System']['system_password']
                    
                    return servers, system_password

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

                # Code B: Rest of main function
                servers, system_password = load_configurations(config_file_path)

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
                            try:
                                os.remove(config_file_path)
                                print("__________")
                            except Exception as e:
                                print("Error deleting tmp config file:", str(e))

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

if __name__ == "__main__":
    main()
