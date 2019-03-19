import Comm, binascii, UI_main, sys, serial, serial.tools.list_ports, threading, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from traceback import print_exc
from PyQt5.QtGui import QIcon

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
        self.setWindowIcon(QIcon('web.png'))

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
        try:
            file = QFileDialog.getOpenFileName(self, caption='打开文件', directory='C:/Users/Administrator/Desktop/',
                                               filter='bin文件 (*.bin)')
            self.ui.lineEdit.setText(file[0])
            with open(file[0], 'rb') as f:
                message = ''
                while 1:
                    c = f.read()
                    ssss = str(binascii.b2a_hex(c))[2:-1]
                    message = message + ssss
                    if not c:
                        break
            self.Sending.open__(message, int(self.ui.comboBox_5.currentText()))
        except:
            pass

    def start_updata(self, add, crc):
        message = '68' + add + '681A00' + '683002' + crc
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器启动升级帧:', Comm.makestr(message))
        send = '发送采集器启动升级帧:\n' + Comm.makestr(message)
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
                self.serial.close()
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
                reValue1 = self.reset(self.add)
                if reValue1 == 0:
                    reValue2 = self.start_updata(self.add, self.CRC16)
                    if reValue2 == 0:
                        reValue3 = self.sending_message(self.add)
                        if reValue3 == 0:
                            reValue4 = self.finish(self.add)
                            if reValue4 == 0:
                                print('升级完成')
                                MainWindow._signal_text.emit('升级完成')
                                MainWindow.sent_time()
                                self.switch()
                            else:
                                print(reValue4, 'ERROR4')
                        else:
                            print(reValue3, 'ERROR3')
                    else:
                        print(reValue2, 'ERROR2')
                else:
                    print(reValue1, 'ERROR1')
                    self.__runflag.clear()
        except:
            print_exc(file=open('bug.txt', 'a+'))
            return 1

    def reset(self, add):
        message = '68' + add + '681A00'
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器复位帧:', Comm.makestr(message))
        send = '发送采集器复位帧:\n' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()
        data = ''
        ageain = 0
        while 1:
            self.serial.write(binascii.a2b_hex(message))
            time.sleep(1)
            num = self.serial.inWaiting()
            data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
            if data == '' and self.__runflag.isSet():
                continue
            else:
                try:
                    if len(data) > 20:
                        data = Comm.makelist(data)
                    else:
                        ageain += 1
                        if ageain == 3:
                            return 1
                        time.sleep(1)
                        continue
                    while 1:
                        if data[0] == 'ff' or data[0] != '68':
                            data = data[1:]
                        else:
                            break
                    if data[0] == '68' and data[-1] == '16':
                        print('Received: ', Comm.list2str(data))
                        Received_data = '收到:\n' + Comm.makestr(Comm.list2str(data))
                        MainWindow._signal_text.emit(Received_data)
                        if data[-3] == '00':
                            print('确认应答')
                            MainWindow._signal_text.emit('确认应答')
                            MainWindow.sent_time()
                            return 0
                        elif data[-3] == '01':
                            print('否认应答')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                        else:
                            print('回应未知')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                except:
                    print_exc(file=open('bug.txt', 'a+'))
                    continue

    def start_updata(self, add, crc):
        message = '68' + add + '683002' + crc
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器启动升级帧:', Comm.makestr(message))
        send = '发送采集器启动升级帧:\n' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()
        data = ''
        while 1:
            self.serial.write(binascii.a2b_hex(message))
            time.sleep(1)
            num = self.serial.inWaiting()
            data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
            if data == '' and self.__runflag.isSet():
                continue
            elif len(data) < 20:
                continue
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
                        if data[-5] == '02':
                            print('确认应答')
                            MainWindow._signal_text.emit('确认应答')
                            return 0
                        elif data[-5] == 'f0':
                            print('否认应答')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                        else:
                            print('回应未知')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                except:
                    print_exc(file=open('bug.txt', 'a+'))

    def sending_message(self, add):
        if int(MainWindow.ui.comboBox_5.currentText()) == 512:
            Flashpage = 8
            offset_ = 4
        else:
            Flashpage = 16
            offset_ = 2
        offset = 0
        Data = Comm.makelist(self.message)[4096:]
        x = 0
        times = len(Data) // 128
        while times:
            text = '共{}帧 '.format(len(Data) // 128) + (' 第{}帧'.format(len(Data) // 128 - times + 1) +
                                                                     '  还需要{}分钟'.format(times // 60) +
                                                                     ('{}秒'.format(times % 60)))
            MainWindow._signal_text.emit(text)
            Data_ = Comm.list2str(Data[x:x + 128])
            new_Flashpage = hex(Flashpage + 51)[2:]
            if len(new_Flashpage) == 1:
                new_Flashpage = '0' + new_Flashpage
            if len(new_Flashpage) == 3:
                new_Flashpage = new_Flashpage[1:]
            new_offset = hex(offset + 51)[2:]
            if len(new_offset) == 1:
                new_offset = '0' + new_offset

            message = '68' + add + '683182' + new_Flashpage + new_offset + Data_
            cs = self.CS(Comm.strto0x(Comm.makelist(message)))
            print('add', add, 'new_Flashpage', new_Flashpage, 'new_offset', new_offset, 'cs', cs)
            message = message + cs + '16'
            print('发送采集器升级数据帧：', Comm.makestr(message))
            send = '发送采集器升级数据帧：\n' + Comm.makestr(message)
            MainWindow._signal_text.emit(send)
            MainWindow.sent_time()
            data = ''
            while 1:
                self.serial.write(binascii.a2b_hex(message))
                time.sleep(1)
                num = self.serial.inWaiting()
                data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
                if data == '' and self.__runflag.isSet():
                    continue
                elif len(data) < 20:
                    data = ''
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
                            if data[8] == 'b1':
                                print('确认应答')
                                MainWindow._signal_text.emit('确认应答')
                                MainWindow.sent_time()
                                break
                            elif data[8] == 'f1':
                                print('否认应答')
                                MainWindow._signal_text.emit('否认应答')
                                return 1
                            else:
                                print('回应未知')
                                MainWindow._signal_text.emit('否认应答')
                                return 1
                    except:
                        print_exc(file=open('bug.txt', 'a+'))
            offset += 1
            if offset == offset_:
                Flashpage += 1
                offset = 0
            x = x + 128
            times -= 1

        return 0

    def finish(self, add):
        message = '68' + add + '683200'
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器升级结束帧:', Comm.makestr(message))
        send = '发送采集器升级结束帧:\n' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()
        data = ''
        while 1:
            self.serial.write(binascii.a2b_hex(message))
            time.sleep(1)
            num = self.serial.inWaiting()
            data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
            if data == '' and self.__runflag.isSet():
                continue
            elif len(data) < 20:
                continue
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
                            print('确认应答')
                            MainWindow._signal_text.emit('确认应答')
                            MainWindow.sent_time()
                            return 0
                        elif data[-3] == '03':
                            print('否认应答')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                        else:
                            print('回应未知')
                            MainWindow._signal_text.emit('否认应答')
                            return 1
                except:
                    print_exc(file=open('bug.txt', 'a+'))

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
        crc = hex(tmpCRC)[2:].zfill(4)
        return hex(int(crc[2:], 16) + 51)[2:] + hex(int(crc[0:2], 16) + 51)[2:]

    def plus33(self, message):
        newstr = ''
        if message is None:
            print('plus33 is none')
        else:
            lenth = len(message)
            new_list = []
            while lenth:
                lenth -= 1
                x = hex(int(message.pop(), 16) + 51)[2:]
                if len(x) == 1:
                    x = '0' + x
                if len(x) == 3:
                    x = x[1:]
                new_list.append(x)
            newstr = Comm.list2str(new_list[::-1])
            return newstr

    def open__(self, message, x):
        try:
            old = len(message) // 2
            message_ff = (((len(message) // 2 - 1) // x) + 1) * x - old
            print('message_ff', message_ff)
            self.message = Comm.makelist(message + ('ff' * message_ff))
            self.CRC16 = self.CRC(self.message[4096:])
            self.message = Comm.list2str(self.plus33(self.message))

            print('CRC16', self.CRC16)
            MainWindow.ui.pushButton_2.setDisabled(0)
        except:
            print_exc(file=open('bug.txt', 'a+'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
