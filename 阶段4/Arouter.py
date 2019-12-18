import DCC
import select
import routetable
def tuple2str(tup):
    return (str(tup[0])+':'+str(tup[1]))
def str2tuple(strs):
    l = strs.split(':')
    r = (l[0],int(l[1]))
    return r
switchtable = {'127.0.0.1:12100':'127.0.0.1:11102', '127.0.0.1:11200':'127.0.0.1:11201'}
Atable = routetable.routeTable()
routetable.addTable(('127.0.0.1',12000),("127.0.0.1",12100),1,Atable)
routetable.addTable(('127.0.0.1',))
a1 = DCC.Unit()
a1.debug4(('127.0.0.1',11100),('127.0.0.1',19986),('127.0.0.1',19985)) #第一个是本地，后两个乱绑定，不会动用它里面的发送函数
readable = [a1.sk]
print('start to host......')
while(1):
    rlist, wlist, elist = select.select(readable,[],[],timeout=0.5)
    for sks in rlist:
        rawBytes = sks.recv(40000)
        rawBins = a1.bytes2Bin(rawBytes)
        afterDirect = a1.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
        #判断是否定位成功
        if(afterDirect==-1):
            print('Frame direct Error!')
            continue
        #判断是否读取帧成功
        try:
            respondBytes, status, Info = a1.tcpLayer.recvControlCenter(a1,afterDirect)
            src = Info[1]
        except:
            print('Parse Frame Error! Info->',src)
            continue
        #判断时候在路由表内
        if():
            pass