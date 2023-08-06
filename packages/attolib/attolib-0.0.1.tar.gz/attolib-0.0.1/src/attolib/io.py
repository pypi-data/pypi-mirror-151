import numpy as np

def SaveBinary(filename,arr):
    arr.astype(np.float64).tofile(filename)

def LoadBinary(filename,row=1,col=1,transpose=False,dtype=np.float64):
    data = np.fromfile(filename, dtype=dtype)
    data = np.reshape(data,[row,col])
    if transpose:
        data = data.T
    return data