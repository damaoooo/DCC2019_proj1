import DCC
B = DCC.Unit()
local = ('127.0.0.1', 12200)
datalink = ('127.0.0.1', 11200)
dest = ('127.0.0.1', 11200)
B.debug4(local, dest, datalink)
print('B.start to recv')
print(B.recv())
res = input('end...')