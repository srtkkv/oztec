import argparse
import os.path


class installer():
    import platform
    import os
    import sys
    args = None
    def __init__(self,args):
        self.args = args
        pass
    def Windows_install(self):
        '''
         the procedure:
         1) copy the executable file to installation folder
         2) add the Windows service
         3) start the service
        :return:
        '''
        if self.args.service_folder is None:
            install_folder = self.os.getenv("ProgramFiles")
        else:
            install_folder = self.args.service_folder
        try:
            self.os.mkdir(install_folder)
            self.os.mkdir(os.path.join(install_folder,"logs"))
        except Exception as err:
            print(err.__str__())
            return {1:f"Can't create installation folder:'{install_folder}'"}
        print(f'copy {os.path.abspath(self.sys.executable)} {install_folder}')
        self.os.popen(f'copy {os.path.abspath(self.sys.executable)} {install_folder}')

        #https://thepythoncorner.com/posts/2018-08-01-how-to-create-a-windows-service-in-python/
        pass

    def mac_install(self):
        pass
    def install(self):
        '''
        The switcher between OS install procedures
        :return:
        '''
        if self.platform.platform()[:3] == "Win":
            return self.Windows_install()
        else:
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
    parser.add_argument('-s', '--service',
                        action='store_true')
    parser.add_argument('-sn', '--service_name', default="oZTeC service")
    parser.add_argument('-sf' , '--service_folder' , default=None)
    args = parser.parse_args()
    print( args.service, args.verbose, args.service_name)
    if args.service:
        print(installer(args).install())



