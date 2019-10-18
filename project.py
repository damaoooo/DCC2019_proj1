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
    mode,local,dest,tcp,datalink = 0,0,0,0,0
    sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
        self.tcp = self.tcpLayer(self.local,self.dest,self.sk)
    class tcpLayer(method):
        frameLength,frameNumber,local,dest,sendSocket = 0,0,0,0,0
        beginWindow,endWindow = 0,0
        def __init__(self,local,dest,sendsocket,*argc,**kwargs):
            self.local = local
            self.dest = dest
            self.sendSocket = sendsocket
        def getHeaders(self):
            sourceIp,sourcePort = self.local[0],self.local[1]
            destIp,destPort = self.dest[0],self.dest[1]
            Number = self.frameNumber
            res =  []
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
        def wrapFrames(self,oneFrame):
            Frame = self.getHeaders()+oneFrame+[method.addXorCheck(self,oneFrame)]
            return Frame
        def checkXor(self,oneFrame):
            xorCheck = method.addXorCheck(self,oneFrame)
            recvXorCheck = oneFrame.pop(-1)
            return (xorCheck == recvXorCheck)
        def wrapChunk(self,oneFrame):
            chunks = []
            length = len(oneFrame)
            while(length>0):
                chunks.append(oneFrame[0:8])
                oneFrame = oneFrame[8:]
                length-=8
            for oneChunkIndex in range(len(chunks)):
                chunks[oneChunkIndex]+=(method.oddCheck(self,chunks[oneChunkIndex]))
            return chunks
        def sendSingleFrame(self,oneFrame):
            afterFrame = self.wrapFrames(oneFrame)
            afterChunk = self.wrapChunk(afterFrame)
            sendBin = self.frames2Bin(afterChunk)
            sendbytes = self.bin2Bytes(sendBin)
            print(self.frameNumber)
            self.sendSocket.sendto(sendbytes,self.dest)
            
        def parseChunk(self):
            pass
        def sendBytes(self,bytesToSend):
            self.sendSocket.sendto(bytesToSend,self.dest)
        def sendControlCenter(self,rawBins):
            Frames = self.bin2Frames(rawBins,386)
            self.frameLength = len(Frames)
            self.beginWindow = 0
            if(self.frameLength>8):
                self.endWindow = 7
            else:
                self.endWindow = self.frameLength-1
            while(Frames!=[]):
                if(self.tcp.frameNumber<min(8,len(Frames))):
                    self.tcp.sendSingleFrame(Frames[self.tcp.frameNumber])
                    print(Frames[self.tcp.frameNumber])
                    self.tcp.frameNumber+=1
                else:
                    status = self.tcp.sendSocket.recv(1024).decode()
                    self.tcp.frameNumber = 0
                    Frames = Frames[int(status.split(' ')[1]):]
                

                    
    def send(self,Text):
        bytesText = method.text2Bytes(self,Text)
        binText = method.bytes2Bin(self,bytesText)
        self.tcpLayer.sendControlCenter(self,binText)
    def recv(self)
        pass

if(__name__ == '__main__'):
    A = Unit()
    A.start()
    text = '我初学时对类的理解是从类的字面上，可以片面的认为它是一个种类，它是相似特征的抽像，也就是相似的东西，可以把相似特征的事务抽象成一个类。（事务可以是具体的物体或行为）以圆为例，圆是具有圆周率(pi)和半径(r)两个相似特征的属性。根据相似特征抽象出圆类，每个圆的半径可以不同，那么半径可以作为圆的实例属性；而每个圆的圆周率pi是相同的，那么圆周率pi就可以作为类属性，这样就定义出了一个圆类。而我们要知道圆的面积，周长等可以通过类方法计算出来。（看完整篇文章，还是对类不理解，回过头在来看这部分，对照列子多理解。）'
    A.send(text)