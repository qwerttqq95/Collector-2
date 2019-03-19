import Comm, binascii, UI_main, sys, serial, serial.tools.list_ports, threading, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from traceback import print_exc


class MainWindow(QMainWindow):
    _signal_text = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UI_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.addItem = self.GetSerialNumber()
        self.Sending = Sending()
        while 1:
            if self.addItem == None:
                Warn = QMessageBox.warning(self, '警告', '未检测到串口', QMessageBox.Reset | QMessageBox.Cancel)
                if Warn == QMessageBox.Cancel:
                    self.close()
                if Warn == QMessageBox.Reset:
                    self.addItem = self.GetSerialNumber()
                continue
            else:
                break
        self.addItem.sort()
        for addItem in self.addItem:
            self.ui.comboBox.addItem(addItem)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.ui.pushButton_2.clicked.connect(self.main)
        self.ui.pushButton.clicked.connect(self.open_)
        self._signal_text.connect(self.show_message)

    def main(self):
        self.add = self.ui.lineEdit_2.displayText()
        if self.add == '' or len(self.add) != 12:
            QMessageBox.about(self, 'ERROR', '地址长度错误！')
        else:

            self.Sending.setDaemon(True)
            self.Sending.start()
            self.ui.pushButton_2.disconnect()
            self.ui.pushButton_2.clicked.connect(self.Sending.switch)

    def open_(self):
        file = QFileDialog.getOpenFileName(self, caption='打开文件', directory='C:/Users/Administrator/Desktop/',
                                           filter='Text Files (*.bin)')
        self.ui.lineEdit.setText(file[0])
        self.Sending.open__(file)


    def start_updata(self, add, crc):
        message = '68' + add + '681A00' + '683002' + crc
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器启动升级帧:', Comm.makestr(message))
        send = '发送采集器启动升级帧:' + Comm.makestr(message)
        self._signal_text.emit(send)
        self.sent_time()

    def show_message(self, message):
        self.ui.textEdit.append(message)

    def GetSerialNumber(self):
        SerialNumber = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("The Serial port can't find!")
        else:
            for i in list(port_list):
                SerialNumber.append(i[0])
            return SerialNumber

    def sent_time(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%3d" % (data_head, data_secs)
        MainWindow._signal_text.emit(time_stamp)
        MainWindow._signal_text.emit('--------------------------------')

    def Show_Hidden(self, num):
        if num == '0':
            self.ui.comboBox.setDisabled(0)
            self.ui.comboBox_2.setDisabled(0)
            self.ui.comboBox_3.setDisabled(0)
            self.ui.comboBox_4.setDisabled(0)
        else:
            self.ui.comboBox.setDisabled(1)
            self.ui.comboBox_2.setDisabled(1)
            self.ui.comboBox_3.setDisabled(1)
            self.ui.comboBox_4.setDisabled(1)


class Sending(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__runflag = threading.Event()
        self.serial = serial.Serial()

    def run(self):
        self.__runflag.set()
        while 1:
            if self.__runflag.isSet():
                try:
                    revalue = self.serial_open()
                    print('revalue', revalue)
                    if revalue == 1:
                        print('clear')
                        self.__runflag.clear()
                        MainWindow.ui.pushButton_2.setText('开始')
                        continue
                except:
                    print('ERROR')
                    print_exc(file=open('bug.txt', 'a+'))
                    self.__runflag.clear()
            else:
                self.__runflag.wait()

    def switch(self):
        if self.__runflag.isSet():
            MainWindow.ui.pushButton_2.setText('开始')
            MainWindow.Show_Hidden('0')
            self.__runflag.clear()
        else:
            MainWindow.ui.pushButton_2.setText('关闭')
            MainWindow.Show_Hidden('1')
            self.__runflag.set()

    def serial_open(self):
        self.serial.port = MainWindow.ui.comboBox.currentText()
        self.serial.baudrate = int(MainWindow.ui.comboBox_2.currentText())
        self.serial.parity = MainWindow.ui.comboBox_3.currentText()
        self.serial.stopbits = int(MainWindow.ui.comboBox_4.currentText())
        self.serial.timeout = 1
        self.sending_lenth = MainWindow.ui.comboBox_5.currentText()
        self.add = MainWindow.ui.lineEdit_2.displayText()
        try:
            self.serial.open()
            MainWindow.ui.pushButton_2.setText('停止')
            while self.__runflag.isSet():
                self.reset(self.add)
                time.sleep(0.1)
                num = self.serial.inWaiting()
                data = binascii.b2a_hex(self.serial.read(num))
        except:
            print_exc(file=open('bug.txt', 'a+'))
            return 1

    def reset(self, add):
        message = '68' + add + '681A00'
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器复位帧:', Comm.makestr(message))
        send = '发送采集器复位帧:' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()
        self.serial.write(binascii.a2b_hex(message))
        time.sleep(0.7)
        num = self.serial.inWaiting()
        data = binascii.b2a_hex(self.serial.read(num))
        if data == '':
            self.reset(self.add)
        else:
            try:
                data = Comm.makelist(data)
                while 1:
                    if data[0] == 'ff':
                        data = data[1:]
                    else:
                        break
                if data[0] == '68' and data[-1] == '16':
                    print('Received: ', Comm.list2str(data))
                    Received_data = '收到:\n' + Comm.makestr(Comm.list2str(data))
                    MainWindow._signal_text.emit(Received_data)
                    if data[-3] == '00':
                        print('确认应答帧')
                        return 0
                    else:

            except:
                self.reset(self.add)

    def start_updata(self, add, crc):
        message = '68' + add + '681A00' + '683002' + crc
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器启动升级帧:', Comm.makestr(message))
        send = '发送采集器启动升级帧:' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()

    def sending_message(self, add):
        Flashpage = 8
        offset = 0
        Data = Comm.makelist(self.message[4096:])
        x = 0
        times = len(Data) // 128
        while times:
            Data_ = Comm.list2str(Data[x:x + 128])
            message = '68' + add + '683182' + str(Flashpage) + str(offset) + Data_
            cs = self.CS(Comm.strto0x(Comm.makelist(message)))
            message = message + cs + '16'
            print('发送采集器升级数据帧：', message)
            send = '发送采集器升级数据帧：' + Comm.makestr(message)
            MainWindow._signal_text.emit(send)
            MainWindow.sent_time()
            offset += 1
            if offset == 4:
                Flashpage += 1
                offset = 0
            x = x + 128
            times -= 1

    def CS(self, list):
        sum = 0
        while list:
            sum = sum + ord(list.pop())
        sum = hex(sum & 0xff)[2:]
        if len(sum) == 1:
            sum = "0" + sum
        return sum

    def CRC(self, Value):
        tmpCRC = 0
        i = 0
        while 1:
            if i < len(Value):
                tmpCRC ^= (int(Value[i], 16) << 8)
                tmpCRC = tmpCRC % 65536
                j = 0
                i += 1
                while 1:
                    if j < 8:
                        iflag = tmpCRC & 0x8000
                        tmpCRC <<= 1
                        tmpCRC = tmpCRC % 65536
                        j += 1
                        if iflag:
                            tmpCRC ^= 0x1021
                            tmpCRC = tmpCRC % 65536
                    else:
                        break
            else:
                break
        return hex(tmpCRC)[2:].zfill(4)

    def open__(self,file):
        try:
            with open(file[0], 'rb') as f:
                message = ''
                while 1:
                    c = f.read()
                    ssss = str(binascii.b2a_hex(c))[2:-1]
                    message = message + ssss
                    if not c:
                        break
                old = len(message) // 2
                message_ff = (((len(message) // 2 - 1) // 512) + 1) * 512 - old
                self.message = message + 'ff' * message_ff
                self.CRC16 = self.CRC(Comm.makelist(self.message)[4096:])
                print('CRC16', self.CRC16)
                MainWindow.ui.pushButton_2.setDisabled(0)

        except:
            print_exc(file=open('bug.txt', 'a+'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
