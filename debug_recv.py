from os import system
import time
from binascii import unhexlify
import socket
import select
class method():
    def findDiffrent(self,bytes1,bytes2):
        res = []
        for i in range(len(bytes1)):
            if(bytes1[i]!=bytes2[i]):
                res.append(i)
        return res
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
        if(isinstance(binText,int)):
            print('ERROR!',binText)
            #a = input('1')
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
    def direction(self,text,keystart,keyend):
        start = text.find(keystart)
        end = text.find(keyend)
        if(start!=-1 and end!=-1):
            return text[start+len(keystart):end]
        else:
            return -1
class Unit(method):
    system('cls')
    mode,local,dest,tcp,datalink = 0,0,0,0,0
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.settimeout(30)
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
            self.datalink = self.dest
            self.sk.bind(self.local)
        elif(mode == 2):
            self.local = ('127.0.0.1',12400)
            self.dest = ('127.0.0.1',12100)
            self.datalink = self.dest
            self.sk.bind(self.local)
        self.tcp = self.tcpLayer(self.local,self.dest,self.sk)
    class tcpLayer(method):
        frameLength,frameNumber,local,dest,sendSocket = 0,0,0,0,0
        def __init__(self,local,dest,sendsocket,*argc,**kwargs):
            self.local = local
            self.dest = dest
            self.sendSocket = sendsocket
        def getHeaders(self,sourceIp,sourcePort,destIp,destPort,frameNumber):
            res =  []
            res.append(bin(frameNumber)[2:].zfill(8))
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

        def checkXor(self,oneFrame):
            xorCheck = method.addXorCheck(self,oneFrame[:-1])
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
            
        def parseChunk(self,oneFrame):
            chunks = []
            while(oneFrame!=[]):
                oneChunk = oneFrame[0:10]
                chunks.append(oneChunk)
                oneFrame = oneFrame[10:]
            for chunkIndex in range(len(chunks)):
                oddCheckRecv = chunks[chunkIndex][-2:]
                data = chunks[chunkIndex][:-2]
                selfCheck = self.oddCheck(data)
                if(selfCheck == oddCheckRecv):
                    chunks[chunkIndex]=data
                    continue
                else:
                    diff = [self.findDiffrent(oddCheckRecv[0],selfCheck[0]),self.findDiffrent(oddCheckRecv[1],selfCheck[1])]
                    x,y = diff[0],diff[1]
                    if(len(x)+len(y)==1):
                        chunks[chunkIndex] = data
                        continue
                    elif(len(x)==len(y)):
                        for i in range(len(x)):
                            try:
                                errorData = list(data[x[i]])
                            except:
                                print('found ERR!->',data)
                            errorData[y[i]] = str(int(errorData[y[i]])^1)
                            patchData = ''.join(errorData)
                            data[x[i]]=patchData
                chunks[chunkIndex] = data
            res = []
            for i in chunks:
                res +=i
            return res
                        
        def sendControlCenter(self,oneFrame):
            sendBin = self.frames2Bin(oneFrame)
            sendBytes = b'\xee\xff'+self.bin2Bytes(sendBin)+b'\xff\xee'
            self.tcp.sendSocket.sendto(sendBytes,self.datalink)

        def recvControlCenter(self,rawBin):
            sourceIp,sourcePort,destIp,destPort = 0,0,0,0
            frameNumber,xorCheckRecv = 0,0
            bytesText = b''
            Frames = self.bin2Frames(rawBin,400)
            status = []
            Info = []
            for oneFrames in Frames:
                afterParse = self.tcp.parseChunk(oneFrames)
                if(afterParse==[]):
                    print('ERROR IN PARSE!')
                    return b'',['ERR.'+str(frameNumber)],Info
                frameNumber = eval('0b'+afterParse[0])
                afterParse.pop(0)
                sourceIp,sourcePort = afterParse[0:4],afterParse[4:6]
                sourceIp = '.'.join([str(eval('0b'+x)) for x in sourceIp])
                sourcePort = eval('0b'+sourcePort[0]+sourcePort[1])
                afterParse = afterParse[6:]
                destIp,destPort = afterParse[0:4],afterParse[4:6]
                destIp = '.'.join([str(eval('0b'+x)) for x in destIp])
                destPort = eval('0b'+destPort[0]+destPort[1])
                afterParse = afterParse[6:]
                Info = [(sourceIp,sourcePort),(destIp,destPort),frameNumber]
                isBad = self.tcp.checkXor(afterParse)
                #print(isBad,frameNumber)
                if(isBad==False):
                    status.append('ERR.'+str(frameNumber))
                    return bytesText,status
                binText = self.frames2Bin(afterParse)
                bytesText += self.bin2Bytes(binText)
                status.append('ACK.'+str(frameNumber))
            return bytesText,status,Info
    def dataWrap(self,frame,frameNumber):
            headers = self.tcp.getHeaders(self.local[0],self.local[1],self.dest[0],self.dest[1],frameNumber)
            xorRes = [self.addXorCheck(frame)]
            wrappedFrames = headers+frame+xorRes
            wrappedFrames = self.tcp.wrapChunk(wrappedFrames)
            return wrappedFrames
    def send(self,Text):
        size = 16
        frameNumber = 0
        bytesText = method.text2Bytes(self,Text)
        binText = method.bytes2Bin(self,bytesText)
        Frames = self.bin2Frames(binText,306)#40 Unit,400-40*2-14=
        #initial send
        startPtr,currentPtr = 0,0
        endPtr = min(size,len(Frames))
        windows = [0]*size
        for i in range(endPtr):
            windows[i] = Frames[i]
            self.tcpLayer.sendControlCenter(self,self.dataWrap(windows[i],i))
        while(1):
            if(startPtr==endPtr):
                break
            respondRaw = self.bytes2Bin(self.tcp.sendSocket.recv(1024))
            respondbin = self.direction(respondRaw,bin(0xeeff)[2:],bin(0xffee)[2:])
            if(respondbin==-1):
                print('ack lost!')
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
                continue
            try:
                respondBytes,status,Info = self.tcpLayer.recvControlCenter(self,respondbin)
                respond = respondBytes.decode()
            except:
                print('respond parse ERR!',respondbin)
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
                continue
            print(respond)
            if(sum([ord(x) for x in list(respond.split('.')[0])])-sum([ord(x) for x in list('ACK')])<=8):
                #print(respond.split('.'))
                try:
                    carryNumber = int(respond.split('.')[1])-startPtr%size+1
                except:
                    print('respond number ERR!',respond)
                    for i in range(lastendPtr,endPtr):
                        self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                        windows[i%size]=Frames[i]
                    continue
                if(carryNumber)<0:
                    carryNumber+=size
                lastendPtr = endPtr
                endPtr = min(endPtr+carryNumber,len(Frames))
                startPtr +=carryNumber
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
            elif(respond.split('.')[0]=='ERR'):
                try:
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(windows[int(respond.split('.')[1])+1],int(respond.split('.')[1])%size))
                except:
                    print('no ERR number!')
                    continue
        finBytes = b'\xad\xff\xda'
        finAfterChunk = self.dataWrap(self.bin2Frames(self.bytes2Bin(finBytes),400)[0],frameNumber)
        self.tcpLayer.sendControlCenter(self,finAfterChunk)
        print('send is over...')
    def recv(self):
        recvText = b''
        size = 16
        frameNumber = 0
        while(1):
            rawBytes = self.sk.recv(40000)
            rawBins = self.bytes2Bin(rawBytes)
            afterDirect = self.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
            if(afterDirect==-1 or afterDirect == ''):
                statusInfo = (b'ERR.'+str(frameNumber).encode())
                waitForChunk = self.bin2Frames(self.bytes2Bin(statusInfo),400)
                afterChunk = self.dataWrap(waitForChunk[0],frameNumber)
                self.tcpLayer.sendControlCenter(self,afterChunk)
                continue
            onebytesText,status,frameInfo = self.tcpLayer.recvControlCenter(self,afterDirect)
            #print(frameInfo)
            if(onebytesText == b'\xad\xff\xda'):
                break
            frameNumber=int(status[0].split('.')[1])
            recvText+=onebytesText
            statusInfo = str(status[0]).encode()
            waitForChunk = self.bin2Frames(self.bytes2Bin(statusInfo),306)
            afterChunk = self.dataWrap(waitForChunk[0],frameNumber)
            self.tcpLayer.sendControlCenter(self,afterChunk)
        return recvText.decode()
