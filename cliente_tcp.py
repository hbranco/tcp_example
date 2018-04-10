# Echo client program
import socket
from crc16branco import calcByte

HOST = '127.0.0.1'    # The remote host
PORT = 9010              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    dataNoCRC = "Mensagem enviada ao servidor"
    crc = 0xFFFF  # inicializa o crc
    for ch in dataNoCRC:
        crc = calcByte(ch, crc)
    print(crc)

    dataNoCRC = dataNoCRC +" "+ str(crc)

    s.sendall(dataNoCRC.encode('UTF-8'))
    data = s.recv(1024)
print('Received', repr(data))