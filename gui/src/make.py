import  os
if __name__ == '__main__':
    cmd = 'pyinstaller -F -w  -i {0}/1.ico {0}/hospital_upload.py {0}/HospitalUploadProc.py {0}/Ui_upload.py {0}/service_manager.py  --noconsole'.format(os.path.dirname(os.path.realpath(__file__)))
    print(cmd)
    os.system(cmd)
    cmd =  'pyinstaller -F -w  -i {0}/1.ico {0}/hospital_service.py {0}/HospitalUploadProc.py '.format(os.path.dirname(os.path.realpath(__file__)))
    print(cmd)
    os.system(cmd)
    cmd = 'pyinstaller -F -w  -i {0}/1.ico {0}/hospital_monitor.py {0}/service_manager.py '.format(os.path.dirname(os.path.realpath(__file__)))
    print(cmd)
    os.system(cmd)
