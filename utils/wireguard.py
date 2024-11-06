import os
import subprocess

class WireGuard:
    def __init__(self, config_dir='/etc/wireguard'):
        self.config_dir = config_dir

    def create_user_config(self, username, private_key, public_key, address, dns):
        config_content = f"""
[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = :51820
PersistentKeepalive = 25
"""
        config_path = os.path.join(self.config_dir, f'{username}.conf')
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)
        return config_path

    def connect_user(self, username):
        config_path = os.path.join(self.config_dir, f'{username}.conf')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for user {username} does not exist.")
        subprocess.run(['wg-quick', 'up', config_path], check=True)

    def disconnect_user(self, username):
        config_path = os.path.join(self.config_dir, f'{username}.conf')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for user {username} does not exist.")
        subprocess.run(['wg-quick', 'down', config_path], check=True)

    def delete_user_config(self, username):
        config_path = os.path.join(self.config_dir, f'{username}.conf')
        if os.path.exists(config_path):
            os.remove(config_path)
        else:
            raise FileNotFoundError(f"Config file for user {username} does not exist.")
        
    def install_wireguard(self):
        try:
            subprocess.run(['wg', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("WireGuard is already installed.")
        except subprocess.CalledProcessError:
            print("WireGuard is not installed. Installing now...")
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'wireguard'], check=True)
            print("WireGuard installation completed.")