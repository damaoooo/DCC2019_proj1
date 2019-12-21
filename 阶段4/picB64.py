import base64

def picEncodeBase64(path):
    file = open(path,'rb')
    base = base64.b64encode(file.read())
    file.close()
    return str(base)[2:-1]

def decodePic(bins,picType):
    imgdata = base64.b64decode(bins)
    file = open('.\\out.'+picType,'wb')
    file.write(imgdata)
    file.close()
    print('pic is saved in .\\out.xxx')
