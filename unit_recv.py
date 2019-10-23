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
    mode,local,dest,tcp,datalink = 0,0,0,0,0
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    st = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    st.settimeout(30)
    conn,addr = 0,0
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
            self.st.bind(('127.0.0.1',34566))
            self.st.listen(5)
            print('waiting for connection...')
            self.conn,self.addr = self.st.accept()
            print(self.addr,'is connected!')
            self.sk.bind(self.local)
        elif(mode == 2):
            self.local = ('127.0.0.1',12400)
            self.dest = ('127.0.0.1',12100)
            self.st.bind(('127.0.0.1',34567))
            print('trying to connect...')
            self.st.connect(('127.0.0.1',34566))
            self.sk.bind(self.local)
        self.tcp = self.tcpLayer(self.local,self.dest,self.sk,self.st,self.conn)
    class tcpLayer(method):
        frameLength,frameNumber,local,dest,sendSocket,statusSocket,conn = 0,0,0,0,0,0,0
        def __init__(self,local,dest,sendsocket,statussocket,conn,*argc,**kwargs):
            self.local = local
            self.dest = dest
            self.sendSocket = sendsocket
            self.statusSocket = statussocket
            self.conn = conn
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
                            data[x[i]][y[i]]^=1
                chunks[chunkIndex] = data
            res = []
            for i in chunks:
                res +=i
            return res
                        
        def sendControlCenter(self,oneFrame):
            sendBin = self.frames2Bin(oneFrame)
            sendBytes = b'\xee\xff'+self.bin2Bytes(sendBin)+b'\xff\xee'
            self.tcp.sendSocket.sendto(sendBytes,self.dest)

        def recvControlCenter(self,rawBin):
            sourceIp,sourcePort,destIp,destPort = 0,0,0,0
            frameNumber,xorCheckRecv = 0,0
            bytesText = b''
            Frames = self.bin2Frames(rawBin,400)
            status = []
            for oneFrames in Frames:
                afterParse = self.tcp.parseChunk(oneFrames)
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
                isBad = self.tcp.checkXor(afterParse)
                #print(isBad,frameNumber)
                if(isBad==False):
                    status.append('ERR.'+str(frameNumber))
                    return bytesText,status
                binText = self.frames2Bin(afterParse)
                bytesText += self.bin2Bytes(binText)
                status.append('ACK.'+str(frameNumber))
            return bytesText,status


    def send(self,Text):
        frameNumber = 0
        bytesText = method.text2Bytes(self,Text)
        binText = method.bytes2Bin(self,bytesText)
        Frames = self.bin2Frames(binText,306)#40 Unit,400-40*2-14=
        dataToSend = []
        while(Frames!=[]):
            if(frameNumber<min(8,len(Frames))):
                headers = self.tcp.getHeaders(self.local[0],self.local[1],self.dest[0],self.dest[1],frameNumber)
                frame = Frames[frameNumber]
                xorRes = [self.addXorCheck(frame)]
                wrappedFrames = headers+frame+xorRes
                wrappedFrames = self.tcp.wrapChunk(wrappedFrames)
                dataToSend+=wrappedFrames
                frameNumber+=1
            else:
                self.tcpLayer.sendControlCenter(self,dataToSend)
                dataToSend = []
                status = self.tcp.conn.recv(40000).decode()
                status = status.split('|')[-2].split('.')
                if(status[0]=='ERR'):
                    Frames = Frames[int(status[1]):]
                elif(status[0]=='ACK'):
                    Frames = Frames[int(status[1])+1:]
                frameNumber = 0
        self.sk.sendto(b'\xee\xff\xad\xff\xda\xff\xee',self.dest)
        print('send is over...')
        self.st.close()
    def recv(self):
        rawBytes = b''
        bytesText = b''
        self.sk.settimeout(1000)
        firstRecv = self.sk.recv(50000)
        while(1):
            rawBytes = b''
            if(firstRecv!=b''):
                rawBytes+=firstRecv
                firstRecv = b''
            else:
                self.sk.settimeout(2)
                try:
                    rawBytes += self.sk.recv(50000)
                except:
                    print('')
            rawBins = self.bytes2Bin(rawBytes)
            afterDirect = self.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
            if(self.bin2Bytes(afterDirect)==b'\xad\xff\xda'):
                break
            onebytesText,status = self.tcpLayer.recvControlCenter(self,afterDirect)
            self.st.send(('|'+'|'.join(status)+'|').encode())
            bytesText+=onebytesText
            #print(bytesText.decode())
        return bytesText.decode()
        self.st.close()

if(__name__ == '__main__'):
    A = Unit()
    A.start()
    # #text = 'Thomas Jefferson and James Madison met in 1776. Could it have been any other year? They worked together starting then to further American Revolution and later to shape the new scheme of government. From the work sprang a friendship perhaps incomparable in intimacy1 and the trustfulness of collaboration2 and induration. It lasted 50 years. It included pleasure and utility but over and above them, there were shared purpose, a common end and an enduring goodness on both sides. Four and a half months before he died, when he was ailing3, debt-ridden, and worried about his impoverished4 family, Jefferson wrote to his longtime friend. His words and Madison  s reply remind us that friends are friends until death. They also remind us that sometimes a friendship has a bearing on things larger than the friendship itself, for has there ever been a friendship of greater public consequence than this one? The friendship which has subsisted5 between us now half a century, the harmony of our po1itical principles and pursuits have been sources of constant happiness to me through that long period. If ever the earth has beheld6 a system of administration conducted with a single and steadfast7 eye to the general interest and happiness of those committed to it, one which, protected by truth, can never known reproach, it is that to which our lives have been devoted8. To myself you have been a pillar of support throughout life. Take care of me when dead and be assured that I should leave with you my last affections. A week later Madison replied- You cannot look back to the long period of our private friendship and political harmony with more affecting recollections than I do. If they are a source of pleasure to you, what aren  t they not to be to me? We cannot be deprived of the happy consciousness of the pure devotion to the public good with Which we discharge the trust committed to us and I indulge a confidence that sufficient evidence will find in its way to another generation to ensure, after we are gone, whatever of justice may be withheld9 whilst we are here.  '*10
    # text = input('input what you want to say:')
    # A.send(text)
    print(A.recv())
    A.st.close()