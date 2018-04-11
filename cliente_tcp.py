# Echo client program
import socket
from crc16branco import calcByte

HOST = '127.0.0.1'    # The remote host
PORT = 9010              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        dataNoCRC = "Mensagem que vai ser enviada ao servidor"
        crc = 0xFFFF  # inicializa o crc
        for ch in dataNoCRC:
            crc = calcByte(ch, crc)
        print("Calculo do CRC", crc)

        dataNoCRC = dataNoCRC + " " + str(crc)
        print("Send Message: ", dataNoCRC)

        s.sendall(dataNoCRC.encode('UTF-8'))
        data = s.recv(1024)
        print('Received', repr(data))
    except ConnectionRefusedError as e:
        print("Tu esqueceu de ligar o servidor dnv:( ")

