# AS.py
import socket

dns_records = {}
UDP_IP, UDP_PORT = '0.0.0.0', 53533

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        data_str = data.decode()

        # If VALUE is present, it's a registration request.
        if 'VALUE=' in data_str:
            _, name, value, _ = data_str.split('\n')
            dns_records[name.split('=')[1]] = value.split('=')[1]

        # If not, it's a DNS query.
        else:
            _, name, _ = data_str.split('\n')
            response_ip = dns_records.get(name.split('=')[1], '')
            response = f'TYPE=A\nNAME={name.split("=")[1]}\nVALUE={response_ip}\nTTL=10\n'
            sock.sendto(response.encode(), addr)
