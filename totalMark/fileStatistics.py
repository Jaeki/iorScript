import os 
import pickle
import sys

class fileStatistics:

    def __init__(self,rootPath):
        
        k = 1024
        M = 1024*1024
        G = 1024*1024*1024

        self.sizeDiv = [1*k,2*k,5*k,10*k,50*k,100*k,500*k,
                        1*M,10*M,50*M,100*M,500*M,
                        1*G,10*G,50*G]

        self.contained = []

        for (dirpath, dirnames, filenames) in os.walk(rootPath):
            self.contained += [os.path.join(dirpath, file) for file in filenames]
        
        self.fileSize = {}
        self.fileStat = {}

        for div in self.sizeDiv:
            self.fileStat[div] = 0

    def getFilesize(self):
        
        idx = 0
        for pth in self.contained:
            try:
                self.fileSize[pth] = os.path.getsize(pth)
            except:
                pass

        return self.fileSize

    def getStat(self):

        for _, sz in self.fileSize.items():
            self.fileStat[self.sizeDivider(sz)] += 1

        return self.fileStat

    
    def sizeDivider(self,fsize):
        
        for sz in self.sizeDiv:
            if fsize < sz:
                return sz

        return 50*1024*1024*1024




if __name__=='__main__':

    basicPath = sys.argv[1]
    
    print('path : ',basicPath)

    fstat = fileStatistics(basicPath)

    fstat.getFilesize()

    for div,sz in fstat.getStat().items():
        print("{} : {}".format(div,sz))