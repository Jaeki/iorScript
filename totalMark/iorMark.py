import subprocess
import shlex
import re



class iorBench:

    def __init__(self,path,resultPath):

        self.options = {}
        self.path = path
        f = open(path,'r')
        self.lines = f.readlines()
        self.rPath = resultPath
        
        for line in self.lines:
            self.options[line.split(':')[0]] = line.split(':')[1].strip().split(',')



    def unitConverter(self,val):

        k = 1024
        M = 1024*1024
        G = 1024*1024*1024

        if val[-1] == 'k':
            return int(val.replace('k','')) * k

        if val[-1] == 'M':
            return int(val.replace('M','')) * M

        if val[-1] == 'G':
            return int(val.replace('G','')) * G

        assert False, 'unit convert error'

    def makeCommands(self):

        self.cmd = []
        basis = '--allow-run-as-root ior -w -r'

        for processOps in self.options['process']:
            
            processCmd = 'mpirun -np ' +processOps + " " + basis

            for blockOps in self.options['block']:

                blockCmd = processCmd + ' -b ' + blockOps

                for transferOps in self.options['transfer']:
                    
                    if self.unitConverter(transferOps) <= self.unitConverter(blockOps):



                        transCmd = blockCmd + ' -t ' + transferOps + " -o " + self.options['target'][0]+'testfile'
                        self.cmd.append(transCmd)
        
        subprocess.run(['mkdir',self.rPath])

        with open(self.rPath+"cmdList.txt",'w') as f:
            f.write(self.options['target'][0]+'\n')
            for cm in self.cmd:
                f.write(cm)
                f.write('\n')

        return self.cmd


    def getBenchName(self,cmd):

        optionName = self.path.split('/')[-1].split('.')[0]
        cmd = cmd.split('-o')[0].replace(' ','').replace('mpirun','').replace('-w-r','').replace('ior','').replace('-','_')
        cmd = cmd.replace('_allow_run_as_root_', '')
        
        return optionName+cmd+'_s'+str(self.options['stripe'][0])


    def contentExtractor(self,results,line,contentsName,index,file):

        val = results.split('\n')[line-1]
        num = re.findall("\d+\.\d+",val)
        file.write(contentsName+":")
        file.write(num[index])
        file.write('\n')

    def runBench(self):

        print('Total benchmarks : ',len(self.cmd))

        idx = 0
        for cm in self.cmd:

            print('Running :',idx,' / ',cm)
            with open(self.rPath+self.getBenchName(cm)+'.txt','w') as f:

                out = subprocess.check_output(shlex.split(cm))
                out = out.decode("utf-8")

                rst = []

                self.contentExtractor(out,34,'Write',1,f)

                self.contentExtractor(out,35,'Read',1,f)

                self.contentExtractor(out,39,'Write(IOP)',6,f)

                self.contentExtractor(out,40,'Read(IOP)',6,f)

                f.write('------------------------------------------\n')

                f.write(out)

            idx += 1


if __name__=='__main__':

    bn = iorBench('./options/case1.options','results/case1/')
    cmd = bn.makeCommands()
    # print(cmd[0])
    # bn.getBenchName(cmd[0])
    bn.runBench()
