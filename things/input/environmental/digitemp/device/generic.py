from ..utils import *
from ..exceptions import OneWireException, CRCError

__all__ = ['AddressableDevice']


class OneWireDevice(object):
    """
    Abstract 1-Wire device.
    """
    TYPES = {
        0x01: 'DS2401 - Silicon Serial Number',
        0x10: 'DS18S20 - High-precision Digital Termometer',
        0x22: 'DS1822 - Econo Digital Termometer',
        0x28: 'DS18B20 - Programmable Resolution Digital Termometer',
    }

    def __init__(self, bus):
        self.bus = bus

    @classmethod
    def _device_name(cls, family_code):
        return OneWireDevice.TYPES.get(family_code, 'Unknown 1-Wire device')


class AddressableDevice(OneWireDevice):
    """
    Abstract 1-Wire device that has a unique registration number (iButton-like).
    See: http://www.maximintegrated.com/en/app-notes/index.mvp/id/937
    """
    # ---[ ROM Commands ]----

    def _read_ROM(self):
        """
        READ ROM [33h]

        This command can only be used when there is one slave on the bus. It allows the bus master to read the
        slave's 64-bit ROM code without using the Search ROM procedure. If this command is used when there
        is more than one slave present on the bus, a data collision will occur when all the slaves attempt to
        respond at the same time.
        """
        self.bus.reset()
        self.bus.write_byte(0x33)
        rom_code = self.bus.read_bytes(8)
        crc = crc8(rom_code[0:7])
        if crc != iord(rom_code, 7):
            raise CRCError('read_ROM CRC error')
        return rom_code

    def _match_ROM(self, rom_code):
        """
        MATCH ROM [55h]

        The match ROM command allows to address a specific slave device on a multidrop or single-drop bus.
        Only the slave that exactly matches the 64-bit ROM code sequence will respond to the function command
        issued by the master; all other slaves on the bus will wait for a reset pulse.
        """
        self.bus.reset()
        self.bus.write_byte(0x55)
        self.bus.write_bytes(rom_code)

    def _skip_ROM(self):
        """
        The master can use this command to address all devices on the bus simultaneously without sending out
        any ROM code information.
        """
        self.bus.reset()
        self.bus.write_byte(0xcc)

    def _search_ROM(self, alarm=False):
        """
        SEARCH ROM [F0h]
        The master learns the ROM codes through a process of elimination that requires the master to perform
        a Search ROM cycle as many times as necessary to identify all of the slave devices.

        ALARM SEARCH [ECh]
        The operation of this command is identical to the operation of the Search ROM command except that
        only slaves with a set alarm flag will respond.
        """
        complete_roms = []
        partial_roms = []

        def search(current_rom=None):
            if current_rom is None:
                current_rom = []
            else:
                current_rom = current_rom[:]
            # send search command
            self.bus.reset()
            self.bus.write_byte(0xec if alarm else 0xf0)
            # send known bits
            for bit in current_rom:
                self.bus.read_bit()  # skip bitN
                self.bus.read_bit()  # skip complement of bitN
                self.bus.write_bit(bit)
            # read rest of the bits
            for i in range(64 - len(current_rom)):
                b1 = self.bus.read_bit()
                b2 = self.bus.read_bit()
                if b1 != b2:  # all devices have this bit set to 0 or 1
                    current_rom.append(b1)
                    self.bus.write_bit(b1)
                elif b1 == b2 == 0b0:
                    # there are two or more devices on the bus with bit 0 and 1 in this position
                    # save version with 1 as possible rom ...
                    rom = current_rom[:]
                    rom.append(0b1)
                    partial_roms.append(rom)
                    # ... and proceed with 0
                    current_rom.append(0b0)
                    self.bus.write_bit(0b0)
                else:  # b1 == b2 == 1:
                    if alarm:
                        # In alarm search that means there is no more alarming devices
                        return
                    else:
                        raise OneWireException('Search command got wrong bits (two sequential 0b1)')
            complete_roms.append(bits2rom(current_rom))

        search()
        while len(partial_roms):
            search(partial_roms.pop())

        return complete_roms

    # ---[ Helper Functions ]----

    def get_connected_ROMs(self):
        roms = self._search_ROM(alarm=False)
        return [rom2str(rom) for rom in roms]

    def alarm_search(self):
        roms = self._search_ROM(alarm=True)
        return [rom2str(rom) for rom in roms]

    def is_connected(self, rom_code):
        """
        :return: True if a device with the ROM connected to the bus.
        """
        self.bus.reset()
        self.bus.write_byte(0xf0)
        for bit in rom2bits(rom_code):
            b1 = self.bus.read_bit()
            b2 = self.bus.read_bit()
            if b1 == b2 == 0b1:
                return False
            self.bus.write_bit(bit)
        return True
