#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 10:28
# @Author  : Zlh
# @Site    : 
# @File    : service_manager.py
# @Software: PyCharm
import win32serviceutil
import win32service
import win32event
import winerror
import datetime
import time
class ServiceManager(object):
    """管理window服务"""
    def __init__(self, name):
        """
        name: 服务的名称
        """
        self.name = name
        # 启动或停止服务时等待操作成功等待时间
        self.wait_time = 0.5
        # 启动或停止服务时最大等待时间，超过时返回超时提示
        self.delay_time = 15
        self.scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        if self.is_exists():
            try:
                self.handle = win32service.OpenService(self.scm, self.name, win32service.SC_MANAGER_ALL_ACCESS)
            except Exception as  e:
                self.log(e)
        else:
            print( '服务%s没有安装'% self.name)

    def is_stop(self):
        """检查服务是否停止"""
        flag = False
        try:
            if self.handle:
                ret = win32service.QueryServiceStatus(self.handle)
                flag = ret[1] != win32service.SERVICE_RUNNING
        except Exception as e:
            self.log(e)
        return flag

    def start(self):
        """开启服务"""
        try:
            if self.handle:
                win32service.StartService(self.handle, None)
        except Exception as e:
            self.log(e)
        status_info = win32service.QueryServiceStatus(self.handle)
        if status_info[1] == win32service.SERVICE_RUNNING:
            return '启动服务%s成功'% self.name
        elif status_info[1] == win32service.SERVICE_START_PENDING:
            # 如果服务正在启动中则延迟返回启动信息，直到启动成功,或返回启动时间过长信息
            start_time = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - start_time).seconds > self.delay_time:
                    return '启动服务%s时间太长'% self.name
                time.sleep(self.wait_time)
                if win32service.QueryServiceStatus(self.handle)[1] == win32service.SERVICE_RUNNING:
                    return '启动服务%s成功' % self.name
        else:
            return '启动服务%s失败'%self.name

    def stop(self):
        """停止服务"""
        try:
            status_info = win32service.ControlService(self.handle, win32service.SERVICE_CONTROL_STOP)
        except Exception as e:
            return e
        if status_info[1] == win32service.SERVICE_STOPPED:
            return '停止服务%s成功!'% self.name
        elif status_info[1] == win32service.SERVICE_STOP_PENDING:
            start_time = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - start_time).seconds > self.delay_time:
                    return '停止服务%s时间太长!'% self.name
                time.sleep(self.wait_time)
                if win32service.QueryServiceStatus(self.handle)[1] == win32service.SERVICE_STOPPED:
                    return '停止服务%s成功!' % self.name
        else:
            return '停止服务%s失败!'% self.name

    def restart(self):
        """重启服务"""
        try:
            self.handle = win32service.OpenService(self.scm, self.name, win32service.SC_MANAGER_ALL_ACCESS)
        except Exception as  e:
            self.log(e)

        if not self.is_stop():
            self.stop()
        self.start()
        return win32service.QueryServiceStatus(self.handle)

    def status(self):
        """获取运行的状态"""
        try:
            status_info = win32service.QueryServiceStatus(self.handle)
            status = status_info[1]
            if status == win32service.SERVICE_STOPPED:
                return "STOPPED"
            elif status == win32service.SERVICE_START_PENDING:
                return "STARTING"
            elif status == win32service.SERVICE_STOP_PENDING:
                return "STOPPING"
            elif status == win32service.SERVICE_RUNNING:
                return "RUNNING"
        except Exception as  e:
            self.log(e)
            return e

    def close(self):
        """释放资源"""
        try:
            if self.scm:
                win32service.CloseServiceHandle(self.handle)
                win32service.CloseServiceHandle(self.scm)
        except Exception as e:
            self.log(e)

    def is_exists(self):
        """windows服务是否已安装"""
        statuses = win32service.EnumServicesStatus(self.scm, win32service.SERVICE_WIN32, win32service.SERVICE_STATE_ALL)
        for (short_name, desc, status) in statuses:
            if short_name == self.name:
                return True
        return False

    def log(self, exception):
        print(exception)