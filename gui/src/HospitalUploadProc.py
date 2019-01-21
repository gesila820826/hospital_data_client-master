#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 12:09
# @Author  : Zlh
# @Site    : 
# @File    : HospitalUploadProc.py
# @Software: PyCharm
import  time
import  os
import json
import requests
import re
import codecs
import oss2
Key_vaild    = 3
CaseId_vaild = 4
from enum import Enum

#定义返回的枚举类型
class UpLoadResult(Enum):
    Total_Case       =0
    UpLoad_OK        =1
    PaInfo_NotExists =2
    Key_vaild        =3
    CaseId_vaild     =4
    Oss_vaild        =5
    Url_vaild        =6
    FailInfo_Exists  =7
    Proc_Ok          =8
    Proc_Fail        =9
    Oss_return_vaild =10
    Url_return_vaild =11
    Read_Pa_vaild    =12

UpLoadResult_dit = {
        UpLoadResult.Total_Case:[],
        UpLoadResult.UpLoad_OK :[],
        UpLoadResult.PaInfo_NotExists:[],
        UpLoadResult.Key_vaild:[],
        UpLoadResult.CaseId_vaild :[],
        UpLoadResult.Oss_vaild :[],
        UpLoadResult.Url_vaild :[],
        UpLoadResult.FailInfo_Exists :[],
        UpLoadResult.Proc_Ok :[],
        UpLoadResult.Proc_Fail:[],
        UpLoadResult.Oss_return_vaild :[],
        UpLoadResult.Url_return_vaild :[],
        UpLoadResult.Read_Pa_vaild :[],
    }

