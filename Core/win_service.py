# SMWinservice
# Base class to create winservice in Python
# -----------------------------------------
# Instructions:
# 1. Just create a new class that inherits from this base class
# 2. Define into the new class the variables
#    _svc_name_ = "nameOfWinservice"
#    _svc_display_name_ = "name of the Winservice that will be displayed in scm"
#    _svc_description_ = "description of the Winservice that will be displayed in scm"
# 3. Override the three main methods:
#     def start(self) : if you need to do something at the service initialization.
#                       A good idea is to put here the inizialization of the running condition
#     def stop(self)  : if you need to do something just before the service is stopped.
#                       A good idea is to put here the invalidation of the running condition
#     def main(self)  : your actual run loop. Just create a loop based on your running condition
# 4. Define the entry point of your module calling the method "parse_command_line" of the new class
# 5. Enjoy
# Credits: Davide Mastromatteo

import socket

import win32serviceutil

import servicemanager
import win32event
import win32service

class SMWinservice(win32serviceutil.ServiceFramework):    
    _svc_name_ = 'oZTeC'
    _svc_display_name_ = 'oZTeC service'
    _svc_description_ = 'test'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args, desc={}):
        self._svc_description_ = desc.get("Description") if desc.get("Description") is not None else "oZTeC service"
        self._svc_name_ = desc.get("name") if desc.get("name") is not None else "oZTeC"
        self._svc_display_name_ = desc.get("display_name") if desc.get("display_name") is not None else "oZTeClient service"

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):

        pass

    def stop(self):

        pass

    def main(self):
        # i = 0

        pass

if __name__ == '__main__':
    SMWinservice.parse_command_line()