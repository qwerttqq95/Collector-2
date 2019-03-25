import Comm, binascii, UI_main_new, sys, serial, serial.tools.list_ports, threading, time, ctypes, inspect
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QPushButton, QHeaderView, \
    QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, Qt
from traceback import print_exc
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    _signal_text = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UI_main_new.Ui_MainWindow()
        self.ui.setupUi(self)
        self.addItem = self.GetSerialNumber()
        self.setWindowTitle('I型采集器升级软件V1.1')
        while 1:
            if self.addItem == None:
                Warn = QMessageBox.warning(self, '警告', '未检测到串口', QMessageBox.Reset | QMessageBox.Cancel)
                if Warn == QMessageBox.Cancel:
                    self.close()
                    sys.exit()
                if Warn == QMessageBox.Reset:
                    self.addItem = self.GetSerialNumber()
                continue
            else:
                break
        self.addItem.sort()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.ui.pushButton.clicked.connect(self.open_)
        self._signal_text.connect(self.show_message)
        self
        self.setWindowIcon(QIcon('upgrade.ico'))
        self.add_button()
        self.list = {}
        self.ui.tableWidget.setDisabled(1)
        self.ui.pushButton_2.clicked.connect(self.showall)

    def showall(self):
        if self.ui.pushButton_2.text() == '全部开始':
            self.ui.pushButton_2.setText('全部关闭')
        else:
            self.ui.pushButton_2.setText('全部开始')

    def plus33(self, message):
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
            x = int(self.ui.comboBox_5.currentText())
            old = len(message) // 2
            message_ff = (((len(message) // 2 - 1) // x) + 1) * x - old
            print('message_ff', message_ff)
            self.message = Comm.makelist(message + ('ff' * message_ff))
            self.CRC16 = self.CRC(self.message[4096:])
            self.message = Comm.list2str(self.plus33(self.message))
            print('CRC16', self.CRC16)
            self.ui.tableWidget.setDisabled(0)
            self.ui.pushButton_2.setDisabled(0)

        except:
            print_exc(file=open('bug.txt', 'a+'))

    def show_message(self, message):
        f = open('log', 'a+', encoding='utf-8')
        f.write(message)
        f.close()

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
        MainWindow._signal_text.emit(time_stamp + '\n')

    def Show_Hidden(self, num):
        if num == '0':
            self.ui.comboBox_2.setDisabled(0)
            self.ui.comboBox_3.setDisabled(0)
            self.ui.comboBox_4.setDisabled(0)
        else:
            self.ui.comboBox_2.setDisabled(1)
            self.ui.comboBox_3.setDisabled(1)
            self.ui.comboBox_4.setDisabled(1)

    def add_button(self):
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        for x in range(len(self.addItem)):
            self.ui.tableWidget.insertRow(x)
            self.ui.tableWidget.setItem(x, 0, QTableWidgetItem(self.addItem[x]))
            self.ui.tableWidget.setCellWidget(x, 1, self.start_button(x))
            self.ui.tableWidget.setItem(x,2,QTableWidgetItem(''))

    def progress(self, position, text):
        self.ui.tableWidget.item(position, 2).setText(text)

    def start_button(self, id):
        star_button = QPushButton('开始')
        star_button.clicked.connect(lambda: self.start_(id))
        self.ui.pushButton_2.clicked.connect(star_button.click)
        return star_button

    def start_(self, id_):
        try:
            serial_ = serial.Serial()
            serial_.port = self.addItem[id_]
            print(self.addItem[id_])
            serial_.baudrate = int(MainWindow.ui.comboBox_2.currentText())
            serial_.parity = MainWindow.ui.comboBox_3.currentText()
            serial_.stopbits = int(MainWindow.ui.comboBox_4.currentText())
            serial_.timeout = 1
            self.sending_lenth = MainWindow.ui.comboBox_5.currentText()
            button = self.sender()
            if button.text() == '开始':
                serial_.open()
                button.setText('停止')
                new_thread = new_sending(id_, serial_, self.message, self.CRC16)
                new_thread.setDaemon(True)
                new_thread.start()
                a = new_thread.ident
                self.list.update({id_: a})
            else:
                button.setText('开始')
                serial_.close()
                ident = self.list.get(id_)
                _async_raise(ident, SystemExit)

        except:
            print_exc(file=open('bug.txt', 'a+'))


class new_sending(threading.Thread):
    def __init__(self, id, port, message, crc16):
        threading.Thread.__init__(self)
        self.id = int(id)
        self.serial = port
        self.add = MainWindow.ui.lineEdit_2.text()
        self.message = message
        self.CRC16 = crc16

    def run(self):
        try:
            while 1:
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
                                break
                            else:
                                print(reValue4, 'ERROR4')
                                break
                        else:
                            print(reValue3, 'ERROR3')
                            break
                    else:
                        print(reValue2, 'ERROR2')
                        break
                else:
                    print(reValue1, 'ERROR1')
                    break
        except:
            print_exc(file=open('bug.txt', 'a+'))

    def reset(self, add):
        message = '68' + add + '681A00'
        cs = self.CS(Comm.strto0x(Comm.makelist(message)))
        message = message + cs + '16'
        print('发送采集器复位帧:', Comm.makestr(message))
        send = '发送采集器复位帧:\n' + Comm.makestr(message)
        MainWindow._signal_text.emit(send)
        MainWindow.sent_time()
        ageain = 0
        while 1:
            self.serial.write(binascii.a2b_hex(message))
            time.sleep(1)
            num = self.serial.inWaiting()
            data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
            if data == '':
                continue
            else:
                try:
                    if len(data) > 20:
                        data = Comm.makelist(data)
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
                    else:
                        ageain += 1
                        if ageain == 3:
                            return 1
                        time.sleep(1)
                        continue


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
        while 1:
            self.serial.write(binascii.a2b_hex(message))
            time.sleep(1)
            num = self.serial.inWaiting()
            data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
            if data == '':
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
            MainWindow._signal_text.emit(text + '\n')
            MainWindow.progress(self.id, text)
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
            while 1:
                self.serial.write(binascii.a2b_hex(message))
                time.sleep(1)
                num = self.serial.inWaiting()
                data = str(binascii.b2a_hex(self.serial.read(num)))[2:-1]
                if data == '':
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
            if data == '':
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


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
