import DCC
C = DCC.Unit()
local = ('127.0.0.1', 13200)
datalink = ('127.0.0.1', 12201)
dest = ('127.0.0.1', 11200)
C.debug4(local, dest, datalink)
print('C.start to send')
C.send('11111')
aa = input('end...')