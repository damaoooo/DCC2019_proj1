import base64

def picEncodeBase64(path):
    file = open(path,'wb')
    base = base64.b64encode(file.read())
    file.close()
    return base

def decodePic(bins,picType):
    imgdata = base64.b64decode(bins)
    file = open('.\\out.'+picType,'wb')
    file.write(imgdata)
    file.close()
    print('pic is saved in .\\out.xxx')
