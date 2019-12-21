import DCC
D = DCC.Unit()
local = ('127.0.0.1', 14200)
datalink = ('127.0.0.1', 14201)
dest = ('127.0.0.1', 13200)
D.debug4(local, dest, datalink)
print('D.start to recv')
print(D.recv())
res = input('end...')