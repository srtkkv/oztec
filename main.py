import argparse
import sys
import os

class installer():
    def __init__(self,os_name):
        print(os_name)
        pass
    def Windows_install(self):
        pass
    def mac_install(self):
        pass

class runner():
    def __init__(self):
        while True:
            pass
        pass

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument('-v', '--verbose',
                    action='store_true')
    parser.add_argument('-i', '--service',
                        action='store_true')
    parser.add_argument('-sn', '--service_name')
    args = parser.parse_args()
    print( args.service, args.verbose, args.service_name)
    if args.service:
        print(sys.hash_info)
        i = installer(sys.platform)
