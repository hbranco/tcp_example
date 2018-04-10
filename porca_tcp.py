#!/usr/bin/python
# -*- coding: utf-8 -*-


import _thread
import socket
import sys
from crc16branco import calcByte

class parsing():
    def startParsing(self, con, cliente):
        print("Leitão conectado", cliente)
        while True:
            data = con.recv(1024)
            if not data:
                break
            if type(data) == bytes:
                data = data.decode("utf-8")
                # data = data.split()
                print("Dados Convertidor para UTF-8: ", data)

            #print("Dados que chegaram: ",data)
            try:
                dataCRC = data[-5::]
                #print("dados do crc: ", dataCRC)
                # dataCRCInt = int(dataCRC, 16)
                # print(dataCRC)
                # pega a string sem o crc
                dataNoCRC = data[:-5]
                dataNoCRC = dataNoCRC.rstrip(" ")
                print(dataNoCRC)

                crc = 0xFFFF  # inicializa o crc
            except ValueError as e:
                print(e)
                print("Finalizando conexao do cliente", cliente)
                con.sendall("CRC Invalido")
                con.close()
                _thread.exit()
                sys.exit(1)

            for ch in dataNoCRC:
                crc = calcByte(ch, crc)
            # falha do crc sai fora do parser
            if int(crc) != int(dataCRC):
                print("falaha do crc")
                print("crc calculado: " + str(crc))
                print("CRC recebido: "+ dataCRC)

                nack = '\x15'
                con.sendall(nack.upper().encode('UTF-8'))
             #   print("CRC falhou")
                break
            else:
              #  print("crc deu certo")
                ack = '\x06'
                con.sendall(ack.upper().encode('UTF-8'))
                # dadosParser = map(None, dataNoCRC.split())
                dadosParser = dataNoCRC.split()
               # print("dados do parser: ", dadosParser)
                x = -1
                print(dadosParser)


        con.close()
        print ("Finalizando conexao do cliente" , cliente)
        _thread.exit()
        sys.exit(1)



'''
inicialização do parser
'''
# HOST = '172.31.32.32'
HOST = '127.0.0.1'
PORT = 9010

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(0)
parsing = parsing()
while True:
    try:
        print("Porca a espera dos leitões.... ")
        con, cliente = tcp.accept()
        _thread.start_new_thread(parsing.startParsing, tuple([con, cliente]))
    except KeyboardInterrupt as e:
        print("Keyboard interrupt")
        tcp.close()
        _thread.exit_thread()
        print(e.args)

# 865328024678491
