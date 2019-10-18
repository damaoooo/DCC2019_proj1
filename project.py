from os import system
import time
from binascii import unhexlify
import socket
import select
class method():
    def oddCheck(self,checkUnit):
        rowRes = [0]*8
        colunmRes = [0]*8
        for singleByteIndex in range(len(checkUnit)):
            #row:行  colunm:列
            listBytes = list(checkUnit[singleByteIndex])
            for singleBitIndex in range(len(listBytes)):
                num = int(listBytes[singleBitIndex])
                rowRes[singleByteIndex]^=num
                colunmRes[singleBitIndex]^=num
        return [''.join([str(x) for x in rowRes]),''.join([str(y) for y in colunmRes])]     
    def bytes2Bin(self,Bytes):
        binres = ''
        for i in Bytes:
            binres+=bin(i)[2:].zfill(8)
        return binres
    def bin2Frames(self,binText,Framelength):
        res = []
        leng = len(binText)
        tempFrame = []
        tempFramelen = 0
        while(leng>0):
            if(tempFramelen!=Framelength):
                tempFrame.append(binText[0:8])
                binText = binText[8:]
                tempFramelen+=1
                leng-=8
            else:
                res.append(tempFrame)
                tempFrame=[]
                tempFramelen=0
        if(res==[] or tempFrame!=res[-1]):
            res.append(tempFrame)
        return res
    def frames2Bin(self,frames):
        res = ''
        for oneFrame in frames:
            for i in oneFrame:
                res+=i
        return res
    def bin2Bytes(self,binText):
        res = b''
        length = len(binText)
        while(length>0):
            singleByte = unhexlify(hex(eval('0b'+binText[0:4]))[2:]+hex(eval('0b'+binText[4:8]))[2:])
            res+=singleByte
            binText = binText[8:]
            length-=8
        return res
    def text2Bytes(self,text):
        return text.encode()
    def bytes2Text(self,bytesText):
        return bytesText.decode()
    def addXorCheck(self,Frame):
        sumxor = 0
        for onebyte in Frame:
            sumxor ^=eval('0b'+onebyte)
        return bin(sumxor)[2:].zfill(8)
class Unit(method):
    mode = 0
    local = 0
    dest = 0
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.settimeout(5)
    def start(self):
        mode = int(input('select your mode:1.debug-1 2.debug-2 3.test'))
        if(mode == 3):
            localIp = input('input your IP->')
            localPort = input('input your Port->')
            self.local = (localIp,int(localPort))
            self.sk.bind(self.local)
            destIp = input('input opposite IP->')
            destPort = input('input opposite Port->')
            self.dest = (destIp,int(destPort))
        elif(mode == 1):
            self.local = ('127.0.0.1',11400)
            self.dest = ('127.0.0.1',11100)
            self.sk.bind(self.local)
        elif(mode == 2):
            self.local = ('127.0.0.1',12400)
            self.dest = ('127.0.0.1',12100)
            self.sk.bind(self.local)
    class tcpLayer(method):
        frameIndexHead = 0
        frameIndexEnd = -1
        frameNumber = 0
        def sendControlCenter(self,rawBins):
            Frames = method.bin2Frames(self,rawBins,386)
            self.frameIndexHead,self.frameIndexEnd = 0,len(Frames)
            for i in Frames:
                self.sendFrames(i)
        def getHeaders(self):
            sourceIp,sourcePort = self.local[0],self.local[1]
            destIp,destPort = self.dest[0],self.dest[1]
            Number = self.frameNumber
            res =  []
            temp = ''
            res.append(bin(Number)[2:].zfill(8))
            for i in sourceIp.split('.'):
                res.append(bin(int(i))[2:].zfill(8))
            portbin = bin(sourcePort)[2:].zfill(16)
            res.append(portbin[0:8])
            res.append(portbin[8:])
            for i in destIp.split('.'):
                res.append(bin(int(i))[2:].zfill(8))
            portbin = bin(destPort)[2:].zfill(16)
            res.append(portbin[0:8])
            res.append(portbin[8:])
            return res
        def recvFrame(self):
            pass
        def sendFrames(self,oneFrame):
            Frame = self.getHeaders()+oneFrame+[method.addXorCheck(self,oneFrame)]
            
        def checkXor(self,oneFrame):
            xorCheck = method.addXorCheck(self,oneFrame)
            recvXorCheck = oneFrame.pop(-1)
            return (xorCheck == recvXorCheck)
    class dataLayer():
        def wrapChunk(self):
            pass
        def parseChunk(self):
            pass
    def send(self,Text):
        bytesText = method.text2Bytes(self,Text)
        binText = method.bytes2Bin(self,bytesText)
        self.tcpLayer.sendControlCenter(self,binText)


if(__name__ == '__main__'):
    A = Unit()
    A.start()
    text = 'hello world!'
    A.send(text)