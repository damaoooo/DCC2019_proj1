from binascii import unhexlify,hexlify
def headersAndEnds():
    # sourceIp = self.local[0]
    # sourcePort = self.local[1]
    # destIp = self.dest[0]
    # destPort = self.dest[1]
    # Number = self.frameNumber
    sourceIp,sourcePort = '127.0.0.1',11400
    destIp,destPort = '127.0.0.1',12400
    Number = 0xf
    res =  []
    temp = ''
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
print(headersAndEnds())