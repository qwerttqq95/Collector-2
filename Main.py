import Comm, binascii

IFLASH_PAGE_SIZE = 0
IFLASH_ADDR = 0


def CS(list):
    sum = 0
    while list:
        sum = sum + ord(list.pop())
    sum = hex(sum & 0xff)[2:]
    if len(sum) == 1:
        sum = "0" + sum
    return sum


def CRC(Value):
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
                    # tmpCRC = tmpCRC % 65535
                    tmpCRC <<= 1
                    tmpCRC = tmpCRC % 65536
                    j += 1
                    if iflag:
                        # tmpCRC = tmpCRC % 65535
                        tmpCRC ^= 0x1021
                        tmpCRC = tmpCRC % 65536
                else:
                    break
        else:
            break
    print('crc', hex(tmpCRC))


def reset(add):
    message = '68' + add + '681A00'
    cs = CS(Comm.strto0x(Comm.makelist(message)))
    message = message + cs + '16'
    print('采集器复位帧:', Comm.makestr(message))


def start(add):
    message = '683002'


def open_():
    file = open('ATSAM3N1BGWN.bin', 'rb')
    message = ''
    while 1:
        c = file.read(1)
        ssss = str(binascii.b2a_hex(c))[2:-1]
        message = message + ssss
        if not c:
            break
    old = len(message) // 2
    message_ff = (((len(message) // 2 - 1) // 512) + 1) * 512 - old
    message = message + 'ff' * message_ff
    print(message, len(message) // 2)
    print(Comm.makelist(message)[4096], 'asddasda')
    CRC16 = CRC(Comm.makelist(message)[4096:])


if __name__ == '__main__':
    add = '000000000001'
    reset(add)
    open_()
