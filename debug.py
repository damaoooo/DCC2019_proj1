from binascii import unhexlify
def bin2Bytes(binText):
    res = b''
    length = len(binText)
    while(length>0):
        singleByte = unhexlify(hex(eval('0b'+binText[0:4]))[2:]+hex(eval('0b'+binText[4:8]))[2:])
        res+=singleByte
        binText = binText[8:]
        length-=8
    return res


binText = '101101110001000011111111000000001111111100000000111111110000000011110000'
print(bin2Bytes(binText))