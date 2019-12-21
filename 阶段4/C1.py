import DCC
C = DCC.Unit()
local = ('127.0.0.1', 13200)
datalink = ('127.0.0.1', 13201)
dest = ('127.0.0.1', 14200)
C.debug4(local, dest, datalink)
print('C.start to send')
C.send('11111'*10)
aa = input('end...')