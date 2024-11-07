import os
import subprocess

from config import PUBLIC_KEY

class WireGuard:
    def __init__(self, config_dir='/etc/wireguard', server_config='wg0.conf'):
        self.config_dir = config_dir
        self.server_config = server_config

    def create_user_config(self, user):
        private_key, public_key = self.generate_keys()
        address = self.generate_address(user)
        dns = '1.1.1.1,1.0.0.1'
        
        server_public_key, server_ip = self.get_server_details()
        
        config_content = f"""
[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {server_public_key}
AllowedIPs = 0.0.0.0/0,::/0
Endpoint = {server_ip}:51820
"""
        config_path = os.path.join(self.config_dir, f'{user.id}.conf')
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)
        
        self.add_peer_to_server_config(public_key, address)
        return config_path, public_key

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
        return f"{base_ip}{user_id // 256}.{user_id % 256}/32"

    def add_peer_to_server_config(self, public_key, address):
        server_config_path = os.path.join(self.config_dir, self.server_config)
        peer_config = f"""
[Peer]
PublicKey = {public_key}
AllowedIPs = {address}
"""
        with open(server_config_path, 'a') as server_config_file:
            server_config_file.write(peer_config)
        subprocess.run(
            ['wg', 'set', self.server_config.split('.')[0], 'peer', public_key, 'allowed-ips', address],
        )
        
    def generate_server_config(self):
        private_key, public_key = self.generate_keys()
        with open('.env', 'r+') as env_file:
            lines = env_file.readlines()
            for line in lines:
                if line.startswith('PRIVATE_KEY='):
                    lines[lines.index(line)] = f'PRIVATE_KEY={private_key}\n'
                elif line.startswith('PUBLIC_KEY='):
                    lines[lines.index(line)] = f'PUBLIC_KEY={public_key}\n'

        config_content = f"""
[Interface]
PrivateKey = {private_key}
Address = 10.0.0.1/16
ListenPort = 51820
PostUp = iptables -I INPUT -p udp --dport 51820 -j ACCEPT
PostUp = iptables -I FORWARD -i ens3 -o wg0 -j ACCEPT
PostUp = iptables -I FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = ip6tables -I FORWARD -i wg0 -j ACCEPT
PostUp = ip6tables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -D INPUT -p udp --dport 51820 -j ACCEPT
PostDown = iptables -D FORWARD -i ens3 -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = ip6tables -D FORWARD -i wg0 -j ACCEPT
PostDown = ip6tables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
"""
        config_path = os.path.join(self.config_dir, self.server_config)
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)
        return config_path

    def get_server_details(self):
        server_config_path = os.path.join(self.config_dir, self.server_config)
        with open(server_config_path, 'r') as server_config_file:
            lines = server_config_file.readlines()
            private_key = None
            for line in lines:
                if line.startswith('PrivateKey'):
                    private_key = line.split('=')[1].strip()
                    break
            if private_key:
                public_key = PUBLIC_KEY
                return public_key, '138.124.10.20'
            else:
                raise ValueError("Server private key not found in the server config.")
            
    def remove_peer_from_server_config(self, public_key):
        server_config_path = os.path.join(self.config_dir, self.server_config)
        with open(server_config_path, 'r') as server_config_file:
            lines = server_config_file.readlines()
        with open(server_config_path, 'w') as server_config_file:
            for line in lines:
                if line.startswith('[Peer]') and f'PublicKey = {public_key}' in lines:
                    continue
                server_config_file.write(line)
        subprocess.run(['wg', 'syncconf', self.server_config.split('.')[0], server_config_path], check=True)
        subprocess.run(['wg-quick', 'down', self.server_config.split('.')[0]], check=True)
        subprocess.run(['wg-quick', 'up', self.server_config.split('.')[0]], check=True)