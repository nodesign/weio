#!/usr/bin/env python
# encoding: utf-8

import struct
import types
import glob
import subprocess
import os

import serial

class detectFW:
    def __init__(self):
        pass

    def detector(self):
        ser = None
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
                return False
        if not ser:
            return False

        return True

    def _encode_int(self, intarg):
        if intarg < 64:
            return chr(intarg)
        packedint = struct.pack('>I', intarg).lstrip('\x00')
        return chr(0xc0 | (len(packedint) - 1)) + packedint

    def _encode_bytes(self, bytestr):
        if len(bytestr) < 64:
            return chr(0x40 | len(bytestr)) + bytestr
        packedlen = struct.pack('>I', len(bytestr)).lstrip('\x00')
        if len(packedlen) == 1:
            return '\xc4' + packedlen + bytestr
        elif len(packedlen) == 2:
            return '\xc5' + packedlen + bytestr

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
        functions = {
            types.StringType: self._encode_bytes,
            bytearray: self._encode_bytes,
            types.IntType: self._encode_int
        }
        sfp_command = chr(command) + ''.join(str(functions[type(arg)](arg)) for arg in args)
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
            if argtype < 64:                    # short int
                args.append(argtype)
            elif argtype < 128:                    # short str
                arglen = argtype & 0x3f
                args.append(buffer[pointer:pointer + arglen])
                pointer += arglen
            else:
                arglen = argtype & 0x0f
                if arglen < 4:            # decoding integers
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
                    if argtype == 0xc4:        # decoding strings
                        arglen = ord(buffer[pointer:pointer + 1])
                    elif argtype == 0xc5:
                        arglen = struct.unpack('>H', buffer[pointer:pointer + 2])[0]
                        pointer += 1
                    pointer += 1
                    args.append(buffer[pointer:pointer + arglen])
                    pointer += arglen
        result.append(args)
        return result

if __name__ == "__main__":
    ### Detect the LPC
    fw = detectFW()
    res = fw.detector()

    if not res:
        '''
        weioRunner.py, just before ioloop.start(), send a command to stop the led_blink init script.
        The command will 'killall ledBlink.py'.
        To avoid weioRunner to kill this process, ledBlink.py is symlinked with a different name
	    '''
        if not os.path.islink("/weio/scripts/ledBlinkSanity.py"): 
            os.symlink("/weio/scripts/ledBlink.py", "/weio/scripts/ledBlinkSanity.py")
        print "LPC not found !"
        subprocess.Popen(["/weio/scripts/ledBlinkSanity.py", '0.1'])
    else:
        print "LPC found with a functionnal firmware"
