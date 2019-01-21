# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""
import win32serviceutil
import win32service
import win32event
import winerror
import servicemanager
import logging
import os
import inspect
import time
import sys
from PyQt5.QtCore import pyqtSlot,QDateTime,QTime
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QDesktopWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
# from Ui_upload import Ui_MainWindow
import oss2
import json
import requests
import codecs
import  datetime
import win32timezone
import re
from PyQt5.QtCore       import QEvent
from HospitalUploadProc import HospitalUploadProc,UpLoadResult,UpLoadResult_dit
from Ui_upload          import Ui_MainWindow
from service_manager    import ServiceManager
def_dirname ='HA003C02201812190011'
# 重载函数，并定义信号，以便主程序处理
Key_vaild = 3

class UploadThread(QtCore.QThread,HospitalUploadProc):
    #完成时返回的信号量
    # finishSignal = QtCore.pyqtSignal(list)  # 信号
    trigger = QtCore.pyqtSignal(dict)
    def __init__(self,parent=None,op_type=None,input_array=dict):
        super(UploadThread, self).__init__(parent)
        self.working = True
        self.num  = 0
        self._type= op_type
        self._arry=input_array
        self._FileCount=0
        self._UpLoadCaseCount = 0
        self._TotalCase=0
        self.local = os.path.dirname(os.path.realpath(__file__))

    def start_timer(self):
        self.num = 0
        self.start()

    def install_service(self,ServiceName,ServicePath):
        count = 0
        app = ServiceManager(ServiceName)
        self.trigger.emit({'info': '正在%s启动服务，请稍后!............'%ServiceName})
        if False == app.is_exists():
            while True:
                if count > 3:
                     self.trigger.emit({'info': '%s服务安装失败' % ServiceName})  # 发送信号
                     return False
                cmd = '{0} --startup auto install'.format(os.path.join(self.local, ServicePath))
                os.system(cmd)
                if True == app.is_exists():
                    self.trigger.emit({'info': '%s服务安装成功'%ServiceName})  # 发送信号
                    break
                time.sleep(5)
                count =count + 1
        self.trigger.emit({'info': '%s服务安装成功'%ServiceName})  # 发送信('PythonService 服务安装成功！')
        if 'RUNNING' not in str(app.status()):
            count = 0
            while True:
                if count > 5:
                    self.trigger.emit({'info': '%s服务启动失败！' % ServiceName})  # 发送信号
                    return False
                app.restart()
                if 'RUNNING' in str(app.status()):
                    self.trigger.emit({'info': '%s服务启动成功!'%ServiceName})
                    return  True
                time.sleep(5)
                count = count + 1
                self.trigger.emit({'info': '%s服务启动失败，第%d次重试！' % (ServiceName,count)})  # 发送信号
        else:
            self.trigger.emit({'info': '%s服务已启动!'%ServiceName})
            return  True

    def StopService(self,ServiceName):
        app = ServiceManager(ServiceName)
        self.trigger.emit({'info': '正在停止%s服务，请稍后!............'%ServiceName})
        if False == app.is_exists():
            self.trigger.emit({'info': '%s服务已停止!'%ServiceName})
            # self.trigger.emit({'status': False})  # 发送信号
            return False
        if 'STOPPING' not in str(app.status()):
            while True:
                app.stop()
                if  'STOPPED' in str(app.status()):
                    self.trigger.emit({'info': '%s服务已停止!' % ServiceName})
                    return True
                else:
                    time.sleep(2)
        else:
            self.trigger.emit({'info': '%s服务已停止!'%ServiceName})
            return True

    def RemoveService(self,ServiceName,ServicePath):
        app = ServiceManager(ServiceName)
        count = 0
        if False == app.is_exists():
            self.trigger.emit({'info': '%s服务已删除！' % ServiceName})
            return True
        while True:
            if count > 5:
                self.trigger.emit({'info': '%s服务已标记为删除，请稍后再查看！' % ServiceName})
                return False
            if False == app.is_exists():
                self.trigger.emit({'info': '%s服务已删除！' % ServiceName})
                return True
            cmd = '{0} remove'.format(os.path.join(self.local, ServicePath))
            os.system(cmd)
            time.sleep(5)
            count =count + 1
            self.trigger.emit({'info': '正在删除%s服务，请稍后..........!' %ServiceName})


    def run(self):
        while self.working:
            # print("Working", self.thread())
            #返回结果
            if self._type =='manuUpLoad':
                self._FileCount = self.Get_File_Nub(self._arry.get('Case_Path'))
                result = self.UpLoad_Case(self._arry.get('Pa_info'),self._arry.get('baseurl') ,self._arry.get('Case_Path') ,self._arry.get('Force_flag'))
                # self.update_text_singal.emit("Running time:", '1')  # 发送信号
                self.trigger.emit({'status':result})# 发送信号

            elif self._type =='allUpLoad':
                count = 0
                temp_count = 0
                self._FileCount = 0
                self._UpLoadCaseCount = 0
                self._TotalCase =0
                self.trigger.emit({'info': '正在统计:%s内需要上传的文件个数,请稍后!' % self._arry.get('Case_Path')})  # 发送信号
                for Key in UpLoadResult_dit.keys():
                    UpLoadResult_dit[Key] = []
                for hp_temp in os.listdir(self._arry.get('Case_Path')):
                    temp_path = os.path.join(self._arry.get('Case_Path'), hp_temp)
                    if os.path.isdir(temp_path):
                        self._FileCount = self._FileCount + self.Get_File_Nub(temp_path)
                        self._TotalCase = self._TotalCase +1
                self.trigger.emit({'info': '%s内共计%d个文件需要上传！' % (self._arry.get('Case_Path'), self._FileCount )})  # 发送信号
                for hp_temp in os.listdir(self._arry.get('Case_Path')):
                    temp_path = os.path.join(self._arry.get('Case_Path'), hp_temp)
                    if os.path.isdir(temp_path):
                        self.trigger.emit({'info': '正在上传CASE文件:%s,请稍后!'%temp_path})  # 发送信号
                        UpLoadResult_dit[UpLoadResult.Total_Case].append(hp_temp)
                        result =self.UpLoad_Case(self._arry.get('Pa_info'),self._arry.get('baseurl') ,temp_path ,self._arry.get('Force_flag'))
                        if result in UpLoadResult_dit.keys():
                            UpLoadResult_dit[result].append(hp_temp)
                        if UpLoadResult.Proc_Ok == result:
                            temp_count = temp_count+1
                        count=count+1
                        self.trigger.emit({'case_count': count,'total_case':self._TotalCase})  # 发送信号
                # print(UpLoadResult_dit)
                self.trigger.emit({'info':self.PraceResult(UpLoadResult_dit)})  # 发送信号
                self.trigger.emit({'status': temp_count})  # 发送信号

            elif self._type =='StartService':
                self.install_service('PythonService','hospital_service.exe')
                result =  self.install_service('Hospital_Monitor','hospital_monitor.exe')
                self.trigger.emit({'status':result})

            elif self._type=='StopService':
                self.StopService('Hospital_Monitor')
                result = self.StopService('PythonService')
                self.trigger.emit({'status': result})

            elif self._type == 'DeleteService':
                self.RemoveService('Hospital_Monitor','hospital_monitor.exe')
                result = self.RemoveService('PythonService','hospital_service.exe')
                self.trigger.emit({'status': result})

            return
            ##self.signal_time.emit("Running time:",'1')  # 发送信号

