# FS.py
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)


@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    # Registering with AS
    dns_request = f'TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(dns_request.encode(), (as_ip, int(as_port)))

    return jsonify(message='Registered successfully'), 201


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number.isdigit():
        return 'Bad Format', 400

    n = int(number)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return jsonify(fibonacci=b), 200


if __name__ == "__main__":
    app.run(port=9090)
