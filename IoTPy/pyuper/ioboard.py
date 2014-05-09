#!/usr/bin/env python
# encoding: utf-8

__version__ = "0.01"

import struct
import types
import platform
import glob

from multiprocessing import Process, Queue

import serial

from IoTPy.pyuper.utils import errmsg, IoTPy_APIError

""" Pin capabilities """
CAP_RESERVED = 0x0
CAP_GPIO     = 0x1
CAP_ADC      = 0x2
CAP_PWM      = 0x4
CAP_SPI      = 0x8

""" UPER1 board pinout """
uper1_pinout = {
1:  [CAP_GPIO,             [0], 	"PIO0_20"],
2:  [CAP_GPIO,             [1], 	"PIO0_2"],
3:  [CAP_GPIO | CAP_PWM,   [2,1,2], "PIO1_26"],
4:  [CAP_GPIO,             [3], 	"PIO1_27"],
5:  [CAP_GPIO | CAP_SPI,   [4,1,2], "PIO1_20"],  #SPI1 SCK
6:  [CAP_RESERVED,					"PIO0_4"],
7:  [CAP_RESERVED,					"PIO0_5"],
8:  [CAP_GPIO | CAP_SPI,   [5,1,1],	"PIO0_21"],  #SPI1 MOSI
9:  [CAP_GPIO,             [6],	    "PIO1_23"],
10: [CAP_GPIO | CAP_PWM,   [7,1,0], "PIO1_24"],
11: [CAP_GPIO,             [8],	    "PIO0_7"],
12: [CAP_GPIO,             [9],	    "PIO1_28"],
13: [CAP_GPIO,             [10],	"PIO1_31"],
14: [CAP_GPIO | CAP_SPI,   [11,1,0],"PIO1_21"],  #SPI1 MISO
15: [CAP_GPIO,             [12],	"PIO0_8"],
16: [CAP_GPIO,             [13],	"PIO0_9"],
17: [CAP_GPIO,             [14],	"PIO0_10"],
18: [CAP_GPIO,             [15],	"PIO1_29"],
19: [CAP_RESERVED],
20: [CAP_RESERVED],
21: [CAP_RESERVED],
22: [CAP_RESERVED],
23: [CAP_GPIO | CAP_ADC,   [33,0],	"PIO1_19"],
24: [CAP_GPIO | CAP_ADC,   [32,1],	"PIO1_25"],
25: [CAP_GPIO | CAP_ADC,   [31,2],	"PIO1_16"],
26: [CAP_GPIO | CAP_ADC,   [30,3],	"PIO0_19"],
27: [CAP_GPIO | CAP_PWM,   [29,0,0],"PIO0_18"],
28: [CAP_GPIO | CAP_PWM,   [28,0,1],"PIO0_17"],
29: [CAP_GPIO,             [27],	"PIO1_15"],
30: [CAP_GPIO | CAP_ADC,   [26,4],	"PIO0_23"],
31: [CAP_GPIO | CAP_ADC,   [25,5],	"PIO0_22"],
32: [CAP_GPIO | CAP_ADC,   [24,6],	"PIO0_16"],
33: [CAP_GPIO | CAP_ADC,   [23,7],	"PIO0_15"],
34: [CAP_GPIO | CAP_PWM,   [22,0,2],"PIO1_22"],
35: [CAP_GPIO,             [21],	"PIO1_14"],
36: [CAP_GPIO,             [20],	"PIO1_13"],
37: [CAP_GPIO,             [19],	"PIO0_14"],
38: [CAP_GPIO,             [18],	"PIO0_13"],
39: [CAP_GPIO | CAP_PWM,   [17,1,1],"PIO0_12"],
40: [CAP_GPIO,             [16],	"PIO0_11"]
}

