import DCC
A = DCC.Unit()
local = ('127.0.0.1', 11200)
datalink = ('127.0.0.1', 12200)
dest = ('127.0.0.1', 12200)
A.debug4(local, dest, datalink)
print('A.start to send')
A.send('aaa这是中文こんばんは...\n'*100)
aa = input('end...')