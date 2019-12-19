import DCC
import select
import routetable
from random import randint
def tuple2str(tup):
    return (str(tup[0])+':'+str(tup[1]))

def str2tuple(strs):
    l = strs.split(':')
    r = (l[0],int(l[1]))
    return r

def isBytes(input):
    for i in range(40):
        if(input[i] == 49 or input[i] == 48):
            continue
        else:
            return True
    return False

#配置交换机表
switchtable = {
    '127.0.0.1:13100':'127.0.0.1:14101',
     '127.0.0.1:14200':'127.0.0.1:14102'
     }

#初始化路由表
Atable = []
routetable.addTable(('127.0.0.1',13000),("127.0.0.1",13100),1,Atable)

a1 = DCC.Unit()
#第一个是本地，后两个乱绑定，不会动用它里面的发送函数
local = ('127.0.0.1',14100)
a1.debug4(local,('127.0.0.1',19986),('127.0.0.1',19985)) 

readable = [a1.sk]
print('start to host......')
while(1):
    #随机交换路由表
    num = randint(1,10)
    if(num==3):
        packaged = routetable.packageTables(Atable).encode()
        waitForChunk = a1.bin2Frames(a1.bytes2Bin(packaged),306)
        afterChunk = a1.dataWrap(waitForChunk[0],0)
        a1.datalink = ('127.0.0.1',14101)
        a1.dest = ('127.0.0.1',13100)
        a1.tcpLayer.sendControlCenter(a1,afterChunk)
        print('send a copy of table')
    rlist, wlist, elist = select.select(readable,[],[],0.5)
    for sks in rlist:
        rawBytes = sks.recv(40000)
        print('A recv a new packet')
        if(isBytes(rawBytes)):
            rawBins = a1.bytes2Bin(rawBytes)
        else:
            rawBins = str(rawBytes)[2:-1]
        afterDirect = a1.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
        #判断是否定位成功
        if(afterDirect==-1):
            print('Frame direct Error!')
            continue
        #判断是否读取帧成功
        try:
            respondBytes, status, Info = a1.tcpLayer.recvControlCenter(a1,afterDirect)
            src = Info[1]
            frameFrom = Info[0]
        except:
            print('Parse Frame Error! Info->',src)
            continue
        #判断是否是路由信息
        if(src == local):
            print('-'*10,'recv table exchange','-'*10)
            routetable.showTable(Atable)
            recvTable = routetable.unpackageTables(respondBytes.decode())
            routetable.mergeTables(Atable,recvTable,local,frameFrom)
            routetable.showTable(Atable)
            continue
        #判断是否在路由表内
        picktable = routetable.findTables(src,Atable)
        if(picktable != False):
            dst = switchtable[tuple2str(picktable.via)]
            sendBins = bin(0xeeff)[2:] + afterDirect + bin(0xffee)[2:]
            sendBytes = a1.bin2Bytes(sendBins)
            sks.sendto(sendBytes, str2tuple(dst))
            print('route mode',src,'->',dst)
        #判断是否是内网
        elif(routetable.isInnerWeb(src,local)):
            dst = switchtable[tuple2str(src)]
            sendBins = bin(0xeeff)[2:] + afterDirect + bin(0xffee)[2:]
            sendBytes = a1.bin2Bytes(sendBins)
            sks.sendto(sendBytes, str2tuple(dst))
            print('switch mode',src,'->',dst)
        else:
            print('No route Item! ->','from:',frameFrom,'src:',src)
            