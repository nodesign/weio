#!/usr/bin/env python
# encoding: utf-8

__version__ = "0.01"

import struct
import threading
import Queue
import types
import platform
import glob

import serial

from IoTPy.pyuper.utils import errmsg, IoTPy_APIError
from IoTPy.pyuper.pinouts import UPER1_PINOUT

class IoBoard:
    """
    Uper type board class.

    :param pinout: A list describing physical board pin layout and capabilities. Optional, default is IoPinout.UPER1_PINOUT.
    :type pinout: :class:`IoTPy.pyuper.pinouts.IoPinout`
    :param serial_port: Name of SFP command serial communications port.
    :type serial_port: str
    """

    def __init__(self, pinout=UPER1_PINOUT, serial_port=None):
        """__init__(self, pinout=UPER1_PINOUT, serial_port=None)"""
        ser = None
        if serial_port is None:
            my_platform = platform.system()
            if my_platform == "Windows":
                ports_list = []
                for i in xrange(256):
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

        self.interrupts = [None] * 8
        self.callbackdict = {}

        self.ser = ser
        self.ser.flush()
        self.outq = Queue.Queue()
        self.reader = Reader(self.ser, self.outq, self.internalCallBack, self.decode_sfp)
        #self.reader = Reader(self.ser, self.outq, self.callbackdict, self.decode_sfp)

        self.devicename = "uper"
        self.version = __version__
        self.pinout = pinout

    def get_info(self):
        """
        Get IoBoard device name and version info.

        :return: Tuple containing board name and version.
        """
        return self.devicename, self.version

    def stop(self):
        """
        Stop all communications with the board and close serial communication port.

        :raise: IoTPy_APIError
        """

        #for i in range(7):
        #    self.detachInterrupt(i)
        try:
            self.reader.stop()
            self.ser.flush()
            self.ser.close()
        except:
            raise IoTPy_APIError("UPER API: Serial/USB port disconnected.")

    def _encode_int(self, intarg):
        if intarg < 64:
            return (chr(intarg))
        packedint = struct.pack('>I', intarg).lstrip('\x00')
        return (chr(0xc0 | (len(packedint) - 1)) + packedint)

    def _encode_bytes(self, bytestr):
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
        """
        Construct binary SFP command.

        :param command: SFP command ID.
        :type command: int
        :param args: A list of SFP arguments, which can be either an integer or a byte collection (string).
        :type args: list
        :return: Binary SFP command.
        :rtype: str
        """
        functions = {types.StringType: self._encode_bytes, types.IntType: self._encode_int}
        sfp_command = chr(command) + ''.join(functions[type(arg)](arg) for arg in args)
        sfp_command = '\xd4' + struct.pack('>H', len(sfp_command)) + sfp_command
        return sfp_command

    def decode_sfp(self, buffer):
        """
        Decode SFP command from byte buffer.

        :param buffer: A byte buffer which stores SFP command.
        :type buffer: str
        :return: A list containing decoded SFP function ID and arguments (if any).
        """
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
        """

        :param ret:
        :param output_buf:
        :return:
        """
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

    def internalCallBack(self, interrupt_data):
        """

        :param interrupt_data:
        :return:
        """

        try:
            interrupt_event = { 'id':interrupt_data[0], 'type':interrupt_data[1] & 0xFF, 'values':interrupt_data[1] >> 8 }
            callback_entry = self.callbackdict[self.interrupts[interrupt_event['id']]]
            callback_entry['callback'](interrupt_event, callback_entry['userobject'])
        except:
            raise IoTPy_APIError("UPER API: internal call back problem.")
        return

    def get_device_info(self):
        """
        Return information about the device.

        :return: A list containing board type, major and minor firmware versions, 16 byte unique identifier, microcontroller part and bootcode version numbers.
        """
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
        """
        Perform software restart.
        """
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

        self.irq_available = threading.Condition()
        self.irq_requests = list()

        self.thread_irq = threading.Thread(target=self.interrupt_handler)
        self.thread_irq.start()

        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.decodefun = decodefun

    def interrupt_handler(self):
        with self.irq_available:
            while self.alive:
                self.irq_available.wait(0.05)
                while len(self.irq_requests):
                    interrupt = self.irq_requests.pop(0)
                    try:
                        self.callback(interrupt[1])
                    except:
                        errmsg("UPER API: Interrupt callback error")

        self.alive = False

    def reader(self):
        while self.alive:
            try:
                data = self.serial.read(1)            #read one, blocking
                n = self.serial.inWaiting()           #look if there is more
                if n:
                    data = data + self.serial.read(n)    #and get as much as possible
                if data:
                    if data[3] == '\x08':
                        interrupt = self.decodefun(data)
                        with self.irq_available:
                            self.irq_requests.append(interrupt)
                            self.irq_available.notify()
                    else:
                        self.outq.put(data)
            except:
                errmsg("UPER API: serial port reading error.")
                #raise APIError("Serial port reading error.")
                break
        self.alive = False

    def stop(self):
        if self.alive:
            self.alive = False
            self.thread_irq.join()
            self.thread_read.join()