""" WEIO board pinout """
weio_pinout = {
0 : [CAP_GPIO,             [20],    "PIO1_13"],
1 : [CAP_GPIO,             [19],    "PIO0_14"],
2 : [CAP_GPIO,             [13],    "PIO0_9"],
3 : [CAP_GPIO,             [12],    "PIO0_8"],
4 : [CAP_GPIO,             [14],    "PIO0_10"],
5 : [CAP_GPIO,             [1],     "PIO0_2"],
6 : [CAP_GPIO,             [8],     "PIO0_7"],
7 : [CAP_GPIO,             [21],    "PIO1_14"],
8 : [CAP_GPIO,             [5],     "PIO0_21"],
9 : [CAP_GPIO,             [11],    "PIO1_21"],
10: [CAP_GPIO,             [4],     "PIO1_20"],
11: [CAP_GPIO,             [0],     "PIO0_20"],
12: [CAP_GPIO,             [18],    "PIO0_13"],
13: [CAP_GPIO,             [16],    "PIO0_11"],
14: [CAP_GPIO,             [27],    "PIO1_15"],
15: [CAP_GPIO,             [6],     "PIO1_23"],
16: [CAP_GPIO,             [3],     "PIO1_27"],
17: [CAP_GPIO,             [9],     "PIO1_28"],
18: [CAP_GPIO | CAP_PWM,   [29,0,0],"PIO0_18"],
19: [CAP_GPIO | CAP_PWM,   [28,0,1],"PIO0_17"],
20: [CAP_GPIO | CAP_PWM,   [22,0,2],"PIO1_22"],
21: [CAP_GPIO | CAP_PWM,   [7,1,0], "PIO1_24"],
22: [CAP_GPIO | CAP_PWM,   [17,1,1],"PIO0_12"],
23: [CAP_GPIO | CAP_PWM,   [2,1,2], "PIO1_26"],
24: [CAP_GPIO | CAP_ADC,   [33,0],  "PIO1_19"],
25: [CAP_GPIO | CAP_ADC,   [32,1],  "PIO1_25"],
26: [CAP_GPIO | CAP_ADC,   [31,2],  "PIO1_16"],
27: [CAP_GPIO | CAP_ADC,   [30,3],  "PIO0_19"],
28: [CAP_GPIO | CAP_ADC,   [26,4],  "PIO0_23"],
29: [CAP_GPIO | CAP_ADC,   [25,5],  "PIO0_22"],
30: [CAP_GPIO | CAP_ADC,   [24,6],  "PIO0_16"],
31: [CAP_GPIO | CAP_ADC,   [23,7],  "PIO0_15"]
}