class MainWindow(QMainWindow,Ui_MainWindow,HospitalUploadProc):
    """
    Class documentation goes here.
    """
    def get_dataDir(self):
        if os.path.exists(os.path.join("C:/",'cfg.txt')):
            return json.loads(codecs.open(os.path.join("C:/",'cfg.txt'), 'r').read()).get('pa_dir')
        else:
            return os.path.dirname(os.path.realpath(__file__))

    def get_setTime(self):
        if os.path.exists(os.path.join("C:/", 'cfg.txt')):
            temp_time=json.loads(codecs.open(os.path.join("C:/", 'cfg.txt'), 'r').read()).get('run_time')
            H  = int(temp_time.split(':')[0])
            M1 = int(temp_time.split(':')[1][:1])
            M2 = int(temp_time.split(':')[1][-1:])
            self.timeEdit.setTime(QtCore.QTime(H, M1, M2))
        else:
            # 设置系统的默认运行时间
            self.timeEdit.setTime(QtCore.QTime(16, 0, 0))

    def Get_url(self):
        if os.path.exists(os.path.join("C:/", 'cfg.txt')):
             cfg = json.loads(codecs.open(os.path.join("C:/", 'cfg.txt'), 'r').read())
             if 'url' in cfg.keys():
                 return  cfg['url']
        return 'http://api.medical.exaai.cn'

    def Get_Server_Status(self):
        app = ServiceManager('PythonService')
        if False == app.is_exists():
            self.statusBar.showMessage('服务未安装！')
            return
        self.statusBar.showMessage('服务的运行状态为：%s'%app.status())

    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._runtTime       = ''
        self.local           = os.path.dirname(os.path.realpath(__file__))
        # self._dataDir        = os.path.dirname(os.path.realpath(__file__))
        self._dataDir        = self.get_dataDir()
        self.id              ='LTAInP47aO9oWL93'
        self.key             ='yRBFKapTmX0d4u95WD2jNtKdW88F4u'
        self.bucket          ='exa-hospital'
        self._baseurl        = self.Get_url()
        # self._baseurl        ='http://www.xcmy.top'
        # self._baseurl ='http://39.96.42.137'
        # self._baseurl ='http://39.96.91.138:3000'
        self.UpLoad_Case_Nub = 0
        self.Pa_Info              ='PatientInfo.txt'
        self.Pa_Info_path_arry    = []
        self.Pa_Info_Current_Path =''
        self.Pa_Info_current_index  =0
        self.SaveInfo={}
        self.CaseCount       = 0
        self.File_Count      = 0
        self._Flag = {
            'allUpLoad'  : False,
            'manuUpLoad' : False,
            'StartService': False,
            'StopService': False,
            'DeleteService': False,
            'EditCase':False,

        }
        self.move_center()
        #禁止窗体拖动以及最小化操作
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setFixedSize(441, 484)
        self.setWindowIcon(QIcon('1.ico'))  # 设置窗体标题图标
        self.get_setTime()
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.groupBox_4.setVisible(False)
        self.radioButton_2.setChecked(True)
        # MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.textBrowser.append('案例路径为：'+self._dataDir)
        self.textBrowser.append('URL：' + self._baseurl)
        ##设置系统的默认运行时间
        #self.timeEdit.setTime(QtCore.QTime(15,0,0))
        self.Get_Server_Status()
        self.progressBar.setVisible(False)
        # '3 5 6 15 20 0'
        self.lineEdit_5.installEventFilter(self)
        self.lineEdit_3.installEventFilter(self)
        self.lineEdit_6.installEventFilter(self)
        self.lineEdit.installEventFilter(self)
        self.lineEdit_15.installEventFilter(self)
        self.lineEdit_20.installEventFilter(self)
        self.lineEdit_24.installEventFilter(self)
        self.lineEdit_7.installEventFilter(self)
        self.timeEdit.setEnabled(False)
        self.textBrowser.append(self.ReadResultInfo(os.path.join('C:/','uploadinfo')))

    def move_center(self):
        screen = QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(x_move_step, y_move_step)


    def save_path_info(self):
        temp_dir = {
            'pa_dir'  : self._dataDir,
            'run_time': self._runtTime,
            'local_path':self.local,
            'url':self._baseurl,
        }
        result = json.dumps(temp_dir)
        file1 = codecs.open(os.path.join('C:/', 'cfg.txt'), 'w')
        file1.write(result)
        file1.close()


    @pyqtSlot(QDateTime)
    def on_timeEdit_dateTimeChanged(self, dateTime):
        # self.textBrowser.append(dateTime.toString('hh:mm'))
        self._runtTime = dateTime.toString('hh:mm')
        self.save_path_info()

    @pyqtSlot(QTime)
    def on_timeEdit_timeChanged(self, time):
        self._runtTime = time.toString('hh:mm')
        # self.textBrowser.append('案例路径为：' + self._runtTime)
        self.save_path_info()

    def ManHandUpLoad(self):
        pa_info = os.path.join(self._dataDir,'PatientInfo.txt')
        if False == os.path.exists(pa_info):
            QMessageBox.critical(self, "错误",
                                 self.tr('用户选择的文件夹:{0},未包含病人信息文件:{1}'.format(self._dataDir, 'PatientInfo.txt')))
            self.statusBar.showMessage('手动上传文件失败！')
            return

        if False == self.Check_PatientInfo(pa_info):
            QMessageBox.critical(self, "错误",self.tr('案例:{0}信息不全，请点击编辑案例补充信息！'.format(pa_info)))
            self.statusBar.showMessage('手动上传文件失败！')
            return

        hp_id = os.path.split(self._dataDir)[1]
        # if len(hp_id) != len(def_dirname):
        #     QMessageBox.critical(self, "错误",
        #                          self.tr('用户选择的文件夹:{0},文件夹命名不符合规范!请参考：{1}'.format(self._dataDir,def_dirname)))
        #     self.statusBar.showMessage('手动上传文件失败！')
        #     return

        self.statusBar.showMessage('开始上传case：%s,请稍后............' % os.path.split(self._dataDir)[1])
        temp_op_arry ={
            'Pa_info':self.Pa_Info,
            'baseurl':self._baseurl,
            'Case_Path':self._dataDir,
            'Force_flag':True
        }
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.StopService.setEnabled(False)
        self.radioButton_6.setEnabled(False)
        self.progressBar.setVisible(True)
        self.MauUpload.setEnabled(False)
        self.statusBar.showMessage('')
        self.textBrowser.clear()
        self.thread = UploadThread(op_type='manuUpLoad',input_array=temp_op_arry)
        self.thread.trigger.connect(self.update_text)
        self.thread.start()

    def update_text(self,result):
        if self._Flag.get('manuUpLoad'):
            if 'status' in result.keys():
                self.pushButton.setEnabled(True)
                self.AutoUpload.setEnabled(True)
                self.AllUpLoad.setEnabled(True)
                self.StopService.setEnabled(True)
                self.radioButton_6.setEnabled(True)
                self.progressBar.setVisible(False)
                self.MauUpload.setEnabled(True)
                self.radioButton.setEnabled(True)
                if UpLoadResult.Proc_Ok == result.get("status"):
                    self.statusBar.showMessage('案例上传成功！')
                    self.textBrowser.clear()
                else:
                    self.statusBar.showMessage('案例上传失败！')
            elif  'file_count' in result.keys():
                temp = result['file_count'].split(':')
                self.progressBar.setValue((int(temp[1])/int(temp[0]))*100)
            else:
                self.textBrowser.append(result.get('info'))
        elif self._Flag.get('allUpLoad'):
            if 'status' in result.keys():
                self.pushButton.setEnabled(True)
                self.AutoUpload.setEnabled(True)
                self.AllUpLoad.setEnabled(True)
                self.StopService.setEnabled(True)
                self.radioButton_6.setEnabled(True)
                self.progressBar.setVisible(False)
                self.MauUpload.setEnabled(True)
                self.radioButton.setEnabled(True)
                self.statusBar.showMessage('共%d个案例，成功插入%d个案例。'%(self.CaseCount,result.get("status")))
            elif 'file_count' in result.keys():
                # self.textBrowser.append(result['file_count'])
                temp = result['file_count'].split(':')
                self.progressBar.setValue((int(temp[1]) / int(temp[0])) * 100)
            elif 'case_count' in  result.keys():
                self.statusBar.showMessage('共%d个案例，已处理%d个案例' % (result["total_case"],result["case_count"]))
            else:
                self.textBrowser.append(result.get('info'))
        elif self._Flag.get('StartService'):
            if 'status' in result.keys():
                self.pushButton.setEnabled(True)
                self.AutoUpload.setEnabled(True)
                self.AllUpLoad.setEnabled(True)
                self.StopService.setEnabled(True)
                self.radioButton_6.setEnabled(True)
                self.MauUpload.setEnabled(True)
                self.radioButton.setEnabled(True)
                if False == result.get("status"):
                    QMessageBox.critical(self, "错误",self.tr('服务启动失败!'))
            else:
                self.textBrowser.append(result.get('info'))

        elif self._Flag.get('StopService'):
            if 'status' in result.keys():
                self.pushButton.setEnabled(True)
                self.AutoUpload.setEnabled(True)
                self.AllUpLoad.setEnabled(True)
                self.StopService.setEnabled(True)
                self.radioButton_6.setEnabled(True)
                self.MauUpload.setEnabled(True)
                self.radioButton.setEnabled(True)
            else:
                self.textBrowser.append(result.get('info'))

        elif self._Flag.get('DeleteService'):
            if 'status' in result.keys():
                self.pushButton.setEnabled(True)
                self.AutoUpload.setEnabled(True)
                self.AllUpLoad.setEnabled(True)
                self.StopService.setEnabled(True)
                self.radioButton_6.setEnabled(True)
                self.MauUpload.setEnabled(True)
                self.radioButton.setEnabled(True)
                self.radioButton_6.setEnabled(True)
            else:
                self.textBrowser.append(result.get('info'))

    def StartService(self):
        if 0 == self.Check_Case_Nub(self._dataDir):
            QMessageBox.critical(self, "错误", self.tr('用户选择的路径：%s中找不到任何%s文件!请检查路径配置!' % (self._dataDir, self.Pa_Info)))
            self.statusBar.showMessage('启动服务失败！')
            return
        Case_VaildList = self.Check_CaseIdByDir(self._dataDir)
        if len(Case_VaildList):
            self.textBrowser.clear()
            for temp_case in Case_VaildList:
                self.textBrowser.append('案例文件夹:%s命名不符合规范！' % temp_case)
            box = QMessageBox(QMessageBox.Warning, "提示", self.tr('有%d个案例命令不符合规范，是否忽视？' % len(Case_VaildList)),
                              QMessageBox.NoButton, self)
            qyes = box.addButton(self.tr("确定"), QMessageBox.YesRole)
            qno = box.addButton(self.tr("取消"), QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == qno:
                return
        case_count = self.Check_PainfoKey_ByDir(self._dataDir)
        if case_count:
            box = QMessageBox(QMessageBox.Warning, "提示", self.tr('有%d个案例信息不全，是否忽视？' % case_count), QMessageBox.NoButton,self)
            qyes = box.addButton(self.tr("确认"), QMessageBox.YesRole)
            qno = box.addButton(self.tr("取消"), QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == qno:
                return
        if False == os.path.exists(os.path.join(self.local, 'hospital_service.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_service.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        if False == os.path.exists(os.path.join(self.local, 'hospital_monitor.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_monitor.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        self.statusBar.showMessage('')
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.StopService.setEnabled(False)
        self.radioButton_6.setEnabled(False)
        self.MauUpload.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.thread = UploadThread(op_type='StartService')
        self.thread.trigger.connect(self.update_text)
        self.thread.start()
        return

    def StopService_Temp(self):
        if False == os.path.exists(os.path.join(self.local, 'hospital_service.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_service.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        if False == os.path.exists(os.path.join(self.local, 'hospital_monitor.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_monitor.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        self.statusBar.showMessage('')
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.StopService.setEnabled(False)
        self.radioButton_6.setEnabled(False)
        self.MauUpload.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.thread = UploadThread(op_type='StopService')
        self.thread.trigger.connect(self.update_text)
        self.thread.start()

    def DeleteService_Temp(self):
        if False == os.path.exists(os.path.join(self.local, 'hospital_service.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_service.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        if False == os.path.exists(os.path.join(self.local, 'hospital_monitor.exe')):
            QMessageBox.critical(self, "错误", self.tr('文件:%s不存在！' % (os.path.join(self.local, 'hospital_monitor.exe'))))
            self.statusBar.showMessage('启动服务失败！')
            return
        self.statusBar.showMessage('')
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.StopService.setEnabled(False)
        self.MauUpload.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.thread = UploadThread(op_type='DeleteService')
        self.thread.trigger.connect(self.update_text)
        self.thread.start()

    def AllUpLoadProc(self):
        Case_Nub = self.Check_Case_Nub(self._dataDir)
        self.CaseCount = Case_Nub
        if 0 == Case_Nub:
            QMessageBox.critical(self, "错误", self.tr('用户选择的路径：%s中找不到任何%s文件!' % (self._dataDir,self.Pa_Info)))
            self.statusBar.showMessage('全部上传失败！')
            return
        Case_VaildList=self.Check_CaseIdByDir(self._dataDir)
        if len(Case_VaildList):
           self.textBrowser.clear()
           for temp_case in Case_VaildList:
               self.textBrowser.append('案例文件夹:%s命名不符合规范！'%temp_case)
           box = QMessageBox(QMessageBox.Warning, "提示", self.tr('有%d个案例命令不符合规范，是否忽视？' % len(Case_VaildList)), QMessageBox.NoButton,self)
           qyes = box.addButton(self.tr("确定"), QMessageBox.YesRole)
           qno = box.addButton(self.tr("取消"), QMessageBox.NoRole)
           box.exec_()
           if box.clickedButton() == qno:
               return
        temp_count = self.Check_PainfoKey_ByDir(self._dataDir)
        if temp_count:
            box = QMessageBox(QMessageBox.Warning, "提示", self.tr('有%d个案例信息不全，是否忽视？' % temp_count),QMessageBox.NoButton, self)
            qyes = box.addButton(self.tr("确定"), QMessageBox.YesRole)
            qno =  box.addButton(self.tr("取消"), QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == qno:
                return
        temp_op_arry = {
            'Pa_info': self.Pa_Info,
            'baseurl': self._baseurl,
            'Case_Path': self._dataDir,
            'Force_flag': True
        }
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.StopService.setEnabled(False)
        self.radioButton_6.setEnabled(False)
        self.MauUpload.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.progressBar.setVisible(True)
        self.statusBar.showMessage('')
        self.textBrowser.clear()
        self.thread = UploadThread(op_type='allUpLoad', input_array=temp_op_arry)
        self.thread.trigger.connect(self.update_text)
        self.thread.start()

        # for hp_temp in os.listdir(self._dataDir):
        #     temp_path = os.path.join(self._dataDir, hp_temp)
        #     if os.path.isdir(temp_path):
        #         self.textBrowser.append('开始上传case：%s,请稍后............' % hp_temp)
        #         result = self.UpLoad_Case(self.Pa_Info, self._baseurl, temp_path, True)
        #
        #         self.UpLoad_Case_Nub = self.UpLoad_Case_Nub + int(result)
        #         self.textBrowser.append('case：%s,上传结束！............' % hp_temp)
        # QMessageBox.information(self, "提示", self.tr("用户数据上传完成,共上传%d个数据" % self.UpLoad_Case_Nub))
        # self.statusBar.showMessage('共计%d个案例，成功上传%d个案例！' % (Case_Nub, self.UpLoad_Case_Nub))

    def Init_EditCase(self,CasePaInfoPath):
        self.textBrowser.append('正在编辑' + CasePaInfoPath)
        PaInfo ={}
        self.SaveInfo.clear()
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_20.setText('')
        self.lineEdit_21.setText('')
        self.lineEdit_22.setText('')
        self.lineEdit_24.setText('')
        self.lineEdit_25.setText('')
        self.textEdit.setText('')
        self.lineEdit_5.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_3.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_6.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_15.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_20.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_24.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit_7.setStyleSheet("background-color:rgb(255, 255, 255)")

        self.Read_PatientInfo(PaInfo,CasePaInfoPath,self.SaveInfo)
        # print(PaInfo)
        Key_arry = []
        Key_arry = PaInfo.keys()
        if 'Name' in Key_arry:
            self.lineEdit_5.setText(PaInfo.get('Name'))
        if 'Birthdate' in Key_arry:
            self.lineEdit_6.setText(PaInfo.get('Birthdate'))
        if 'ClinicDate' in Key_arry  and 'ClinicTime' in Key_arry:
            self.lineEdit_19.setText(PaInfo.get('ClinicDate')+' '+PaInfo.get('ClinicTime'))
            self.lineEdit_19.setEnabled(False)
        # self.lineEdit_7.setText(PaInfo.get('Gender'))
        # self.lineEdit_7.setEnabled(False)
        if 'GA'in Key_arry:
            self.lineEdit_20.setText(PaInfo.get('GA'))
        if 'BirthWeight' in Key_arry:
            self.lineEdit_15.setText(PaInfo.get('BirthWeight'))
        if 'Phone' in Key_arry:
            self.lineEdit_3.setText(PaInfo.get('Phone'))
        if 'CorrectGA' in Key_arry:
            self.lineEdit_21.setText(PaInfo.get('CorrectGA'))
        if 'Gender' in  Key_arry:
            if PaInfo.get('Gender') in ['男','女']:
                self.comboBox.setCurrentText( PaInfo.get('Gender'))
        if  'LitterIndex' in  PaInfo.keys():
            if len(PaInfo.get('LitterIndex')) > 0:
                temp_str_index = PaInfo.get('LitterIndex').split()[0]
                if temp_str_index in ['单', '双','三','四','其他']:
                    self.comboBox_2.setCurrentText(temp_str_index)
                    temp_str = PaInfo.get('LitterIndex')
                    if '双' in  PaInfo.get('LitterIndex'):
                        self.groupBox_4.setVisible(True)
                        if '2-2' in  temp_str:
                            self.radioButton_3.setChecked(True)
                    elif '三' in PaInfo.get('LitterIndex'):
                        self.groupBox_4.setVisible(True)
                        if '3-2' in  temp_str:
                            self.radioButton_3.setChecked(True)
                        elif '3-3' in temp_str:
                            self.radioButton_4.setChecked(True)
                    elif '四' in PaInfo.get('LitterIndex'):
                        self.groupBox_4.setVisible(True)
                        if '4-2' in temp_str:
                            self.radioButton_3.setChecked(True)
                        elif '4-3' in temp_str:
                            self.radioButton_4.setChecked(True)
                        elif '4-4' in temp_str:
                            self.radioButton_5.setChecked(True)
        if 'MatherName' in Key_arry:
            self.lineEdit.setText(PaInfo.get('MatherName'))
        if 'MatherID' in Key_arry:
            self.lineEdit_2.setText(PaInfo.get('MatherID'))
        if 'Home Address' in Key_arry:
            self.lineEdit_4.setText(PaInfo.get('Home Address'))
        if 'SelfId' in Key_arry:
            self.lineEdit_11.setText(PaInfo.get('SelfId'))
        if 'Pregnancy' in Key_arry:
            if PaInfo.get('Pregnancy') in ['引导产', '剖腹产']:
                self.comboBox_3.setCurrentText(PaInfo.get('Pregnancy'))
        if 'Oxygen' in Key_arry:
            if len(PaInfo.get('Oxygen')) > 0:
                if PaInfo.get('Oxygen') in ['是', '否']:
                    self.comboBox_4.setCurrentText(PaInfo.get('Oxygen'))
        # self.comboBox.setCurrentText('女')
        if 'BirthHospital' in Key_arry:
            self.lineEdit_22.setText(PaInfo.get('BirthHospital'))
        if 'PhotoID' in Key_arry:
            self.lineEdit_12.setText(PaInfo.get('PhotoID'))
        if 'VisitID' in Key_arry:
            self.lineEdit_24.setText(PaInfo.get('VisitID'))
        if 'HospitalNum' in Key_arry:
            self.lineEdit_7.setText(PaInfo.get('HospitalNum'))
        if 'NativePlace' in Key_arry:
            self.lineEdit_25.setText(PaInfo.get('Native Place'))
        if 'Disease' in Key_arry:
            self.textEdit.setText(PaInfo.get('Disease'))
        if 'Other' in Key_arry:
            self.lineEdit_8.setText(PaInfo.get('Other'))

    def Save_CaseInfo(self,SaveInfoDict,Key,KeyName,Value):
        #空字典
        if SaveInfoDict == {}:
           self.my_print('error! Dict is null!')
           SaveInfoDict[KeyName] = Value
           return
        if isinstance(SaveInfoDict,dict):
            for temp_key in SaveInfoDict.keys():
                if Key in temp_key:
                    SaveInfoDict[temp_key] = Value
                    return
            SaveInfoDict[KeyName] = Value

    def Get_EditCase(self):
        self.Save_CaseInfo(self.SaveInfo, '母亲姓名(Mather Name)', '母亲姓名(Mather Name)', self.lineEdit.text())
        self.Save_CaseInfo(self.SaveInfo, '母亲身份证号(Mather ID)', '母亲身份证号(Mather ID)', self.lineEdit_2.text())
        self.Save_CaseInfo(self.SaveInfo, '患者电话(Phone)','患者电话(Phone)',self.lineEdit_3.text())
        self.Save_CaseInfo(self.SaveInfo, '家庭地址(Home Address)', '家庭地址(Home Address)', self.lineEdit_4.text())
        self.Save_CaseInfo(self.SaveInfo, '患者姓名(Name)', '患者姓名(Name)', self.lineEdit_5.text())
        self.Save_CaseInfo(self.SaveInfo, '身份证号(Self Id)', '身份证号(Self Id)', self.lineEdit_11.text())
        self.Save_CaseInfo(self.SaveInfo, '出生日期(Birthdate)', '出生日期(Birthdate)', self.lineEdit_6.text())
        self.Save_CaseInfo(self.SaveInfo, '患者性别(Gender)', '患者性别(Gender)', self.comboBox.currentText())
        Litter_result = ''
        if '单' in self.comboBox_2.currentText() or '其他' in self.comboBox_2.currentText():
            # self.SaveInfo['胎数(Litter Index)'] =2 self.comboBox_2.currentText()
            Litter_result = self.comboBox_2.currentText()
        elif '双' in self.comboBox_2.currentText():
            if self.radioButton_2.isChecked():
                Litter_result = '双 2-1'
            elif self.radioButton_3.isChecked():
                Litter_result = '双 2-2'
        elif '三' in self.comboBox_2.currentText():
            if self.radioButton_2.isChecked():
                Litter_result = '三 3-1'
            elif self.radioButton_3.isChecked():
                Litter_result = '三 3-2'
            elif self.radioButton_4.isChecked():
                Litter_result = '三 3-3'
        elif '四' in self.comboBox_2.currentText():
            if self.radioButton_2.isChecked():
                Litter_result = '四 4-1'
            elif self.radioButton_3.isChecked():
                Litter_result = '四 4-2'
            elif self.radioButton_4.isChecked():
                Litter_result = '四 4-3'
            elif self.radioButton_5.isChecked():
                Litter_result = '四 4-4'
        self.Save_CaseInfo(self.SaveInfo, '胎数(Litter Index)', '胎数(Litter Index)', Litter_result)
        self.Save_CaseInfo(self.SaveInfo, '出生体重（kg）(BirthWeight)', '出生体重（kg）(BirthWeight)', self.lineEdit_15.text())
        self.Save_CaseInfo(self.SaveInfo, '出生胎龄（周）(GA)', '出生胎龄（周）(GA)', self.lineEdit_20.text())
        self.Save_CaseInfo(self.SaveInfo, '矫正胎龄（周）(Correct GA)', '矫正胎龄（周）(Correct GA)', self.lineEdit_21.text())
        self.Save_CaseInfo(self.SaveInfo, '生产方式(Pregnancy', '生产方式(Pregnancy)', self.comboBox_3.currentText())
        self.Save_CaseInfo(self.SaveInfo, '吸氧史(Oxygen)', '吸氧史(Oxygen)', self.comboBox_4.currentText())
        self.Save_CaseInfo(self.SaveInfo, '家族病史(Disease)', '家族病史(Disease)', self.textEdit.toPlainText())
        self.Save_CaseInfo(self.SaveInfo, '出生医院(Birth Hospital)', '出生医院(Birth Hospital)', self.lineEdit_22.text())
        self.Save_CaseInfo(self.SaveInfo, '检查日期(ClinicDate)',     '检查日期(ClinicDate)', self.lineEdit_22.text())
        self.Save_CaseInfo(self.SaveInfo, '照片编号(Photo ID)', '照片编号(Photo ID)', self.lineEdit_12.text())
        self.Save_CaseInfo(self.SaveInfo, '就诊号(Visit ID)', '就诊号(Visit ID)', self.lineEdit_24.text())
        self.Save_CaseInfo(self.SaveInfo, '住院号(HospitalNum)', '住院号(HospitalNum)', self.lineEdit_7.text())
        self.Save_CaseInfo(self.SaveInfo, '籍贯(Native Place)', '籍贯(Native Place)', self.lineEdit_25.text())
        self.Save_CaseInfo(self.SaveInfo, '其他(Other)', '其他(Other)', self.lineEdit_8.text())
        self.my_print(self.lineEdit_5.text())
        if 0 == len(self.lineEdit_5.text()):
            tmp_str = '女'
            nub_str = ' '
            if self.comboBox.currentText() in ['男']:
                tmp_str = '子'
            if len(self.SaveInfo['胎数(Litter Index)'].split(' ')) > 1:
                nub_str = self.SaveInfo['胎数(Litter Index)'].split(' ')[1]
            self.Save_CaseInfo(self.SaveInfo, '患者姓名(Name)', '患者姓名(Name)','{0} {1} {2}'.format(self.lineEdit.text(), tmp_str, nub_str))
        # self.SaveInfo = sorted(self.SaveInfo.items(), key=lambda item: item[0])
        self.my_print(self.SaveInfo)

    #3 5 6 15 20 0
    def Check_EditCase(self):
        result = True
        if 0 == len(self.lineEdit_3.text()):
            self.lineEdit_3.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        # if 0 == len(self.lineEdit_5.text()):
        #      # self.lineEdit_5.setStyleSheet("background-color:rgb(255, 170, 255)")
        #
        #      self.lineEdit_5.setText()
        #     result = False
        if 0 == len(self.lineEdit.text()):
            self.lineEdit.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        if 0 == len(self.lineEdit_6.text()):
            self.lineEdit_6.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        if 0 == len(self.lineEdit_15.text()):
            self.lineEdit_15.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        if 0 == len(self.lineEdit_20.text()):
            self.lineEdit_20.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        if 0 == len(self.lineEdit_24.text()) and 0 == len(self.lineEdit_7.text()):
            if 0 == len(self.lineEdit_24.text()) :
                self.lineEdit_24.setStyleSheet("background-color:rgb(255, 170, 255)")
            if 0 == len(self.lineEdit_7.text()) :
                self.lineEdit_7.setStyleSheet("background-color:rgb(255, 170, 255)")
            result = False
        return result

    def Save_Case(self):
        #self.SaveInfo.clear()
        self.Get_EditCase()
        #将字典进行排序处理
        # self.my_print('保存结果！')
        result = self.ResortDict(self.SaveInfo)
        # self.my_print(result)
        try:
            temp_file = open(self.Pa_Info_Current_Path, "w", encoding='utf_8')
            for temp_key in result:
                temp_file.writelines("%s\n"%temp_key)
            temp_file.close()
            self.Pa_Info_current_index = self.Pa_Info_current_index + 1
            # recode_path =os.path.split(self.Pa_Info_Current_Path)[0]
            # recode_file_name =os.path.join(recode_path,'check_flag')
            # recode_file     = open(recode_file_name, "w", encoding='utf_8')
            # temp_file.close()
            return True
        except:
            return False


    def ProcEditCase(self):
        self.Pa_Info_current_index = 0
        self.CaseCount = self.Check_Case_Nub(self._dataDir)
        if 0  == self.CaseCount:
            QMessageBox.critical(self, "错误", self.tr('用户选择的路径：%s中找不到任何%s文件!' % (self._dataDir, self.Pa_Info)))
            self.statusBar.showMessage('请确认是否选择案例主目录文件夹路径！')
            return
        self.Pa_Info_path_arry = self.Get_PaInfo_Path(self._dataDir)
        if len(self.Pa_Info_path_arry) == 0:
            QMessageBox.critical(self, "错误", self.tr('用户选择的路径：%s中无信息不全的案例！'% (self._dataDir)))
            return
        self.setFixedSize(1060,500)
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.pushButton_4.setVisible(True)
        self.pushButton_5.setVisible(True)
        self.pushButton.setEnabled(False)
        self.AutoUpload.setEnabled(False)
        self.AllUpLoad.setEnabled(False)
        self.StopService.setEnabled(False)
        self.radioButton_6.setEnabled(False)
        self.MauUpload.setEnabled(False)
        self.progressBar.setVisible(False)
        self.statusBar.showMessage('共计%d个案例需要编辑。'%len(self.Pa_Info_path_arry))
        self.Pa_Info_Current_Path = self.Pa_Info_path_arry[0]
        self.Init_EditCase(self.Pa_Info_Current_Path)
        if len(self.Pa_Info_path_arry) == 1 :
            self.pushButton_4.setEnabled(False)
        else:
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(False)

    #手动进行上传操作
    @pyqtSlot()
    def on_MauUpload_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key]=False
        self._Flag['manuUpLoad'] = True
        self.timeEdit.setEnabled(False)

    @pyqtSlot()
    def on_AutoUpload_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key] = False
        self._Flag['StartService'] = True
        self.timeEdit.setEnabled(True)

    @pyqtSlot()
    def on_AllUpLoad_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key]=False
        self._Flag['allUpLoad'] = True
        self.timeEdit.setEnabled(False)

    @pyqtSlot()
    def on_StopService_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key] = False
        self._Flag['StopService'] =True
        self.timeEdit.setEnabled(False)

    @pyqtSlot()
    #退出按钮
    def on_pushButton_2_clicked(self):
        sys.exit(app.exec_())

    @pyqtSlot()
    #确认按钮
    def on_pushButton_clicked(self):
        if self._Flag.get('StopService'):
            self.StopService_Temp()
        elif self._Flag.get('allUpLoad'):
            self.AllUpLoadProc()
        elif self._Flag.get('manuUpLoad'):
            self.ManHandUpLoad()
        elif self._Flag.get('StartService'):
            self.StartService()
        elif self._Flag.get('DeleteService'):
            self.DeleteService_Temp()
        elif self._Flag.get('EditCase'):
            self.ProcEditCase()

    @pyqtSlot()
    # 用户案例按钮
    def on_pushButton_3_clicked(self):
        self._dataDir = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        self.textBrowser.append('案例路径为：' + self._dataDir)
        self.save_path_info()
        self.statusBar.showMessage('用户选择的案例路径为:%s' % self._dataDir)
        self.setFixedSize(441, 484)
        self.pushButton.setVisible(True)
        self.pushButton_2.setVisible(True)
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton.setEnabled(True)
        self.AutoUpload.setEnabled(True)
        self.AllUpLoad.setEnabled(True)
        self.StopService.setEnabled(True)
        self.MauUpload.setEnabled(True)
        self.Pa_Info_current_index = 0

    @pyqtSlot()
    def on_radioButton_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key] = False
        self._Flag['EditCase'] = True
        self.timeEdit.setEnabled(False)

    @pyqtSlot()
    def on_radioButton_6_clicked(self):
        for (key, value) in self._Flag.items():
            self._Flag[key] = False
        self._Flag['DeleteService'] = True
        self.timeEdit.setEnabled(False)

    @pyqtSlot()
    #完成按钮
    def on_pushButton_5_clicked(self):
        if self.Pa_Info_current_index == len(self.Pa_Info_path_arry)-1:
            if True == self.Check_EditCase():
                if self.Save_Case():
                    self.setFixedSize(441, 484)
                    self.pushButton.setVisible(True)
                    self.pushButton_2.setVisible(True)
                    self.pushButton_4.setVisible(False)
                    self.pushButton_5.setVisible(False)
                    self.pushButton.setEnabled(True)
                    self.AutoUpload.setEnabled(True)
                    self.AllUpLoad.setEnabled(True)
                    self.StopService.setEnabled(True)
                    self.MauUpload.setEnabled(True)
                else:
                    self.statusBar.showMessage('保存信息到：%s失败！'%self.Pa_Info_Current_Path)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.lineEdit_5:
                self.statusBar.showMessage('如果新生儿没取名字，可输入XXX子或XXX女')
                # self.lineEdit_5.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_3:
                self.statusBar.showMessage('联系电话必填！')
                self.lineEdit_3.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit:
                self.statusBar.showMessage('母亲姓名必填！')
                self.lineEdit.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_6:
                self.statusBar.showMessage('出生日期必填！')
                self.lineEdit_6.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_15:
                self.statusBar.showMessage('出生体重必填！')
                self.lineEdit_15.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_20:
                self.statusBar.showMessage('出生胎龄必填！')
                self.lineEdit_20.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_24:
                self.statusBar.showMessage('住院号与就诊号不能同时为空！')
                self.lineEdit_24.setStyleSheet("background-color:rgb(255, 255, 255)")
            elif obj == self.lineEdit_7:
                self.statusBar.showMessage('住院号与就诊号不能同时为空！')
                self.lineEdit_7.setStyleSheet("background-color:rgb(255, 255, 255)")
        elif event.type() == QEvent.FocusOut:
                self.statusBar.showMessage('')
        else:
            pass
        return False

    @pyqtSlot()
    # 下一步按钮
    def on_pushButton_4_clicked(self):
        if self.Pa_Info_current_index < len(self.Pa_Info_path_arry) - 1:
            # print(self.Pa_Info_current_index)
            if True == self.Check_EditCase():
                 self.statusBar.showMessage(
                    '共%d个案例，正在处理第%d个案例' % (len(self.Pa_Info_path_arry), self.Pa_Info_current_index + 2))
                 if self.Save_Case():
                     self.Pa_Info_Current_Path = self.Pa_Info_path_arry[self.Pa_Info_current_index]
                     self.Init_EditCase(self.Pa_Info_Current_Path)
                     if self.Pa_Info_current_index == len(self.Pa_Info_path_arry) - 1:
                        self.pushButton_4.setEnabled(False)
                        self.pushButton_5.setEnabled(True)

            else:
                if 0 == self.Pa_Info_current_index:
                    self.statusBar.showMessage('共%d个案例，正在处理第%d个案例' % (len(self.Pa_Info_path_arry), 1))
            # self.setFixedSize(441, 484)
            # self.pushButton.setVisible(True)
            # self.pushButton_2.setVisible(True)
            # self.pushButton_4.setVisible(False)
            # self.pushButton_5.setVisible(False)
            # self.Init_EditCase(self.Pa_Info_path_arry[self.Pa_Info_current_index])
            # if self.Pa_Info_current_index == len(self.Pa_Info_path_arry):
            #    self.pushButton_4.setEnabled(False)

    @pyqtSlot(str)
    def on_comboBox_2_currentIndexChanged(self, p0):
         _translate = QtCore.QCoreApplication.translate
         if  p0 in ['双','三','四']:
             self.groupBox_4.setVisible(True)
         else:
             self.groupBox_4.setVisible(False)
         if p0 =='双':
             self.radioButton_2.setText(_translate("MainWindow", "2-1"))
             self.radioButton_3.setText(_translate("MainWindow", "2-2"))
             self.radioButton_4.setVisible(False)
             self.radioButton_5.setVisible(False)
         elif  p0 =='三':
             self.radioButton_2.setText(_translate("MainWindow", "3-1"))
             self.radioButton_3.setText(_translate("MainWindow", "3-2"))
             self.radioButton_4.setText(_translate("MainWindow", "3-3"))
             self.radioButton_4.setVisible(True)
             self.radioButton_5.setVisible(False)
         elif p0 =='四':
             self.radioButton_2.setText(_translate("MainWindow", "4-1"))
             self.radioButton_3.setText(_translate("MainWindow", "4-2"))
             self.radioButton_4.setText(_translate("MainWindow", "4-3"))
             self.radioButton_5.setText(_translate("MainWindow", "4-4"))
             self.radioButton_4.setVisible(True)
             self.radioButton_5.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow2 = QtWidgets.QMainWindow()
    ui = MainWindow(MainWindow2)
    ui.show()
    sys.exit(app.exec_())
    
