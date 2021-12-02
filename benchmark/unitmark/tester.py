import subprocess
import shlex
import re

class optionsReader:
    # def __init__(self):
        
    def parse(self,path,resultPath):
        self.results = {}
        self.path = path
        f = open(path,'r')
        self.lines = f.readlines()
        self.rPath = resultPath
        
        for line in self.lines:
            self.results[line.split(':')[0]] = line.split(':')[1].strip().split(',')

        # print(self.results)


    def getCommands(self):

        cmd = []
        basis = 'ior -w -r'

        for processOps in self.results['process']:
            
            processCmd = 'mpirun -np ' +processOps + " " + basis

            for shareOps in self.results['share']:
                
                shareCmd = processCmd

                if shareOps == 'False':
                    shareCmd = processCmd + ' -F'

                for blockOps in self.results['block']:

                    blockCmd = shareCmd + ' -b ' + blockOps

                    for transferOps in self.results['transfer']:
                        
                        transCmd = blockCmd + ' -t ' + transferOps + " -o " + self.results['target'][0]+'/testfile'

                        cmd.append(transCmd)
        
        self.targetPath = self.rPath+self.path.replace('.','').replace('txt','').split('/')[-1]+'/'

        subprocess.run(['mkdir',self.targetPath])

        with open(self.targetPath+"cmdList.txt",'w') as f:
            f.write(self.results['target'][0]+'\n')
            for cm in cmd:
                f.write(cm)
                f.write('\n')

        return cmd, self.targetPath


class cmdRunner():

    def runCmd(self,cmd,path):

        idx = 0
        self.gathers = []
        
        for cm in cmd:
            with open(path+'result_'+str(idx)+'.txt','w') as f: 
                out = subprocess.check_output(shlex.split(cm))
                out = out.decode("utf-8")
                f.write(out)
                rst = []
                out1 = out.split('\n')[33]
                # print(out1)
                num = re.findall("\d+\.\d+",out1)
                rst.append(num[0])
                # print(num)

                out2 = out.split('\n')[34]
                # print(out2)
                num = re.findall("\d+\.\d+",out2)
                rst.append(num[0])
                self.gathers.append(rst)
            idx +=1
        # print(self.gathers)

    def writeResults(self,path):

        with open(path+'/results_summary.txt','w') as f:
            for rst in self.gathers:
                for val in rst:
                    f.write(val+',')
                f.write('\n')



if __name__ == '__main__':
    reader = optionsReader()
    reader.parse('../options/all-big.txt','../results/')
    cmd,path = reader.getCommands()

    runner = cmdRunner()
    runner.runCmd(cmd,path)
    runner.writeResults(path)
