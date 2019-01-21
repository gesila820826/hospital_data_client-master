#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 17:25
# @Author  : Zlh
# @Site    : 
# @File    : MonitorPid.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import win32serviceutil
import win32service
import win32event
import win32timezone
import psutil
import os
import datetime
import codecs
import json
from service_manager import ServiceManager
class Hospital_Monitor(win32serviceutil.ServiceFramework):
    _svc_name_         = 'Hospital_Monitor' #服务名称
    _svc_display_name_ = 'Hospital_Monitor AutoUpLoad Demo'
    _svc_description_  = 'Hospital_Monitor AutoUpLoad Demo demo.'

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.local = 'C:/'
        self.logger    = self._getLogger()
        self.run       = True
        self.pid_name  = 'hospital_service.exe'
        self.dirlocal  = os.path.dirname(os.path.realpath(__file__))
        self.ServiceName   = "PythonService"

    def _getLogger(self):
        import inspect
        import logging
        logger    = logging.getLogger('[Hospital_Monitor]')
        this_file = inspect.getfile(inspect.currentframe())
        # dirpath   = os.path.abspath(os.path.dirname(this_file))
        dirpath   = self.local
        handler   = logging.FileHandler(os.path.join(dirpath,'service.log'))
        formatter = logging.Formatter('%(asctime)s  %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def _GetServiceStatus(self):
        Temp_PidList = []
        pid_infoList =[]
        Temp_pidNotHandle = list(psutil.process_iter())  # 获取当前计算机的pid
        for each_pid in Temp_pidNotHandle:
            a = str(each_pid)  # each 是 class类型，可用type(each)查看类型
            # a 数据样式为：psutil.Process(pid=0, name='System Idle Process')
            Temp_PidList.append(a[15:-1])  # 只取括号内部分；pid=0, name='System Idle Process'
        for tempPid in Temp_PidList:
            each_infoList = tempPid.split(',')
            for temp in each_infoList:
                if 'name' in temp:
                    pid_infoList.append(temp.split('=')[1][1:-1])
        for temp_pid in pid_infoList:
            if self.pid_name == temp_pid:
                return True
        return False

    def ProceService(self):
        app = ServiceManager(self.ServiceName)
        if False == app.is_exists():
            self.logger.error('%s not exists'%self.ServiceName)
            return
        app_status = str(app.status())
        self.logger.info('%s status is:%s '%(self.ServiceName,app_status))
        if 'RUNNING' in app_status:
            return
        else:
            self.logger.info('PythonService is death now reboot............')
            result = str(app.restart())
            self.logger.info('restart %s  result:%s' % (self.ServiceName,result))

    def SvcDoRun(self):
        import time
        self.logger.info('service is run...')
        # self.my_print(self.local)
        while self.run:
            M = datetime.datetime.now().strftime('%H:%M').split(':')[1].strip()
            M = int(M)
            # 每隔5分钟判断一下服务是否正常
            if M % 5 == 0:
               self.logger.info('Hospital_Monitor is alive............')
               self.ProceService()
            time.sleep(60)

    def SvcStop(self):
        self.logger.info('Hospital_Monitor service is stop.')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    import sys
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(Hospital_Monitor)
            servicemanager.Initialize('Hospital_Monitor',evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(Hospital_Monitor)
