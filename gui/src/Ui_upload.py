# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\code\hospital_data-master\gui\upload.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 500)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 421, 421))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 401, 311))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 381, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(10, 283, 391, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.timeEdit = QtWidgets.QTimeEdit(self.frame)
        self.timeEdit.setGeometry(QtCore.QRect(320, 10, 91, 21))
        self.timeEdit.setObjectName("timeEdit")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(240, 10, 91, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 10, 61, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 40, 401, 61))
        self.groupBox_3.setObjectName("groupBox_3")
        self.MauUpload = QtWidgets.QRadioButton(self.groupBox_3)
        self.MauUpload.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.MauUpload.setObjectName("MauUpload")
        self.AutoUpload = QtWidgets.QRadioButton(self.groupBox_3)
        self.AutoUpload.setGeometry(QtCore.QRect(150, 20, 71, 16))
        self.AutoUpload.setObjectName("AutoUpload")
        self.AllUpLoad = QtWidgets.QRadioButton(self.groupBox_3)
        self.AllUpLoad.setGeometry(QtCore.QRect(10, 40, 89, 16))
        self.AllUpLoad.setObjectName("AllUpLoad")
        self.StopService = QtWidgets.QRadioButton(self.groupBox_3)
        self.StopService.setGeometry(QtCore.QRect(150, 40, 71, 16))
        self.StopService.setObjectName("StopService")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setGeometry(QtCore.QRect(280, 40, 89, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_6.setGeometry(QtCore.QRect(280, 20, 89, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 440, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 440, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(440, 10, 611, 411))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 331, 381))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 13, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 8, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 10, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.gridLayout.addWidget(self.lineEdit_15, 10, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout.addWidget(self.lineEdit_11, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 4, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 8, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 7, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 11, 0, 1, 1)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.gridLayout.addWidget(self.lineEdit_20, 11, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 12, 0, 1, 1)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.gridLayout.addWidget(self.lineEdit_21, 12, 1, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 6, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 7, 1, 1, 1)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.gridLayout.addWidget(self.lineEdit_22, 13, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 10, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_3.setGeometry(QtCore.QRect(60, 10, 89, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_4.setGeometry(QtCore.QRect(120, 10, 89, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_5.setGeometry(QtCore.QRect(180, 10, 89, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_2.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 9, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(350, 20, 251, 391))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_25 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 7, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_3.addWidget(self.textEdit, 12, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_29.setObjectName("label_29")
        self.gridLayout_3.addWidget(self.label_29, 1, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 0, 0, 1, 1)
        self.lineEdit_24 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.gridLayout_3.addWidget(self.lineEdit_24, 9, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 12, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_3, 0, 1, 1, 1)
        self.lineEdit_25 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.gridLayout_3.addWidget(self.lineEdit_25, 10, 1, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_4, 1, 1, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout_3.addWidget(self.lineEdit_12, 7, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 10, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_26.setObjectName("label_26")
        self.gridLayout_3.addWidget(self.label_26, 9, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_17.setText("")
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 13, 0, 1, 1)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.gridLayout_3.addWidget(self.lineEdit_19, 6, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_24.setObjectName("label_24")
        self.gridLayout_3.addWidget(self.label_24, 6, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 8, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_3.addWidget(self.lineEdit_7, 8, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 11, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_3.addWidget(self.lineEdit_8, 11, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 440, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 440, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "案例上传工具"))
        self.groupBox_2.setTitle(_translate("MainWindow", "输出日志："))
        self.label_3.setText(_translate("MainWindow", "脚本运行时间："))
        self.pushButton_3.setText(_translate("MainWindow", "案例路径"))
        self.groupBox_3.setTitle(_translate("MainWindow", "文件操作："))
        self.MauUpload.setText(_translate("MainWindow", "手动上传"))
        self.AutoUpload.setText(_translate("MainWindow", "定时上传"))
        self.AllUpLoad.setText(_translate("MainWindow", "全部上传"))
        self.StopService.setText(_translate("MainWindow", "停止服务"))
        self.radioButton.setText(_translate("MainWindow", "编辑案例"))
        self.radioButton_6.setText(_translate("MainWindow", "删除服务"))
        self.pushButton.setText(_translate("MainWindow", "确认"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))
        self.groupBox.setTitle(_translate("MainWindow", "录入信息："))
        self.label_23.setText(_translate("MainWindow", "出生医院"))
        self.label_15.setText(_translate("MainWindow", "*胎数"))
        self.label_16.setText(_translate("MainWindow", "*出生体重"))
        self.label_2.setText(_translate("MainWindow", "*母亲姓名"))
        self.label_4.setText(_translate("MainWindow", "*联系电话"))
        self.label.setText(_translate("MainWindow", "母亲身份证号码"))
        self.label_13.setText(_translate("MainWindow", "*出生日期"))
        self.label_5.setText(_translate("MainWindow", "家庭地址"))
        self.label_6.setText(_translate("MainWindow", "*姓名"))
        self.label_12.setText(_translate("MainWindow", "身份证号码"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "单"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "双"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "三"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "四"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "其他"))
        self.label_14.setText(_translate("MainWindow", "*性别"))
        self.label_21.setText(_translate("MainWindow", "*出生胎龄"))
        self.label_31.setText(_translate("MainWindow", "矫正胎龄(周天)"))
        self.comboBox.setItemText(0, _translate("MainWindow", "男"))
        self.comboBox.setItemText(1, _translate("MainWindow", "女"))
        self.radioButton_2.setText(_translate("MainWindow", "1"))
        self.radioButton_3.setText(_translate("MainWindow", "2"))
        self.radioButton_4.setText(_translate("MainWindow", "3"))
        self.radioButton_5.setText(_translate("MainWindow", "4"))
        self.label_25.setText(_translate("MainWindow", "照片编号"))
        self.label_29.setText(_translate("MainWindow", "*吸氧史"))
        self.label_19.setText(_translate("MainWindow", "*生产方式"))
        self.label_22.setText(_translate("MainWindow", "家族病史"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "阴道产"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "剖宫产"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "无"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "有"))
        self.label_27.setText(_translate("MainWindow", "籍贯"))
        self.label_26.setText(_translate("MainWindow", "就诊号"))
        self.label_24.setText(_translate("MainWindow", "检查日期"))
        self.label_7.setText(_translate("MainWindow", "住院号"))
        self.label_8.setText(_translate("MainWindow", "其他"))
        self.pushButton_4.setText(_translate("MainWindow", "下一个"))
        self.pushButton_5.setText(_translate("MainWindow", "完成"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

