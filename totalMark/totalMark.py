import sys
import iorMark as iorm
# import hwmark as hwm


if __name__ == '__main__':

    ior = iorm.iorBench(sys.argv[1],sys.argv[2])
    ior.makeCommands()
    ior.runBench()