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
    recvsockets = []
    sendsockets = []
    def start(self):
        sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sk.settimeout(5)
        localIp = input('input your IP->')
        localPort = input('input your port->')
        self.local = (localIp,int(localPort))
        sk.bind(self.local)
        mode = int(input('mode:1.server 2.client->'))
        if(mode == 2):
            destIp = input('input oppsite IP->')
            destPort = input('input oppsite port->')
            self.dest = (destIp,int(destPort))
            print('try to connect...')
            try:
                sk.connect(self.dest)
                print('connect success!')
            except:
                print('connect Failed ...')
                return 
        elif(mode == 1):
            sk.listen(1)
            print('waiting for connection...')
            connection,client_address = sk.accept()
            connection.setblocking(0)
            connection.settimeout(5)
            
    def send(self,Text):
        pass
    class tcpLayer(method):
        def controlCenter(self):
            pass
        def recvFrame(self):
            pass
        def sendFrams(self):
            pass
        def checkXor(self,oneFrame):
            xorCheck = method.addXorCheck(self,oneFrame)
            recvXorCheck = oneFrame.pop(-1)
            return (xorCheck == recvXorCheck)
    class dataLayer():
        def wrapFrame(self):
            pass
        def parseFrame(self):
            pass

A = method()
checkUnit = ['11110000','10101010','11111111','00000000','01011010','11001100','00110011','10011001']
print(A.oddCheck(checkUnit))