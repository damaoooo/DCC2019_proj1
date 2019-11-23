                            errorData = list(data[x[i]])
                            errorData[y[i]] = str(int(errorData[y[i]])^1)
                            patchData = ''.join(errorData)
                            data[x[i]]=patchData