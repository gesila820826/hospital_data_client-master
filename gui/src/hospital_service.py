#encoding=utf-8
import win32serviceutil
import win32service
import win32event
import win32timezone
import os
import time
import codecs
import json
import datetime
import requests
import subprocess
import oss2
import re
from HospitalUploadProc import HospitalUploadProc,UpLoadResult,UpLoadResult_dit
def_dirname ='HA003C02201812190011'

class PythonService(win32serviceutil.ServiceFramework,HospitalUploadProc):
    _svc_name_         = 'PythonService' #服务名称
    _svc_display_name_ = 'PythonService AutoUpLoad Demo'
    _svc_description_  = 'PythonService AutoUpLoad Demo demo.'


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.local = 'C:/'
        self.logger    = self._getLogger()
        self.run       = True
        # self.local   = os.path.dirname(os.path.realpath(__file__))
        # self._baseurl  = 'http://www.xcmy.top'
        # self._baseurl  = 'http://39.96.42.137'
        # self._baseurl = 'http://39.96.91.138:3000'
        # self._baseurl = 'http://192.168.1.102:3000'
        self._baseurl  =  self._Get_url()
        self.Pa_Info   = 'PatientInfo.txt'
        self.SendFlag  = False
        self._UpLoadCaseCount = 0

    def _Get_url(self):
        if os.path.exists(os.path.join("C:/", 'cfg.txt')):
             cfg = json.loads(codecs.open(os.path.join("C:/", 'cfg.txt'), 'r').read())
             if 'url' in cfg.keys():
                 return  cfg['url']
        return 'http://api.medical.exaai.cn'

    def _getLogger(self):
        import inspect
        import logging
        logger    = logging.getLogger('[PythonService]')
        this_file = inspect.getfile(inspect.currentframe())
        # dirpath   = os.path.abspath(os.path.dirname(this_file))
        dirpath   = self.local
        handler   = logging.FileHandler(os.path.join(dirpath,'service.log'))
        formatter = logging.Formatter('%(asctime)s  %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger


    def save_SendData(self):
        file1 = codecs.open(os.path.join(self.local, 'cfg.txt'), 'r')
        cfg_info = json.loads(file1.read())
        file1.close()
        cfg_info['Send_Data'] = datetime.datetime.now().strftime('%m%d')
        result = json.dumps(cfg_info)
        file1 = codecs.open(os.path.join(self.local, 'cfg.txt'), 'w')
        file1.write(result)
        file1.close()

    def Comper_Time(self,Now_Time,Set_Time,cfg_info):
        if int(Now_Time.split(':')[0]) >=  int(Set_Time.split(':')[0]) and int(Now_Time.split(':')[1]) >= int(Set_Time.split(':')[1]):
            if 'Send_Data' not in cfg_info.keys():
                self.logger.info("can not find key Send_Data!" )
                self.save_SendData()
                return  True
            else:
                if datetime.datetime.now().strftime('%m%d') != cfg_info.get('Send_Data'):
                    self.logger.info("Now Time;%s != Send_Data:%s"%(datetime.datetime.now().strftime('%m%d'),cfg_info.get('Send_Data')))
                    self.save_SendData()
                    return True
        return  False

    def SendMsg(self,error_info):
        Send_Count = 0
        while True:
            if Send_Count > 4:
                self.my_print('无法连接至服务器地址：%s' % self._baseurl)
                return
            try:
                response = requests.post(url='{0}/CaseLog/create'.format(self._baseurl), data=json.dumps(error_info),
                                         headers={'Content-Type': 'application/json'})
                self.my_print('%s发送数据：%s' % (self._baseurl,json.dumps(error_info)))
                self.my_print('%s:发送数据校验失败消息成功!' % response.text)
                return
            except:
                Send_Count = Send_Count + 1
                self.my_print('%s:发送数据上传失败消息:%s失败!重试：%d次' % (self._baseurl, json.dumps(error_info), Send_Count))

    def ProcUpLoadCase(self,cfg_info):
        for Key in UpLoadResult_dit.keys():
            UpLoadResult_dit[Key] = []
        path_info = cfg_info.get('pa_dir')
        for hp_temp in os.listdir(cfg_info.get('pa_dir')):
            temp_path = os.path.join(path_info, hp_temp)
            self.logger.info(temp_path)
            if os.path.isdir(temp_path):
                self.logger.info('begin upload case:%s' % temp_path)
                UpLoadResult_dit[UpLoadResult.Total_Case].append(hp_temp)
                result = self.UpLoad_Case(self.Pa_Info, self._baseurl, temp_path, False)
                if result in UpLoadResult_dit.keys():
                    UpLoadResult_dit[result].append(hp_temp)
        temp_list = UpLoadResult_dit[UpLoadResult.Key_vaild]
        if len(temp_list):
            temp_string =''
            for temp in temp_list:
                hp_id = temp
                temp_string = temp_string+" 案例编号:{0}".format(hp_id, hp_id[0:5],hp_id[5:9])
            error_info = {
                'type': '3',
                'desc': '共计%d个数据校验失败,详情:%s'% (len(temp_list),temp_string),
                'case_id':' '
            }
            self.SendMsg(error_info)
        temp_list = UpLoadResult_dit[UpLoadResult.CaseId_vaild]
        if len(temp_list):
            self.logger.error('CaseId_vaild case:%d ' % len(temp_list))
            temp_string = ''
            for temp in temp_list:
                temp_string = temp_string + "案例编号:{0} ".format(temp)
            error_info = {
                'type': '4',
                'desc': '共计%d个案例命名不符合规范,详情：%s' % (len(temp_list),temp_string),
                'case_id':' '
            }
            self.SendMsg(error_info)
        temp_list = UpLoadResult_dit[UpLoadResult.Oss_vaild]
        if len(temp_list):
            self.logger.error('Oss_vaild case:%d ' % len(temp_list))
            temp_string = ''
            for temp in temp_list:
                temp_string = temp_string + "案例编号:{0} ".format(temp)
            error_info = {
                'type': '1',
                'desc': '共计%d个案例发送至OSS云端失败！详情：%s' % (len(temp_list), temp_string),
                'case_id': ' '
            }
            self.SendMsg(error_info)
        temp_list = UpLoadResult_dit[UpLoadResult.Oss_return_vaild]
        if len(temp_list):
            self.logger.error('Oss_return_vaild case:%d ' % len(temp_list))
            temp_string = ''
            for temp in temp_list:
                temp_string = temp_string + "案例编号:{0} ".format(temp)
            error_info = {
                'type': '5',
                'desc': '共计%d个案例发送至OSS云端返回失败！详情：%s' % (len(temp_list), temp_string),
                'case_id': ' '
            }
            self.SendMsg(error_info)
        temp_dit = {}
        for Key in UpLoadResult_dit.keys():
            temp_dit[str(Key)] = UpLoadResult_dit[Key]
        temp_dit['Send_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        result = json.dumps(temp_dit)
        file1 = codecs.open(os.path.join(self.local, 'uploadinfo'), 'a+')
        file1.writelines(result+'\n')
        file1.close()

    def SvcDoRun(self):
        import time
        self.logger.info('service is run...')
        # self.my_print(self.local)
        while self.run:
            M = datetime.datetime.now().strftime('%H:%M').split(':')[1].strip()
            M = int(M)
            if os.path.exists(os.path.join(self.local, 'cfg.txt')):
                file1 = codecs.open(os.path.join(self.local, 'cfg.txt'), 'r').read()
                cfg_info = json.loads(file1)
                # self.logger.info('get cfg info:%s' % cfg_info)
                Now_Time = datetime.datetime.now().strftime('%H:%M')
                Set_time = cfg_info.get('run_time')
                result = self.Comper_Time(Now_Time,Set_time,cfg_info)
                if M % 10 == 0:
                    self.logger.info("nowtime:%s,set_time:%s result:%d" % (Now_Time, Set_time,result))
                if result:
                    self.save_SendData()
                    self.logger.info('Now_time:%s > Set_time:%s' % (Now_Time, Set_time))
                    self.ProcUpLoadCase(cfg_info)
            else:
                self.logger.error('can not find cfg.txt in %s'%os.path.join(self.local, 'cfg.txt'))
            if M%10 ==0:
                self.logger.info('PythonService is alive............')
            time.sleep(60)

    def SvcStop(self):
        self.logger.info('service is stop.')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    import sys
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(PythonService)
            servicemanager.Initialize('PythonService',evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(PythonService)
