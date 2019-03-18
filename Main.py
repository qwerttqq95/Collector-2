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
            self.reset(self.add)
            self.start_updata(self.add, self.CRC16[2:] + self.CRC16[0:2])
            self.sending_message(self.add)

    def open_(self):
        file = QFileDialog.getOpenFileName(self, caption='打开文件', directory='C:/Users/Administrator/Desktop/',
                                           filter='Text Files (*.bin)')
        self.ui.lineEdit.setText(file[0])
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
                self.ui.pushButton_2.setDisabled(0)

        except:
            print_exc(file=open('bug.txt', 'a+'))

    def reset(self, add):
        message = '68' + add + '681A00'
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器复位帧:', Comm.makestr(message))
        send = '发送采集器复位帧:' + Comm.makestr(message)
        self._signal_text.emit(send)
        self.sent_time()

    def start_updata(self, add, crc):
        message = '68' + add + '681A00' + '683002' + crc
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器启动升级帧:', Comm.makestr(message))
        send = '发送采集器启动升级帧:' + Comm.makestr(message)
        self._signal_text.emit(send)
        self.sent_time()

    def sending_message(self, add):
        Flashpage = 8
        offset = 0
        Data = Comm.makelist(self.message[4096:])
        print('data', Data)
        x = 0
        times = len(Data) // 128
        while times:
            Data_ = Comm.list2str(Data[x:x + 128])
            message = '68' + add + '683182' + str(Flashpage) + str(offset) + Data_
            cs = self.CS(Comm.strto0x(Comm.makelist(message)))
            message = message + cs + '16'
            print('发送采集器升级数据帧：', message)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
