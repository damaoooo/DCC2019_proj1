from binascii import unhexlify
def addXorCheck(Frame):
    sumxor = 0
    for onebyte in Frame:
        sumxor ^=eval('0b'+onebyte)
    return bin(sumxor)[2:].zfill(8)
frame = ['11110000','01010101','11100010','10101010']
print(addXorCheck(frame))