#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:44:52 2018

@author: henrithomas
"""
from bitstring import BitArray
class Packet:
    opcode = BitArray('0x0000')
    fileName = ""
    zeroByte = BitArray('0x00')
    mode = BitArray('0x6e65746173636969') #bitstring of "netascii" after encoding
    block = BitArray('0x0000')
    packetData = bytes()
    errorCode = BitArray('0x0000')
    errorMsg = ""
    
    def padhexa(self,s):
        return '0x' + s[2:].zfill(4)

    #extract strings from request or error packets
    def extractString(self, data,start):
        seeking = True
        i = start
        while seeking == True:
            if data[i] == 0:
                seeking = False
            else:
                i += 1
        name = data[start:i]
        return name.decode()

    def setOpcode(self,val):
        self.opcode = val

    def setFileName(self,val):
        self.fileName = val

    def setZeroByte(self,val):
        self.zeroByte = val

    def setMode(self,val):
        self.mode = val

    def setBlock(self,b):
        self.block = BitArray(self.padhexa(hex(b)))

    def setData(self,val):
        self.packetData = val

    def setErrorCode(self,val):
        self.errorCode = val

    def setErrorMsg(self,val):
        self.errorMsg = val

    def getOpcode(self):
        return self.opcode

    def getFileName(self):
        return self.fileName

    def getZeroByte(self):
        return self.zeroByte

    def getMode(self):
        return self.mode

    def getBlock(self):
        return self.block

    def getData(self):
        return self.packetData

    def getErrorCode(self):
        return self.errorCode

    def getErrorMsg(self):
        return self.errorMsg

    #form a RRQ packet
    def createRRQPacket(self,name):
        self.fileName = name
        file = BitArray(name.encode())
        self.opcode = BitArray('0x0001')
        pkt = self.opcode
        pkt.append(file)
        pkt.append(self.zeroByte)
        pkt.append(self.mode)
        pkt.append(self.zeroByte)
        self.block = BitArray('0x0000')
        self.packetData = bytes()
        self.errorCode = BitArray('0x0000')
        self.errorMsg = ""
        return pkt.tobytes()

    #form a WRQ packet
    def createWRQPacket(self,name):
        self.fileName = name
        file = BitArray(name.encode())
        self.opcode = BitArray('0x0002')
        pkt = self.opcode
        pkt.append(file)
        pkt.append(self.zeroByte)
        pkt.append(self.mode)
        pkt.append(self.zeroByte)
        self.block = BitArray('0x0000')
        self.packetData = bytes()
        self.errorCode = BitArray('0x0000')
        self.errorMsg = ""
        return pkt.tobytes()

    #form a data packet
    def createDataPacket(self,b,dat):
        self.packetData = dat
        data = BitArray(dat)
        self.opcode = BitArray('0x0003')
        pkt = self.opcode
        self.block = self.padhexa(hex(b))
        pkt.append(self.block)
        pkt.append(data)
        self.fileName = ""
        self.errorCode = BitArray('0x0000')
        self.errorMsg = ""
        return pkt.tobytes()

    #form an ACK packet
    def createACKPacket(self,b):
        self.opcode = BitArray('0x0004')
        pkt = self.opcode
        block = BitArray(self.padhexa(hex(b)))
        pkt.append(block)
        self.fileName = ""
        self.packetData = bytes()
        self.errorCode = BitArray('0x0000')
        self.errorMsg = ""
        return pkt.tobytes()

    #form an error packet
    def createErrorPacket(self,errCode):
        self.opcode = BitArray('0x0005')
        if errCode == 0:
            self.errorMsg = 'file not found'
        elif errCode == 1:
            self.errorMsg = 'unknown TID'
        elif errCode == 2:
            self.errorMsg = 'file already exists'
        self.errorCode = BitArray(self.padhexa(hex(errCode)))
        pkt = self.opcode
        pkt.append(self.errorCode)
        pkt.append(BitArray(self.errorMsg.encode()))
        pkt.append(self.zeroByte)
        self.fileName = ""
        self.block = BitArray('0x0000')
        self.packetData = bytes()
        return pkt.tobytes()

    #deconstruct a packet
    def deconstructPacket(self, data):
        self.opcode = BitArray(data[0:2])
        op = self.opcode.int
        #read request
        if op == 1:
            self.fileName = self.extractString(data,2)
            self.block = BitArray('0x0000')
            self.packetData = bytes()
            self.errorCode = BitArray('0x0000')
            self.errorMsg = ""
        #write request
        elif op == 2:
            self.fileName = self.extractString(data,2)
            self.block = BitArray('0x0000')
            self.packetData = bytes()
            self.errorCode = BitArray('0x0000')
            self.errorMsg = ""
        #data packet
        elif op == 3:
            self.block = BitArray(data[2:4])
            self.packetData = data[4:len(data)]
            self.fileName = ""
            self.errorCode = BitArray('0x0000')
            self.errorMsg = ""
        #ACK packet
        elif op == 4:
            self.block = BitArray(data[2:4])
            self.fileName = ""
            self.packetData = bytes()
            self.errorCode = BitArray('0x0000')
            self.errorMsg = ""
        #error packet
        elif op == 5:
            self.errorCode = BitArray(data[2:4])
            self.errorMsg = self.extractString(data,4)
            self.fileName = ""
            self.block = BitArray('0x0000')
            self.packetData = bytes()