class HospitalUploadProc():
    def my_print(*args):
        print_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        print(print_time,'[Hospital_AutoUpLoad]','info',*args, file=open(os.path.join("C:/",'service.log'), 'a+', encoding='utf-8'))

    def Read_PatientInfo(self,Patient_info_dic,Patient_info_path,Save_info):
        try:
            #去掉读取文件后出现的\ufeff现象
            lines = open(Patient_info_path, "r",encoding='utf-8-sig').readlines()
            # print(lines)
        except:
            try:
                lines = open(Patient_info_path, "r").readlines()
            except:
                self.my_print('读取文件%s失败！'%Patient_info_path)
                return UpLoadResult.Read_Pa_vaild
        if 'hp_id' in Patient_info_dic.keys():
            #if True == Patient_info_dic['hp_id'][0].isalpha()  and True == Patient_info_dic['hp_id'][1].isalpha() and len(Patient_info_dic['hp_id']) > 9:
                Patient_info_dic['hospital_sn'] = Patient_info_dic['hp_id'][0:5]
                Patient_info_dic['machine_id']  = Patient_info_dic['hp_id'][5:9]
        for temp_string in lines:
            # self.my_print('temp_string:%s'%temp_string)
            temp_info = temp_string.split('=')
            if len(temp_info) != 2:
                continue
            Save_info[temp_info[0]] = temp_info[1].strip('\n')
            rule  = re.compile(r'[(](.*?)[)]', re.S)  # 贪婪匹配
            items = re.findall(rule, temp_info[0])
            if  len(items) > 0:
                key = items[-1:][0]
                if '住院号' not in key:
                    key = key.replace(' ', '')
                Patient_info_dic[key]=temp_info[1].strip('\n')
        # self.my_print(Patient_info_dic)
        return  UpLoadResult.Proc_Ok

    def Check_PatientInfo_Key(self,Pa_Key,Patient_info_dic):
        if Pa_Key not in Patient_info_dic.keys():
            self.my_print('文件内不包含必填字段：%s!'%(Pa_Key))
            return False
        if 0 == len(Patient_info_dic[Pa_Key]):
            self.my_print('文件内必填字段：%s其内容为空' % (Pa_Key))
            return False
        return True

    def Check_PatientInfo(self,Patient_info_Path):
         Patient_info_dic ={}
         Save_info = {}
         result = self.Read_PatientInfo(Patient_info_dic,Patient_info_Path,Save_info)
         if UpLoadResult.Proc_Ok != result:
             return result
         if False == self.Check_PatientInfo_Key('MatherName',Patient_info_dic):
            return  UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('Phone',Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('Birthdate', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('Gender', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('LitterIndex', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('BirthWeight', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('GA', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('Pregnancy', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('Oxygen', Patient_info_dic):
             return UpLoadResult.Key_vaild
         if False == self.Check_PatientInfo_Key('HospitalNum', Patient_info_dic) and False == self.Check_PatientInfo_Key('VisitID', Patient_info_dic):
             return UpLoadResult.Key_vaild
         return UpLoadResult.Proc_Ok

    def Creat_CaseInfo(self,Pa_info,baseurl,Case_Path, hp_id):
        result = False
        ReTry_Time=0
        Patient_info_dic = {}
        Save_info ={}
        Patient_info_dic['hp_id'] = hp_id
        self.my_print('Creat_CaseInfo in %s  baseurl:%s Pa_info:%s'%(Case_Path,baseurl,Pa_info))
        root_images =[]
        temp_arry = []
        for hp_temp in os.listdir(Case_Path):
            dir_path = os.path.join(Case_Path, hp_temp)
            #新增文件信息
            if os.path.isfile(dir_path):
                suffix = dir_path.split('.')[-1:][0]
                self.my_print(dir_path)
                if Pa_info in hp_temp:
                    Patient_info_dic['pa_info'] = '/'.join(['Hospital_data', hp_id, hp_temp])
                    self.Read_PatientInfo(Patient_info_dic,dir_path,Save_info)
                elif suffix in ['jpg','png','bmp','gif','jpeg']:
                    temp_str ='/'.join(['Hospital_data', hp_id,hp_temp])
                    root_images.append(temp_str)
                    Patient_info_dic['root_images'] = root_images
            else:
                for temp in os.listdir(dir_path):
                    suffix = temp.split('.')[-1:][0]
                    if suffix in ['jpg', 'png', 'bmp', 'gif', 'jpeg']:
                        temp_str = '/'.join(['Hospital_data', hp_id, hp_temp, temp])
                        temp_arry.append(temp_str)
                        Patient_info_dic['images'] = temp_arry
                # result = json.dumps(Patient_info_dic,ensure_ascii=False)
                headers = {'Content-Type': 'application/json'}  ## headers中添加上content-type这个参数，指定为json格式

        if len(Patient_info_dic['Name']) == 0:
            tmp_str = '女'
            nub_str = ''
            if Patient_info_dic['Gender'] in ['男']:
                tmp_str = '子'
            if len(Patient_info_dic['LitterIndex'].split(' ')) > 1:
                nub_str = Patient_info_dic['LitterIndex'].split(' ')[1]
            Patient_info_dic['Name'] = '{0} {1} {2}'.format(Patient_info_dic['MatherName'], tmp_str, nub_str)

        temp_result = json.dumps(Patient_info_dic)
        while True:
            if ReTry_Time > 4:
                self.my_print('case_id:%s  requests post 上传数据失败!' % (hp_id))
                return UpLoadResult.Url_vaild
            try:
                temp_url = '{0}/Case/create'.format(baseurl)
                self.my_print('post Pa_info to %s url:%s data:%s' % (baseurl, temp_url,temp_result))
                response = requests.post(url=temp_url, headers=headers, data=temp_result)  ## post的时候，将data字典形
                self.my_print('response.text is %s' % response.text)
                retun_result = json.loads(response.text)
                if retun_result.get('result') == 'fail':
                    error_info = {
                        "case_id": Patient_info_dic.get('hp_id'),
                        'type': '2',
                        'desc': '插入数据失败，原因：%s'%retun_result.get('msg')
                    }
                    response = requests.post(url='{0}/CaseLog/create'.format(baseurl), data=error_info)
                    self.my_print('case_id:%s 插入数据失败! info:%s' % (hp_id, retun_result))
                    result = UpLoadResult.Url_return_vaild
                else:
                    self.my_print('case_id:%s上传数据成功! info:%s' % (hp_id, retun_result))
                    result = UpLoadResult.Proc_Ok
                file1 = codecs.open(os.path.join(Case_Path, 'file_info.txt'), 'w', 'utf-8')  # 将获取到的内容写到文件，以指定的编码方式打开文件，这样才能正常写入中文
                file1.write(temp_result)
                file1.close()
                # if os.path.exists(os.path.join(Case_Path, 'check_flag')):
                #     file1 = codecs.open(os.path.join(Case_Path, 'check_send_flag'), 'w','utf-8')
                #     file1.close()
                return result
            except:
                ReTry_Time = ReTry_Time + 1
                self.my_print('case_id:%s  requests post 上传数据失败! ReTry_Time:%d' % (hp_id, ReTry_Time))
                if hasattr(self, 'trigger'):
                    self.trigger.emit({'info': 'case_id:%s 发送数据至%s失败！重试次数：%d' % (hp_id,baseurl,ReTry_Time)})  # 发送信号

    def oss2_put_singe_file(self,Bucket,bucket_dir,local_file_dir):
        Up_Load_Time = 0
        self.my_print('oss_put file to bucket_dir:%s,Local_path:%s'%(bucket_dir,local_file_dir))
        self._UpLoadCaseCount = self._UpLoadCaseCount+1
        if hasattr(self, 'trigger'):
            self.trigger.emit({'file_count': '%d:%d' %(self._FileCount,self._UpLoadCaseCount) })  # 发送信号
        # QtWidgets.QApplication.processEvents()
        while True:
            if Up_Load_Time > 4:
                self.my_print('oss_put file to bucket_dir:%s,Local_path:%s file:%d' % (bucket_dir, local_file_dir,Up_Load_Time))
                return  UpLoadResult.Oss_vaild
            try:
                result = Bucket.put_object_from_file(bucket_dir,local_file_dir)
                if int(result.status) != int('200'):
                    self.my_print('oss_put file to bucket_dir:%s,Local_path:%s faile result:%s' % (
                        bucket_dir, local_file_dir, result.status))
                    return UpLoadResult.Oss_return_vaild
                else:
                    return UpLoadResult.Proc_Ok
            except:
                Up_Load_Time = Up_Load_Time + 1
                time.sleep(5)
                if hasattr(self, 'trigger'):
                    if self._type == 'manuUpLoad':
                        self.trigger.emit({'info': '文件上传至0SS云端失败！重试%d次' % Up_Load_Time})  # 发送信号
                self.my_print('Bucket.put_object_from_file file to bucket_dir:%s,Local_path:%s time%d' % (
                bucket_dir, local_file_dir, Up_Load_Time))


    def OSS2_Upload(self,DirPath):
        # oss2.resumable_upload(bucket, 'Hospital_data', 'D:\code\hospital_data-master\gui\dist\data\H001C02201812190008\PatientInfo.txt',
        #                       store=oss2.ResumableStore(root='C:/'),
        #                       multipart_threshold=100 * 1024,
        #                       part_size=100 * 1024,
        #                       num_threads=4)
        auth   = oss2.Auth('LTAInP47aO9oWL93', 'yRBFKapTmX0d4u95WD2jNtKdW88F4u')
        bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'exa-hospital')
        hp_id  = os.path.split(DirPath)[1]
        for hp_temp in os.listdir(DirPath):
            dir_path = os.path.join(DirPath,hp_temp)
            if os.path.isfile(dir_path):
                suffix = dir_path.split('.')[-1:][0]
                if 'PatientInfo.txt' in hp_temp or suffix in ['jpg','png','bmp','gif','jpeg']:
                    oss_dir = '/'.join(['Hospital_data',hp_id,hp_temp])
                    result = self.oss2_put_singe_file(bucket, oss_dir, dir_path)
                    if result != UpLoadResult.Proc_Ok :
                        if hasattr(self, 'trigger'):
                                self.trigger.emit({'info':'上传文件%s失败！'%dir_path})  # 发送信号
                        return result
                    else:
                        if hasattr(self, '_type'):
                            if self._type == 'manuUpLoad':
                                self.trigger.emit({'info':'上传文件%s成功！' % dir_path})  # 发送信
            else:
                for temp_file in os.listdir(dir_path):
                    temp_file_dir = os.path.join(dir_path, temp_file)
                    if False == os.path.isfile(temp_file_dir):
                        continue
                    suffix = temp_file.split('.')[-1:][0]
                    if suffix not in ['jpg','png','bmp','gif','jpeg']:
                        continue
                    oss_dir = '/'.join(['Hospital_data',hp_id, hp_temp,temp_file])
                    result = self.oss2_put_singe_file(bucket, oss_dir, temp_file_dir)
                    if result !=  UpLoadResult.Proc_Ok:
                        if hasattr(self, '_type'):
                            if self._type == 'manuUpLoad':
                                self.trigger.emit({'info':'上传文件%s失败!请确认网络是否畅通或防火墙是否关闭！' % temp_file_dir})  # 发送信号
                        return result
                    else:
                        if hasattr(self, '_type'):
                            if self._type == 'manuUpLoad':
                                self.trigger.emit({'info':'上传文件%s成功！' % temp_file_dir})  # 发送信号
        return UpLoadResult.Proc_Ok

    def Check_CaseId(self,hp_id):
        if len(hp_id) not in [20,21]:
            return False
        return True

    def UpLoad_File(self,Pa_info,baseurl,Case_Path,Force_flag):
        Send_Count = 0
        hp_id = os.path.split(Case_Path)[1]
        self.my_print('开始发送case文件：%s!' % Case_Path)
        if False == os.path.exists(os.path.join(Case_Path, 'PatientInfo.txt')):
            if hasattr(self, 'trigger'):
                self.trigger.emit({'info': '%s文件不存在!' % os.path.join(Case_Path, 'PatientInfo.txt')})  # 发送信号
            self.my_print('%s文件不存在!' % '%s文件不存在!' % os.path.join(Case_Path, 'PatientInfo.txt'))
            return UpLoadResult.Pa_vaild
        if False == self.Check_CaseId(hp_id):
            if hasattr(self, 'trigger'):
                self.trigger.emit({'info': 'CASE_ID:%s长度为%d不符合规范，必须为20或21位！' % (hp_id,len(hp_id))})  # 发送信号
            self.my_print('CASE_ID:%s长度为%d不符合规范，必须为20或21位！' % (hp_id,len(hp_id)))
            return UpLoadResult.CaseId_vaild
        result = self.Check_PatientInfo(os.path.join(Case_Path, 'PatientInfo.txt'))
        if UpLoadResult.Proc_Ok != result:
            if hasattr(self, 'trigger'):
                self.trigger.emit({'info': 'CASE:%s信息不全！' % Case_Path})  # 发送信号
            self.my_print('文件%s校验失败!' % Case_Path)
            return result
        if Force_flag == False:
            if os.path.exists(os.path.join(Case_Path, 'file_info.txt')):
                self.my_print('%s:已传送，无需再次发送！' % Case_Path)
                return UpLoadResult.FailInfo_Exists
        # temp_local = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        result = self.OSS2_Upload(Case_Path)
        if UpLoadResult.Proc_Ok != result:
            self.my_print('%s:传送失败!' % Case_Path)
            return result
            # 文件上传失败
            # error_info = {
            #     "case_id": hp_id,
            #     'type': '1',
            #     'desc': '数据上传失败'
            # }
            # Send_Count = 0
            # while True:
            #     if Send_Count > 3:
            #         self.my_print('无法连接至服务器地址：%s' % baseurl)
            #         return False
            #     try:
            #       response = requests.post(url='{0}/CaseLog/create'.format(baseurl), data=error_info)
            #       self.my_print('%s:发送数据上传失败消息成功!' % response.test)
            #     except:
            #       Send_Count=Send_Count+1
            #       self.my_print('%s:发送数据上传失败消息失败!%d' % (Case_Path,Send_Count))

        self.my_print('%s:传送成功!' % Case_Path)
        return result

    def UpLoad_Case(self,Pa_info,baseurl,Case_Path,Force_flag = False):
        #非强制上传，已经上传过的文件不再上传
        result = False
        hp_id = os.path.split(Case_Path)[1]
        # if len(hp_id) != len(def_dirname):
        #     self.my_print('文件夹:%s命名不符合命名规范!，请参考%s' % (Case_Path,def_dirname))
        #     self.trigger.emit({'info': '文件夹:%s命名不符合命名规范,请参考%是,上传文件失败！' % (Case_Path,def_dirname)})  # 发送信号
        #     return False
        result = self.UpLoad_File(Pa_info, baseurl, Case_Path, Force_flag)
        if UpLoadResult.Proc_Ok == result:
            if hasattr(self,'_type'):
                if self._type == 'allUpLoad':
                    self.trigger.emit({'info': '上传CASE:%s成功！'%Case_Path})  # 发送信号
            result = self.Creat_CaseInfo(Pa_info,baseurl,Case_Path,hp_id)
            if hasattr(self, '_type'):
                if self._type == 'allUpLoad':
                    if UpLoadResult.Proc_Ok  == result :
                        self.trigger.emit({'info': '插入CASE:%s记录成功！' % Case_Path})  # 发送信号
                    else:
                        self.trigger.emit({'info': '插入CASE:%s记录失败！' % Case_Path})  # 发送信号
        else:
            if hasattr(self, '_type'):
                if self._type == 'allUpLoad':
                    self.trigger.emit({'info': '上传CASE:%s失败！' % Case_Path})  # 发送信号
        return result


    def Get_File_Nub(self, SingeCase_Path):
        File_Nub = 0
        temp_file_array=[]
        temp_file_array = os.listdir(SingeCase_Path)
        if 'PatientInfo.txt' in temp_file_array:
            for hp_temp in os.listdir(SingeCase_Path):
                temp_dir_path = os.path.join(SingeCase_Path, hp_temp)
                if os.path.isfile(temp_dir_path):
                    File_Nub = File_Nub + 1
                else:
                    File_Nub = File_Nub + len(os.listdir(temp_dir_path))
        return File_Nub

    def Check_Case_Nub(self,Data_Path):
        Case_Nub = 0
        if False == os.path.isdir(Data_Path):
            return Case_Nub
        #不支持路径设置在C盘
        for hp_temp in os.listdir(Data_Path):
            temp_dir_path = os.path.join(Data_Path,hp_temp)
            if os.path.exists(os.path.join(temp_dir_path,self.Pa_Info)):
                Case_Nub = Case_Nub + 1
            # if os.path.isdir(temp_dir_path):
            #     # print(len(hp_temp))
            #     # print(len('HA003C02201812190011'))
            #     # if len(hp_temp) == len(def_dirname):
            #     for file_Temp in os.listdir(temp_dir_path):
            #         if self.Pa_Info in file_Temp:
            #             Case_Nub = Case_Nub + 1
        return Case_Nub


    def Check_PainfoKey_ByDir(self,DirPath):
         case_count =0
         for temp_info in os.listdir(DirPath):
              temp_info_dir =os.path.join(DirPath,temp_info)
              if False != self.Check_CaseId(temp_info):
                  if os.path.exists(os.path.join(temp_info_dir,'PatientInfo.txt')):
                      if UpLoadResult.Key_vaild == self.Check_PatientInfo(os.path.join(temp_info_dir,'PatientInfo.txt')):
                          case_count = case_count+1
         return  case_count

    def Get_PaInfo_Path(self,Case_Path):
        path_info_arry =[]
        for hp_temp in os.listdir(Case_Path):
            temp_dir_path = os.path.join(Case_Path, hp_temp)
            Pa_info_Path  = os.path.join(temp_dir_path,'PatientInfo.txt')
            if False == os.path.exists(Pa_info_Path):
                continue
            if UpLoadResult.Key_vaild == self.Check_PatientInfo(Pa_info_Path):
                path_info_arry.append(Pa_info_Path)
        return path_info_arry

    def Check_CaseIdByDir(self,Case_Path):
        case_vild_list = []
        for hp_temp in os.listdir(Case_Path):
            hp_temp_path = os.path.join(Case_Path,hp_temp)
            if os.path.isdir(hp_temp_path):
                if len(hp_temp) not in [20,21]:
                    case_vild_list.append(hp_temp)
        return case_vild_list

    def PoceResultItem(self,tempDict,tempKey,Key_string,):
        if tempKey in tempDict.keys():
            if isinstance(tempDict[tempKey],list):
               if len(tempDict[tempKey]):
                   return '%s:%d '%(Key_string, len(tempDict[tempKey]))
        return ''

    def PraceResult(self,ResultInfo):
        Temp_string = ''
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Total_Case,'病例总计')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Proc_Ok,   '上传信息成功')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Key_vaild, '信息不全')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.PaInfo_NotExists, '病例文件缺失')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.CaseId_vaild, '病例ID错误')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Oss_vaild, 'OSS云端无法连接')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Url_vaild, 'Url无法连接')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.FailInfo_Exists, '已上传无需再传')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Oss_return_vaild, 'OSS云端返回错误')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Url_return_vaild, 'Url插入案例失败')
        Temp_string = Temp_string +self.PoceResultItem(ResultInfo, UpLoadResult.Read_Pa_vaild, '读取病人信息文件失败')
        return Temp_string


    def TrancKey(self,tempstr):
        if 'UpLoadResult.Total_Case' == tempstr:
            return UpLoadResult.Total_Case
        if 'UpLoadResult.Proc_Ok' == tempstr:
            return UpLoadResult.Proc_Ok
        if 'UpLoadResult.Key_vaild' == tempstr:
            return UpLoadResult.Key_vaild
        if 'UpLoadResult.CaseId_vaild' == tempstr:
            return UpLoadResult.CaseId_vaild
        if 'UpLoadResult.Oss_vaild' == tempstr:
            return UpLoadResult.Oss_vaild
        if 'UpLoadResult.Url_vaild' == tempstr:
            return UpLoadResult.Url_vaild
        if 'UpLoadResult.FailInfo_Exists' == tempstr:
            return UpLoadResult.FailInfo_Exists
        if 'UpLoadResult.Oss_return_vaild' == tempstr:
            return UpLoadResult.Oss_return_vaild
        if 'UpLoadResult.Url_return_vaild' == tempstr:
            return UpLoadResult.Url_return_vaild
        if 'UpLoadResult.Read_Pa_vaild' == tempstr:
            return UpLoadResult.Read_Pa_vaild
        return  None

    def ReadResultInfo(self,resultInfoPath):
        Temp_string = ''
        if False == os.path.exists(resultInfoPath):
            return Temp_string
        lines  = open(resultInfoPath, 'r').readlines()# 打开文件
        last_line = lines[-1]  # 取最后一行
        last_line = last_line.strip('\n')
        temp_dict = json.loads(last_line)
        result_dict ={}
        for temp_key  in temp_dict:
            result = self.TrancKey(temp_key)
            if None != result:
                result_dict[result] =temp_dict[temp_key]
        Temp_string = '最近一次后台上传时间:%s\n'%temp_dict.get('Send_time')+ self.PraceResult(result_dict)
        return Temp_string

        # temp_dict = json.loads(line)

    def ResortDict(self,ResultDict):
        KeyList = [
            '编号(ID)',
            '患者姓名(Name)',
            '患者性别(Gender)',
            '出生日期(Birthdate)',
            '年龄(Age)',
            '患者电话(Phone)',
            '出生胎龄（周）(GA)',
            '出生体重（kg）(BirthWeight)',
            '科室(Department)',
            '住院号(HospitalNum)',
            '首次就诊日期(FirstVisitDate)',
            '主诊医生(Doctor)',
            '上次就诊日期(LastVisitDate)',
            '检查日期(ClinicDate)',
            '检查时间(ClinicTime)',
            '母亲姓名(Mather Name)',
            '母亲身份证号(Mather ID)',
            '家庭地址(Home Address)',
            '身份证号(Self Id)',
            '胎数(Litter Index)',
            '矫正胎龄（周）(Correct GA)',
            '生产方式(Pregnancy)',
            '吸氧史(Oxygen)',
            '家族病史(Disease)',
            '出生医院(Birth Hospital)',
            '照片编号(Photo ID)',
            '就诊号(Visit ID)',
            '籍贯(Native Place)',
            '其他(Other)'
        ]
        Key_list    = []
        result_list = []
        for temp_item in KeyList:
             for TempKey in ResultDict.keys():
                if temp_item in TempKey:
                    result_list.append('%s=%s' % (temp_item, ResultDict[TempKey]))
                    Key_list.append(TempKey)
        for temp_key in Key_list:
            ResultDict.pop(temp_key)
        for temp in ResultDict.keys():
            result_list.append('%s=%s'%(temp,ResultDict[temp]))
        return result_list
