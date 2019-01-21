#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 17:39
# @Author  : Zlh
# @Site    : 
# @File    : service_test.py
# @Software: PyCharm
from hospital_service import PythonService,HospitalUploadProc
from hospital_monitor import Hospital_Monitor
import os
import codecs
import json

class Test(PythonService,HospitalUploadProc):
    def __init__(self):
        self.local = 'C:/'
        self.logger = self._getLogger()
        # self._baseurl = 'http://39.96.91.138'
        self._baseurl = 'http://192.168.1.101:3000'
        # self._baseurl = 'http://39.96.91.138:3000'
        self._baseurl
        self.Pa_Info = 'PatientInfo.txt'
        self.SendFlag = False
        self._UpLoadCaseCount = 0


    def run_test(self):
        if os.path.exists(os.path.join(self.local, 'cfg.txt')):
            file1 = codecs.open(os.path.join(self.local, 'cfg.txt'), 'r').read()
            cfg_info = json.loads(file1)
            print(cfg_info)
            self.ProcUpLoadCase(cfg_info)

class MonitTest(Hospital_Monitor):
    def __init__(self):
        self.local = 'C:/'
        self.pid_name = 'hospital_service.exe'
        self.logger = self._getLogger()

    def run_test(self):
        self.ProceService()

if __name__ == '__main__':
    for_test_1 = Test()
    for_test_1.run_test()

    # for_test_2 = MonitTest()
    # for_test_2.run_test()