from operator import add
import os
import subprocess

class WireGuard:
    def __init__(self, config_dir='/etc/wireguard'):
        self.config_dir = config_dir

    def create_user_config(self, user):
        private_key, public_key = self.generate_keys()
        address = self.generate_address(user.id)
        dns = '1.1.1.1,1.0.0.1'
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
        config_path = os.path.join(self.config_dir, f'{user.id}.conf')
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)
        return config_path

    def connect_user(self, user):
        config_path = os.path.join(self.config_dir, f'{user.id}.conf')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for user {user.id} does not exist.")
        subprocess.run(['wg-quick', 'up', config_path], check=True)

    def disconnect_user(self, user):
        config_path = os.path.join(self.config_dir, f'{user.id}.conf')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for user {user.id} does not exist.")
        subprocess.run(['wg-quick', 'down', config_path], check=True)

    def delete_user_config(self, user):
        config_path = os.path.join(self.config_dir, f'{user.id}.conf')
        if os.path.exists(config_path):
            os.remove(config_path)
        else:
            raise FileNotFoundError(f"Config file for user {user.id} does not exist.")
        
    def install_wireguard(self):
        try:
            subprocess.run(['wg', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("WireGuard is already installed.")
        except Exception as e:
            print("WireGuard is not installed. Installing now...")
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'wireguard'], check=True)
            print("WireGuard installation completed.")
            
    def generate_keys(self):
        private_key = subprocess.run(['wg', 'genkey'], check=True, stdout=subprocess.PIPE).stdout.decode().strip()
        public_key = subprocess.run(['wg', 'pubkey'], input=private_key.encode(), check=True, stdout=subprocess.PIPE).stdout.decode().strip()
        return private_key, public_key
    
    def generate_address(self, user):
        base_ip = "10.0."
        user_id = user.id % 65534 + 1
        return f"{base_ip}{user_id // 256}.{user_id % 256}/16"