if(__name__ == '__main__'):
    A = Unit()
    A.start()
    text = 'Thomas Jefferson and James Madison met in 1776. Could it have been any other year? They worked together starting then to further American Revolution and later to shape the new scheme of government. From the work sprang a friendship perhaps incomparable in intimacy1 and the trustfulness of collaboration2 and induration. It lasted 50 years. It included pleasure and utility but over and above them, there were shared purpose, a common end and an enduring goodness on both sides. Four and a half months before he died, when he was ailing3, debt-ridden, and worried about his impoverished4 family, Jefferson wrote to his longtime friend. His words and Madison  s reply remind us that friends are friends until death. They also remind us that sometimes a friendship has a bearing on things larger than the friendship itself, for has there ever been a friendship of greater public consequence than this one? The friendship which has subsisted5 between us now half a century, the harmony of our po1itical principles and pursuits have been sources of constant happiness to me through that long period. If ever the earth has beheld6 a system of administration conducted with a single and steadfast7 eye to the general interest and happiness of those committed to it, one which, protected by truth, can never known reproach, it is that to which our lives have been devoted8. To myself you have been a pillar of support throughout life. Take care of me when dead and be assured that I should leave with you my last affections. A week later Madison replied- You cannot look back to the long period of our private friendship and political harmony with more affecting recollections than I do. If they are a source of pleasure to you, what aren  t they not to be to me? We cannot be deprived of the happy consciousness of the pure devotion to the public good with Which we discharge the trust committed to us and I indulge a confidence that sufficient evidence will find in its way to another generation to ensure, after we are gone, whatever of justice may be withheld9 whilst we are here.  '*10
    print(A.recv())
