from socket import *
import socket as s
from bitstring import BitArray
from Packet import Packet
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description = "TFTP Server - Henri Thomas")
parser.add_argument('-p',"--port",action="store",type=int,help="Server's port number")
args = parser.parse_args()

serverPort = args.port
reading = False
error = False
receiving = True
received = bytes()
toSend = bytes()
serverPacketManager = Packet()
host = s.gethostname()
b = 0
blockSize = 512
block = 1
#establish a connection and listen
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host,serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
received = connectionSocket.recv(2048)
serverPacketManager.deconstructPacket(received)

#check WRQ or RRQ
if serverPacketManager.getOpcode().int == 2:
    fileTest = Path(serverPacketManager.getFileName()) #file error check
    if fileTest.is_file():
        fName = serverPacketManager.getFileName() + "SERVER"
        f = open(fName, 'wb')
        toSend = serverPacketManager.createACKPacket(0)
        reading = True
        connectionSocket.send(toSend)
    else:
        toSend = serverPacketManager.createErrorPacket(0)
        error = True
        connectionSocket.send(toSend)
else:
    fileTest = Path(serverPacketManager.getFileName()) #file error check
    if fileTest.is_file():
        fName = serverPacketManager.getFileName()
        f = open(fName, 'rb')
        receiving = False
    else:
        toSend = serverPacketManager.createErrorPacket(0)
        error = True
        connectionSocket.send(toSend)

if receiving:
    while reading:
        #receive packets until data block is < 512 bytes
        received = connectionSocket.recv(2048)
        serverPacketManager.deconstructPacket(received)
        if len(serverPacketManager.getData()) < 512:
            reading = False
        b = serverPacketManager.getBlock().int
        f.write(serverPacketManager.getData())
        toSend = serverPacketManager.createACKPacket(b)
        connectionSocket.send(toSend)
else:#sending
    while blockSize == 512 and block <= 65535:
        #send data packets until data block is < 512 bytes or max block count reached
        d = f.read(512)
        blockSize = len(d)
        toSend = serverPacketManager.createDataPacket(block,d)
        connectionSocket.send(toSend)
        received = connectionSocket.recv(2048)
        serverPacketManager.deconstructPacket(received)
        block += 1


connectionSocket.close()
if error == False:
    f.close()
print('The server is closed')
