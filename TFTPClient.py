from socket import *
import socket as s
from Packet import Packet
from bitstring import BitArray
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description = "TFTP Server - Henri Thomas")
parser.add_argument('-p',"--port",action="store",type=int,help="Server's port number")
parser.add_argument('-f',"--file",action="store",help="Client's requested file to read/write to/from the server")
parser.add_argument('-m',"--mode",choices={'r','w'},help="Client's mode to either read or write to/from the server")
parser.add_argument('-i',"--ip",action="store",help="Client's IP address")
args = parser.parse_args()

serverPort = args.port
fName = args.file
if args.mode == 'r':
    writing = False
else:
    writing = True
host = args.ip

approved = False
error = False
blockSize = 512
block = 1
received = bytes()
toSend = bytes()
clientPacketManager = Packet()
#connect to server
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,serverPort))

if writing:
    f = open(fName, 'rb')
    toSend = clientPacketManager.createWRQPacket(fName)
    clientSocket.send(toSend)
    print('Client - write requested')
    received = clientSocket.recv(2048)
    clientPacketManager.deconstructPacket(received)

    if clientPacketManager.getOpcode().int != 5:
        if clientPacketManager.getOpcode().int == 4 and clientPacketManager.getBlock().int == 0:
            print('Client - able to send')
            approved = True
    else:
        print('ERROR: ',clientPacketManager.getErrorMsg(),'   error code:',clientPacketManager.getErrorCode().int)
        error = True
    #wait for writing confimation from server
    if approved:
        while blockSize == 512 and block <= 65535:
            #send data packets until data block is < 512 bytes or max block count reached
            d = f.read(512)
            blockSize = len(d)
            toSend = clientPacketManager.createDataPacket(block,d)
            clientSocket.send(toSend)
            received = clientSocket.recv(2048)
            clientPacketManager.deconstructPacket(received)
            block += 1
else:#reading
    fileTest = Path(fName)
    if fileTest.is_file():
        f = open(fName + 'CLIENT', 'wb')
    toSend = clientPacketManager.createRRQPacket(fName)
    clientSocket.send(toSend)
    print('Client - read requested')
    reading = True
    while reading:
        #receive packets until data blocks are < 512 bytes
        received = clientSocket.recv(2048)
        clientPacketManager.deconstructPacket(received)
        if clientPacketManager.getOpcode().int != 5:
            if len(clientPacketManager.getData()) < 512:
                reading = False
            b = clientPacketManager.getBlock().int
            f.write(clientPacketManager.getData())
            toSend = clientPacketManager.createACKPacket(b)
            clientSocket.send(toSend)
        else:
            print('ERROR: ',clientPacketManager.getErrorMsg(),'   error code:',clientPacketManager.getErrorCode().int)
            reading = False
            error = True
if error == False:
    f.close()
clientSocket.close()
print('Client complete')
print('The client is closed')
