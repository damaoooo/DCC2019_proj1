import DCC
import select
if (__name__=='__main__'):
    A = DCC.Unit()
    A.local = ('127.0.0.1',11400)
    A.opposite=[('127.0.0.1',12100),('127.0.0.1',13100),('127.0.0.1',14100)]
    A.sk.bind(A.local)
    while(1):
        rawBytes = A.recv(40000)
        rawBins = A.bytes2Bin(rawBytes)
        afterDirect = A.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
        onebytesText,status,frameInfo = A.tcpLayer.recvControlCenter(afterDirect)
        A.dest = frameInfo[1]
        A.tcp = A.tcpLayer(A.local,A.dest,A.sk)
        if(A.dest in A.opposite):
            A.sk.sendto(rawBytes,A.dest)
        if(A.dest[0] == '255.255.255.255'):
            for addrs in A.opposite:
                A.sk.sendto(rawBytes,addrs)
        else:
            print('Destination Error!')