class routeTable:
    destination = ''
    via = ''
    cost = 0

def addTable(dest,via,cost,table):
    r = routeTable()
    r.destination = dest
    r.via = via
    r.cost = cost
    table.append(r)

def getTable(tables,destination):
    for i in tables:
        if(i.destination == destination):
            return i
    return 'Can\'t find destination'

def aboveTable(tuble1,tuble2):
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

if __name__ == "__main__":
    tables = []
    addTable(('127.0.0.1',14851),('127.0.0.1',13987),4,tables)
    addTable(('127.0.0.1',12345),('127.0.0.1',23456),4,tables)
    
    showTable(tables)
    sortTable(tables)
    print('after sort...')
    showTable(tables)