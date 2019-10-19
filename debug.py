def parseChunk(oneFrame):
    chunks = []
    while(oneFrame!=[]):
        oneChunk = oneFrame[0:10]
        chunks.append(oneChunk)
        oneFrame = oneFrame[10:]
    return chunks

frame = ['11111111']*100
print(parseChunk(frame))