from os import system
import socket
from binascii import unhexlify,b2a_hex
class method:
    def direction(self,text,keystart,keyend):
        start = text.find(keystart)
        end = text.find(keyend)
        if(start!=-1 and end!=-1):
            return text[start+len(keystart):end]
        else:
            return -1
            
    def str2binarr(self,text):
        num = list(text.encode())
        for i in range(len(num)):
            num[i] = bin(num[i])[2:].zfill(8)
        return num

    def frameWrap(self,binarr):
        res = []
        lens = len(binarr)
        frames = 0
        while(lens>0):
            lens-=8
            frames+=1
        for i in range(frames):
            oneFrame = binarr[i*8:(i+1)*8]
            row = ['0']*8
            crow = ['0']*8
            for oneFrameIndex in range(len(oneFrame)):
                if(oneFrame[oneFrameIndex].count('1')%2==1):
                    row[oneFrameIndex]='1'
            tempText = ''.join(oneFrame)
            for i in range(8):
                if(tempText[i::8].count('1')%2==1):
                    crow[i]='1'
            oneFrame.append(''.join(row))
            oneFrame.append(''.join(crow))
            res.append(oneFrame)
        return res

    def checkFrame(self,Frames):
        res = []
        for oneFrame in Frames:
            recvRow = list(oneFrame[-2])
            recvCrow = list(oneFrame[-1])
            data = oneFrame[:-2]
            row = ['0']*8
            crow = ['0']*8
            for dataIndex in range(len(data)):
                if(data[dataIndex].count('1')%2==1):
                    row[dataIndex]='1'
            tempText = ''.join(data)
            for pointer in range(8):
                if(tempText[pointer::8].count('1')%2==1):
                    crow[pointer] = '1'
            #try to correct the mistake
            mistakeX = []
            mistakeY = []
            for i in range(8):
                if(recvCrow[i]!=crow[i]):
                    mistakeY.append(i)
                if(recvRow[i]!=row[i]):
                    mistakeX.append(i)
            if(mistakeX==[] and mistakeY==[]):
                res.append(data)
            elif((mistakeX==[] and mistakeY!=[]) or (mistakeX!=[] and mistakeY==[])):
                res.append(data)
            else:
                for x in mistakeX:
                    section = list(data[x])
                    for y in mistakeY:
                        section[y] = str(int(section[y])^1)
                    data[x]=''.join(section)
                res.append(data)
        return res

    def parseFrames(self,Frames):
        #collect frames
        totalFrame = []
        for i in Frames:
            totalFrame+=i
        for i in range(len(totalFrame)):
            totalFrame[i] = eval('0b'+totalFrame[i])
        return bytes(totalFrame).decode()

    def frames2bytes(self,Frames):
        res = b''
        totalFrame = []
        for i in Frames:
            totalFrame+=i
        totalFrame = ''.join(totalFrame)
        s = list(map(''.join,zip(*[iter(totalFrame)]*8)))
        for i in s:
            binary = eval('0b'+i)
            emm = unhexlify(hex(binary)[2:])
            res+=emm
        return res
    def bytes2frames(self,bytesrecv):
        frames = []
        oneframe = []
        for i in bytesrecv:
            hexnum = bin(i)[2:].zfill(8)
            if(len(oneframe)!=10):
                oneframe.append(hexnum)
            else:
                frames.append(oneframe)
                oneframe=[]
                oneframe.append(hexnum)
        frames.append(oneframe)
        return frames
    def bytes2RawBin(self,recvBytes):
        text = ''
        for i in recvBytes:
            text+=bin(i)[2:].zfill(8)
        return text
    def rawBin2Bytes(self,rawBin):
        res = b''
        s = list(map(''.join,zip(*[iter(rawBin)]*8)))
        for i in s:
            binary = eval('0b'+i)
            emm = unhexlify(hex(binary)[2:])
            res+=emm
        return res
    def printTest(self,text):
        print(text)

class unit(method):
    def __init__(self):
        super().__init__()
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    local = 0
    dest = 0
    def start(self):
        system('cls')
        opcode = input('select mode: 1.release 2.debug send 3.debug recv\n ->')
        if(opcode == '2'):
            print('your input is ',opcode)
            self.local = ('127.0.0.1',11400)
            self.dest = ('127.0.0.1',11100)
            self.sk.bind(self.local)
        elif(opcode == '3'):
            print('your input is ',opcode)
            self.local = ('127.0.0.1',12400)
            self.dest = ('127.0.0.1',12100)
            self.sk.bind(self.local)
        else:
            print('your input is ',opcode)
            IP = input('please input your local IP address->')
            PORT = input('please input your local port->')
            self.local = (IP,int(PORT))
            toIP = input('please input opposite IP->')
            toPORT = input('please input opposite port->')
            self.dest = (toIP,int(toPORT))
            self.sk.bind(self.local)
    def send(self,text):
        datasend = method.frameWrap(self,method.str2binarr(self,text))
        bytesdata = method.frames2bytes(self,datasend)
        bytesdata = b'\x00\xee\xff'+bytesdata+b'\xff\xee\x00'
        #return bytesdata
        self.sk.sendto(bytesdata,self.dest)
    def receive(self):
        recv = self.sk.recv(1024)
        rawBin = method.bytes2RawBin(self,recv)
        directFrame = method.direction(self,rawBin,'1110111011111111','1111111111101110')
        frame = method.bytes2frames(self,method.rawBin2Bytes(self,directFrame))
        check = method.checkFrame(self,frame)
        data = method.parseFrames(self,check)
        print(data)
        
    def textIt(self,text):
        method.printTest(self,text)

        
        
#todo:字符转byte的方式就直接传输byte编码过的UTF-8会有自动识别的，就只需要考虑成帧，然后校验，然后组合了
# 一次传64个，添加16个校验位，一帧一共有80个数据，最开始有一个传输开始和结尾有一个传输结尾的密码作为组装的起止
#帧定位如果最后剩余的bit<=3会被清除掉，开始0x00ffff;结尾0xffff00，没有编码会是ffff
#todo:然后是滑动窗口的设计

context = 'hello world!'
A = unit()
A.start()
while(1):
    try:
        opcode = input('1->send,2->recv')
        if(opcode=='1'):
            context = input('input your input->')
            A.send(context)
        else:
            print('Waiting to receive...')
            A.receive()
    except Exception as e:
        print(e)
        continue