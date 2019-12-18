class routeTable:
    destination = ''
    via = ''
    cost = 0

def addTable(dest, via, cost, table):
    r = routeTable()
    r.destination = dest
    r.via = via
    r.cost = cost
    table.append(r)

def isInnerWeb(dest1,dest2):
    ip1 = dest1[0].split('.')
    ip2 = dest2[0].split('.')
    port1 = dest1[1]
    port2 = dest2[1]
    ipTrue = 1
    for i in range(4):
        int1 = int(ip1[i])
        int2 = int(ip2[i])
        if(int1!=int2):
            if(int1==0 or int2==0):
                continue
            else:
                ipTrue = 0
                break
    return (str(port1)[:2]==str(port2)[:2]) and (ipTrue)

def getTable(tables, destination):
    for i in tables:
        if(i.destination == destination):
            return i
    return 'Can\'t find destination'

def aboveTable(tuble1, tuble2):
    ips1 = tuble1.destination[0].split('.')
    ips2 = tuble2.destination[0].split('.')
    for i in range(len(ips1)):
        if(int(ips1[i])>int(ips2[i])):
            return True
    port1 = tuble1.destination[1]
    port2 = tuble2.destination[1]
    if(port1>port2):
        return True
    else:
        return False

def sortTable(tables):
    lens = len(tables)
    for i in range(lens):
        for j in range(0,lens-i-1):
            if(aboveTable(tables[j],tables[j+1])):
                tables[j],tables[j+1] = tables[j+1],tables[j]

def showTable(tables):
    for i in tables:
        print(str(i.destination),str(i.via),str(i.cost))

# In this fxxking software there's only port is diffent so that you can only route by port,such a bull shit
def mergeTables(localtables, recvtables, local,recvfrom): 
    add = 0
    for oneRecvTables in recvtables:
        add = 0
        for oneLocalTables in localtables:
            writeAble = not(isInnerWeb(oneLocalTables.destination, oneRecvTables.destination) or isInnerWeb(local,oneRecvTables.destination))
            if(writeAble):
                add+=1
        if(add == len(localtables)):
            addTable(oneRecvTables.destination,recvfrom,oneRecvTables.cost+1,localtables)

def packageTables(tables):
    txt = []
    for i in tables:
        txt.append(str(i.destination))
        txt.append(str(i.via))
        txt.append(str(i.cost))
    return '|'.join(txt)

def unpackageTables(rawString):
    tables = []
    dest,via,cost = '','',''
    split = rawString.split('|')
    for i in range(len(split)):
        cnt = i%3
        if(cnt==0):
            dest = eval(split[i])
        elif(cnt==1):
            via = eval(split[i])
        elif(cnt==2):
            cost = int(split[i])
            addTable(dest,via,cost,tables)
    return tables
if __name__ == "__main__":
    tablesA,tablesB,tablesC,tablesD = [],[],[],[]
    addTable(('192.1.2.0',12000),('192.1.2.1',12100),1,tablesA)
    addTable(('192.1.1.0',11000),('192.1.1.1',11100),1,tablesB)
    addTable(('192.1.3.0',13000),('192.1.3.1',13100),1,tablesB)
    addTable(('192.1.2.0',12000),('192.1.2.1',12100),1,tablesC)
    addTable(('192.1.4.0',14000),('192.1.4.1',14100),1,tablesC)
    addTable(('192.1.3.0',13000),('192.1.3.1',13100),1,tablesD)
    addTable(('192.1.3.1',13001),('192.1.3.1',13100),1,tablesD)
    print('tables A')
    showTable(tablesA)
    print('tables B')
    showTable(tablesB)
    print('tables C')
    showTable(tablesC)
    print('tables D')
    showTable(tablesD)
    print('merge A,B,C,D')
    mergeTables(tablesA,tablesB,('192.1.1.1',11100),('192.1.2.1',12100))
    mergeTables(tablesB,tablesA,('192.1.2.1',12100),('192.1.2.1',12100))
    mergeTables(tablesC,tablesB,('192.1.3.1',13100),('192.1.2.1',12100))
    mergeTables(tablesB,tablesC,('192.1.2.1',12100),('192.1.3.1',13100))
    mergeTables(tablesC,tablesD,('192.1.3.1',13100),('192.1.4.1',14100))
    mergeTables(tablesD,tablesC,('192.1.4.1',14100),('192.1.3.1',13100))
    mergeTables(tablesA,tablesB,('192.1.1.1',11100),('192.1.2.1',12100))
    mergeTables(tablesB,tablesA,('192.1.2.1',12100),('192.1.2.1',12100))
    mergeTables(tablesC,tablesB,('192.1.3.1',13100),('192.1.2.1',12100))
    mergeTables(tablesB,tablesC,('192.1.2.1',12100),('192.1.3.1',13100))
    mergeTables(tablesC,tablesD,('192.1.3.1',13100),('192.1.4.1',14100))
    mergeTables(tablesD,tablesC,('192.1.4.1',14100),('192.1.3.1',13100))
    print('showtable A')
    showTable(tablesA)
    print('showtable B')
    showTable(tablesB)
    print('showtable C')
    showTable(tablesC)
    print('showtable D')
    showTable(tablesD)
    print('package tables D')
    packaged = packageTables(tablesD)
    print(packaged)
    print('unpackaged tables D')
    unpackage = unpackageTables(packaged)
    showTable(unpackage)