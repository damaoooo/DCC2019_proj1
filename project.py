from os import system
import time
from binascii import unhexlify



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
    def frames2Bin(self):
        pass
    def bin2Bytes(self):
        pass
    def text2Bytes(self):
        pass
    def bytes2Text(self):
        pass
    def addXorCheck(self):
        pass
class Unit(method):
    mode = 0
    local = 0
    dest = 0
    def start(self):
        pass
    class tcpLayer(method):
        def controlCenter(self):
            pass
        def recvFrame(self):
            pass
        def sendFrams(self):
            pass
        def checkXor(self):
            pass
    class dataLayer():
        def wrapFrame(self):
            pass
        def parseFrame(self):
            pass

A = method()
checkUnit = ['11110000','10101010','11111111','00000000','01011010','11001100','00110011','10011001']
print(A.oddCheck(checkUnit))