class IoBoard:
    """ low level IO """
    cap_reserved = CAP_RESERVED
    cap_gpio = CAP_GPIO
    cap_adc = CAP_ADC
    cap_pwm = CAP_PWM

    def __init__(self, pinout=weio_pinout, serial_port=None):
        ser = None
        if serial_port is None:
            my_platform = platform.system()
            if my_platform == "Windows":
                ports_list = []
                for i in range(256):
                    try:
                        ser = serial.Serial(i)
                        ports_list.append('COM' + str(i + 1))
                        ser.close()
                    except serial.SerialException:
                        pass
            elif my_platform == "Darwin":
                ports_list = glob.glob("/dev/tty.usbmodem*")
            elif my_platform == "Linux":
                ports_list = glob.glob("/dev/ttyACM*")
        for my_port in ports_list:
            try:
                port_to_try = serial.Serial(
                    port=my_port,
                    baudrate=230400, #virtual com port on USB is always max speed
                    parity=serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.1
                )
                port_to_try.write(self.encode_sfp(255, []))
                uper_response = port_to_try.read(1)    #read one, blocking
                n = port_to_try.inWaiting()        #look if there is more
                if n:
                    uper_response = uper_response + port_to_try.read(n)
                    if self.decode_sfp(uper_response)[0] == -1: # found port with UPER
                        ser = port_to_try
                        break
                port_to_try.close()
            except:
                raise IoTPy_APIError("Unrecoverable serial port error.")
        if not ser:
            raise IoTPy_APIError("No UPER found on USB/serial ports.")

        self.ser = ser
        self.ser.flush()
        #self.outq = Queue.Queue()
        self.outq = Queue()
        self.reader = Reader(self.ser, self.outq, self.internalCallBack, self.decode_sfp)

        self.interrupts = [None] * 8
        self.callbackdict = {}

        self.devicename = "uper"
        self.version = __version__
        self.pinout = pinout

    def get_info(self):
        return self.devicename, self.version

    def stop(self):

        #for i in range(7):
        #    self.detachInterrupt(i)
        try:
            self.reader.stop()
            self.ser.flush()
            self.ser.close()
        except:
            raise IoTPy_APIError("UPER API: Serial/USB port disconnected.")

    def encode_int(self, intarg):
        if intarg < 64:
            return (chr(intarg))
        packedint = struct.pack('>I', intarg).lstrip('\x00')
        return (chr(0xc0 | (len(packedint) - 1)) + packedint)

    def encode_bytes(self, bytestr):
        if len(bytestr) < 64:
            return (chr(0x40 | len(bytestr)) + bytestr)
        packedlen = struct.pack('>I', len(bytestr)).lstrip('\x00')
        if len(packedlen) == 1:
            return ('\xc4' + packedlen + bytestr)
        elif len(packedlen) == 2:
            return ('\xc5' + packedlen + bytestr)
        else:
            raise IoTPy_APIError("UPER API: - too long string passed to UPER, encode_bytes can't handle it.")

    def encode_sfp(self, command, args):
        functions = {types.StringType: self.encode_bytes, types.IntType: self.encode_int}
        sfp_command = chr(command) + ''.join(functions[type(arg)](arg) for arg in args)
        sfp_command = '\xd4' + struct.pack('>H', len(sfp_command)) + sfp_command
        return sfp_command

    def decode_sfp(self, buffer):
        result = []
        if buffer[0:1] != '\xd4':
            return result
        buflen = struct.unpack('>H', buffer[1:3])[0] + 3
        result.append(struct.unpack('b', buffer[3:4])[0])
        pointer = 4
        args = []
        while pointer < buflen:
            argtype = ord(buffer[pointer:pointer + 1])
            pointer += 1
            if argtype < 64:                    #short int
                args.append(argtype)
            elif argtype < 128:                    #short str
                arglen = argtype & 0x3f
                args.append(buffer[pointer:pointer + arglen])
                pointer += arglen
            else:
                arglen = argtype & 0x0f
                if arglen < 4:            #decoding integers
                    if arglen == 0:
                        args.append(ord(buffer[pointer:pointer + 1]))
                    elif arglen == 1:
                        args.append(struct.unpack('>H', buffer[pointer:pointer + 2])[0])
                    elif arglen == 2:
                        args.append(struct.unpack('>I', '\x00' + buffer[pointer:pointer + 3])[0])
                    elif arglen == 3:
                        args.append(struct.unpack('>I', buffer[pointer:pointer + 4])[0])
                    pointer += arglen + 1
                else:
                    if argtype == 0xc4:        #decoding strings
                        arglen = ord(buffer[pointer:pointer + 1])
                    elif argtype == 0xc5:
                        arglen = struct.unpack('>H', buffer[pointer:pointer + 2])[0]
                        pointer += 1
                    else:
                        raise IoTPy_APIError("UPER API: Bad parameter type in decodeSFP method.")
                    pointer += 1
                    args.append(buffer[pointer:pointer + arglen])
                    pointer += arglen
        result.append(args)
        return result

    def uper_io(self, ret, output_buf):
        try:
            self.ser.write(output_buf)
        except:
            raise IoTPy_APIError("Unrecoverable serial port writing error, dying.")
        data = None
        if ret != 0:
            try:
                data = self.outq.get(True, 1)
            except Queue.Empty:
                raise IoTPy_APIError("Nothing to read on serial port exception.")
        return data

    def internalCallBack(self, intdata):
        try:
            self.callbackdict[self.interrupts[intdata[0]]][1]()
        except:
            raise IoTPy_APIError("UPER API: internal call back problem.")
        return

    def get_device_info(self):
        device_info = []
        result = self.decode_sfp(self.uper_io(1, self.encode_sfp(255, [])))
        if result[0] != -1:
            errmsg("UPER error: get_device_info wrong code.")
            raise IoTPy_APIError("")
        result = result[1]
        if result[0] >> 24 != 0x55: # 0x55 == 'U'
            print "UPER error: getDeviceInfo unknown device/firmware type"
            return
        device_info.append("UPER") # type
        device_info.append((result[0] & 0x00ff0000) >> 16) #fw major
        device_info.append(result[0] & 0x0000ffff) #fw minor
        device_info.append(result[1]) # 16 bytes long unique ID from UPER CPU
        device_info.append(result[2]) # UPER LPC CPU part number
        device_info.append(result[3]) # UPER LPC CPU bootload code version
        return device_info

    def get_pin(self, pin_class, pin_no):
        return pin_class(self, pin_no)

    def get_port(self, port_class, port = 0, pins = []):
        return port_class(self, port, pins)

    def reset(self):
        self.uper_io(0, self.encode_sfp(251, []))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

class Reader:
    def __init__(self, serial, outq, callback, decodefun):
        self.serial = serial
        self.outq = outq
        self.callback = callback
        self.alive = True
        #self.thread_read = threading.Thread(target=self.reader)
        #self.thread_read.setDaemon(1)
        #self.thread_read.start()
        self.process_read = Process(target=self.reader, args=(self.alive, self.outq, self.serial, self.callback))
        self.process_read.start()
        self.decodefun = decodefun

    def reader(self, alive, q, serial, callback):
        while alive:
            try:
                data = serial.read(1)            #read one, blocking
                n = serial.inWaiting()           #look if there is more
                if n:
                    data = data + serial.read(n)    #and get as much as possible
                if data:
                    if data[3] == '\x08':
                        interrupt = self.decodefun(data)
                        callback_process = Process(target=callback, args=[interrupt[1]])
                        callback_process.start()
                        #callbackthread = threading.Thread(target=self.callback, args=[interrupt[1]])
                        #callbackthread.start()
                    else:
                        q.put(data)
                        #self.outq.put(data)
            except:
                errmsg("UPER API: serial port reading error.")
                #raise APIError("Serial port reading error.")
                alive = False
                break

    def stop(self):
        if self.alive:
            self.alive = False
            self.process_read.terminate()
            self.process_read.join(0.1)
            #self.thread_read.join()