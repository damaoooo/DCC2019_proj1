import select
import DCC
dest1 = ('127.0.0.1',12100)
dest2 = ('127.0.0.1',12101)
b = DCC.Unit()
b.debug3()
table = {str(('127.0.0.1',13100)):('127.0.0.1',12101),str(('127.0.0.1',11100)):('127.0.0.1',12100)}
readable = [b.sk]
print('start....')
while(1):
    rlist,wlist,elist = select.select(readable,[],[],1)
    for sks in rlist:
        rawBytes = sks.recv(40000)
        rawBins = b.bytes2Bin(rawBytes)
        afterDirect = b.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
        if(afterDirect==-1):
            print('direct ERROR!')
            continue
        try:
            respondBytes,status,Info = b.tcpLayer.recvControlCenter(b,afterDirect)
            src = Info[1]
        except:
            continue
        if(str(src) in table):
            dst = table[str(src)]
            sendBytes = b'\xee\xff'+b.bin2Bytes(afterDirect)+b'\xff\xee'
            sks.sendto(sendBytes,dst)
            print(src,dst)
        elif(src[0]=='255.255.255.255'):
            for i in table:
                sendBytes = b'\xee\xff'+b.bin2Bytes(afterDirect)+b'\xff\xee'
                sks.sendto(sendBytes,table[i])
        else:
            print('no route')
