import argparse
import os.path
#from Core.win_service import SMWinservice
from Core.oztec import OZTEC


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
"""
class Server_mode_runner(SMWinservice):
    def start(self) :
        self.isrunning = True

    def stop(self) :
        self.isrunning = False

    def main(self) :
       pass
"""
if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument('-v', '--verbose',
                    action='store_true')
    parser.add_argument('-si', '--service_install',
                        action='store_true')
    parser.add_argument('-sn', '--service_name', default="oZTeC service")
    parser.add_argument('-sf' , '--service_folder' , default=None)
    parser.add_argument('-r', '--register', default=None, help="Register agent in oZTeS by --register URL")
    parser.add_argument('-c', '--config', default=None, help="Specify config path.")
    args = parser.parse_args()
    print( args.service_install, args.verbose, args.service_name, args.register, args.config)
    if args.service_install:
        print(installer(args).install())
    elif args.register is not None:
        empty_agent = OZTEC(cfg=args.config).register_agent(URL=args.register)
        pass



