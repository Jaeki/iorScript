import pandas as pd
import os
import numpy as np
import sys

class dataEntity:
    
    def __init__(self):
        
        # lustre&ior variable -> baseData
        self.stripeSize = None
        self.transSize = None
        self.fileSize = None
        self.threadSize = None
        
        # H/W config -> configData
        self.ostSize = None
        self.ostType = None
        
        self.ostWrite = None
        self.ostRead = None
        self.ostBW = None
        
        # y variable -> resultsData
        self.maxWrite = None
        self.maxWriteIOP = None
        self.maxRead = None
        self.maxReadIOP = None
        
    def setMeasureConfigData(self,oWrite,oRead,oBW):
        self.ostWrite = oWrite
        self.ostRead = oRead
        self.ostBW = oBW
    
    def setPreConfigData(self,oSize,oType):
        self.ostSize = oSize
        # 0 : SSD, 1 : HDD, 2 : Mixed
        self.ostType = oType
        
    def setBaseData(self,strip,trans,fsize,tsize):
        self.stripeSize = strip
        self.transSize = trans
        self.fileSize = fsize
        self.threadSize = tsize
    
    def setBaseData(self,data):
        self.stripeSize = data[0]
        self.transSize = data[1]
        self.fileSize = data[2]
        self.threadSize = data[3]
        
    def setResultsData(self, mWrite, mWriteIOP, mRead, mReadIOP):
        self.maxWrite = mWrite
        self.maxWriteIOP = mWriteIOP
        self.maxRead = mRead
        self.maxReadIOP = mReadIOP
        
    def setResultsData(self, data):
        self.maxWrite = data[0]
        self.maxRead = data[1]
        self.maxWriteIOP = data[2]
        self.maxReadIOP = data[3]
        
#     def setConfigData(self, )
        
    def getData(self):
        self.Data = {}
        # from fine name
        self.Data['Stripe#'] = self.stripeSize
        self.Data['Xfer'] = self.transSize
        self.Data['Fsize'] = self.fileSize
        self.Data['Threads'] = self.threadSize
        
        #from external input
        self.Data['OST#'] = self.ostSize
        self.Data['Type'] = self.ostType
        
        #fron file contents
        self.Data['Write'] = self.maxWrite
        self.Data['WriteIOP'] = self.maxWriteIOP
        self.Data['Read'] = self.maxRead
        self.Data['ReadIOP'] = self.maxReadIOP
        
        return self.Data

class analyzer:
    
    def __init__(self,oSize,oType):
        self.table = pd.DataFrame(None,columns=['Stripe#','Xfer','Fsize','Threads','OST#','Type','Write','WriteIOP','Read','ReadIOP'])
        self.ostSize = oSize
        self.ostType = oType
        
    def appendTable(self,path):
        self.path = path
        self.fList = os.listdir(self.path)
        self.fList.pop(0)
        
        for file in self.fList:
#             print(file)
            
            entity = dataEntity()
            entity.setBaseData(self.extractFileName(file))
            entity.setResultsData(self.extractFileData(path+file))
            entity.setPreConfigData(self.ostSize,self.ostType)
            
#             print(entity.getData())
            self.table = self.table.append(entity.getData(),ignore_index=True)
    
    def unitConvert(self, input):
    
        k = 1024
        M = 1024*1024
        G = 1024*1024*1024
        
        if 'k' in input:
            return int(input.replace('k','')) * k
        
        if 'M' in input:
            return int(input.replace('M','')) * M
        
        if 'G' in input:
            return int(input.replace('G','')) * G
        
        print(input)
        assert False, "Unit conversion ERROR !!"
        
    def extractFileData(self,path):
        # write, read, writeiop, readiop order
        contents = []
        
        mWrite = None
        mRead = None
        writeIOP = None
        readIOP = None
        
        idx = 0
        f = open(path,'r')
        while True:
            line = f.readline()
            
            if idx == 0:
                mWrite = float(line.split(':')[1])
                
            if idx == 1:
                mRead = float(line.split(':')[1])
                
            if idx == 2:
                writeIOP = float(line.split(':')[1])
            
            if idx == 3:
                readIOP = float(line.split(':')[1])
            
            idx += 1
            
            if idx == 4: 
                break
        f.close()
            
        contents.append(mWrite)
        contents.append(mRead)
        contents.append(writeIOP)
        contents.append(readIOP)
        
        return contents
            
    
    
    def extractFileName(self,name):
        # strip,trans,fsize,tsize order
        contents = []
        strip = None
        trans = None
        fsize = None
        tsize = None
        
        
        name = name.split('.')[0].split('_')
        name.pop(0)
        
        for val in name:
            if 'np' in val:
                tsize = int(val.replace('np',''))
            
            if 'b' in val:
                fsize = self.unitConvert(val.replace('b',''))
                
            if 't' in val:
                trans = self.unitConvert(val.replace('t',''))
                
            if 's' in val:
                strip = int(val.replace('s',''))
        
        contents.append(strip)
        contents.append(trans)
        contents.append(fsize)
        contents.append(tsize)
        
        return contents
        
    def getTable(self):
        return self.table

if __name__=='__main__':
    
    # argv[1] -> Dir contained results txt file
    # argv[2] -> The number of OST 
    # argv[3] -> The Type of OST ; 0 : SSD, 1 : HDD, 2 : Mixed
    az = analyzer(sys.argv[2],sys.argv[3])
    az.appendTable(sys.argv[1])
    
    
    table = az.getTable()
    
    print(table)