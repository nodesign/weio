#!/usr/bin/env python
# encoding: utf-8

__version__ = "0.000000001" # :-)

import struct, serial, threading, Queue, time, types

class Readers:
    def __init__(self, serial, outq, callback, decodefun):
        self.serial = serial
        self.outq = outq
        self.callback = callback
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.decodefun = decodefun

    def reader(self):
        while self.alive:
            try:
                data = self.serial.read(1)            #read one, blocking
                n = self.serial.inWaiting()            #look if there is more
                if n:
                    data = data + self.serial.read(n)    #and get as much as possible
                if data:
                    if data[3] == '\x09':
                        interrupt = self.decodefun(data)
                        self.callback(interrupt)
                    else:
                        #print ":".join("{:02x}".format(ord(c)) for c in data)
                        self.outq.put(data)
            except RuntimeError:
                print "Error!!!"
                break
        self.alive = False
    
    def stop(self):
        if self.alive:
            self.alive = False
            self.thread_read.join()

class UPER:  
    
    def stop(self):
        for i in range(7):
            self.detachInterrupt(i)
        self.reader.stop()
        self.ser.close()

    def encodeINT(self, intarg):
        packedint = struct.pack( '>I', intarg ).lstrip('\x00')
        return (chr(0x80 | len(packedint)) + packedint)

    def encodeBYTES(self, bytestr):
        if len( bytestr ) == 0:
            return('\xa0')
        return('\xa1' + chr(len(bytestr)) + bytestr)

    def encodeSFP(self, command, args):
        functions = { types.StringType : self.encodeBYTES, types.IntType : self.encodeINT }
        SFPcommand = chr(command) + ''.join(functions[ type(arg) ]( arg ) for arg in args)
        SFPcommand = '\xd4' + struct.pack('>H', len(SFPcommand)) + SFPcommand
        return(SFPcommand)

    def decodeSFP(self, buffer):
        result = []
        if buffer[0:1] != '\xd4':
            return( result )
        buflen = struct.unpack('>H', buffer[1:3])[0] + 3
        result.append( struct.unpack('b', buffer[3:4])[0] )
        #print "buflen =", buflen #debug print
        pointer = 4
        args = []
        while pointer < buflen:
            argtype = ord(buffer[pointer:pointer+1])
            #print "argtype = %x" % argtype
            pointer +=1
            if argtype == 0x80:
                args.append( 0 )
            elif argtype & 0x80 == 0x80:
                arglen = argtype & 0x0f
                #print "integer arglen = ", arglen
                if arglen == 1:
                    args.append( ord(buffer[pointer:pointer+1]))
                elif arglen == 2:
                    args.append( struct.unpack('>H', buffer[pointer:pointer+2])[0])
                elif arglen == 3:
                    args.append( struct.unpack('>I', '\x00' + buffer[pointer:pointer+3])[0])
                elif arglen == 4:
                    args.append( struct.unpack('>I', buffer[pointer:pointer+4])[0])
                else:
                    print "bad integer length"
                    return
                pointer += arglen
            elif argtype == 0xa0:
                args.append( '' )
            elif argtype == 0xa1:
                arglen = ord(buffer[pointer:pointer+1])
                pointer += 1
                #print "string arglen =", arglen
                args.append( buffer[pointer:pointer+arglen])
                pointer += arglen
            else:
                print "!! bad arg type, returning"
                break
            #print "loop result", args
        result.append(args)
        return(result)

    def UPER_IO(self, ret, buf):
        #print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #print "UPER1: sending RAW:",
        #print ":".join("{:02x}".format(ord(c)) for c in buf)
        self.ser.write( buf )
        if ret == 0:
            return
        data = self.outq.get() # True, 0.02 )
        #print "UPER1: got RAW data: ",
        #print ":".join("{:02x}".format(ord(c)) for c in data)
        return(data)

    def setPrimary(self, pinID):
        self.UPER_IO(0, self.encodeSFP(1, [pinID]))

    def setSecondary(self, pinID):
        self.UPER_IO(0, self.encodeSFP(2, [pinID]))

    def pinMode(self, pinID, pinMode):
        self.UPER_IO(0, self.encodeSFP(3, [pinID, pinMode]))

    def digitalWrite(self, pinID, value):
        self.UPER_IO(0, self.encodeSFP(4, [pinID, value]))

    def digitalRead(self, pinID):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP( 5, [pinID])))[1][1])

    def attachInterrupt(self, interruptID, pinID, mode):
        self.UPER_IO(0, self.encodeSFP(6, [interruptID, pinID, mode])) 

    def detachInterrupt(self, interruptID):
        self.UPER_IO(0, self.encodeSFP(7, [interruptID])) 

    def analogRead(self, analogPinID):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(10, [analogPinID])))[1][1])
    
    def pwm0_begin(self, period):
        self.UPER_IO(0, self.encodeSFP(50, [period]))     

    def pwm1_begin(self, period):
        self.UPER_IO(0, self.encodeSFP(60, [period])) 

    def pwm0_set(self, channel, high_time):
        self.UPER_IO(0, self.encodeSFP(51, [channel, high_time]))

    def pwm1_set(self, channel, high_time):
        self.UPER_IO(0, self.encodeSFP(61, [channel, high_time]))

    def pwm0_end(self):
        self.UPER_IO(0, self.encodeSFP(52, []))

    def pwm1_end(self):
        self.UPER_IO(0, self.encodeSFP(62, []))

    def spi0_begin(self, divider, mode):
        self.UPER_IO(0, self.encodeSFP(20, [divider, mode]))

    def spi0_trans(self, data, respond):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(21, [data, respond])))[1][0])

    def spi0_end(self):
        self.UPER_IO(0, self.encodeSFP( 22, []))
         
    def i2c_begin(self):
        self.UPER_IO(0, self.encodeSFP(40, []))

    def i2c_trans(self, address, writeData, readLength):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(41, [ address, writeData, readLength]))))

    def i2c_end(self):
        self.UPER_IO(0, self.encodeSFP( 42, []))

    def registerWrite(self, registerAddress, value):
        self.UPER_IO(0, self.encodeSFP(100, [registerAddress, value]))

    def registerRead(self, registerAddress):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(101, [registerAddress])))[1][1])

    def internalCallBack(intdata):
        print"default CallBack is working %r" % intdata
        return

    def __init__(self, callbackfun = internalCallBack, serial_port = "/dev/ttyACM1"):
        self.ser = serial.Serial(
        port=serial_port,
        baudrate=1, #virtual com port on USB is always max speed
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 0.1
        )
        self.ser.flushInput()
        self.outq = Queue.Queue()
        self.callbackfun = callbackfun
        self.reader = Readers(self.ser, self.outq, self.callbackfun, self.decodeSFP)


if __name__ == '__main__':
    print " Will initUper, do ADC read and lit RGB LED in blue for 5 sec using PWM."
    u = UPER()
    u.setSecondary(30)
    print "analogRead = %x" % u.analogRead(3)
    u.attachInterrupt(0,33,4)

    u.setSecondary(22)
    u.pwm0_begin(1000)
    u.pwm0_set(2,0)
    time.sleep(5)
    u.pwm0_set(2,1000)