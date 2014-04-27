import os, glob, urllib, urllib2, time


class Upgrader:

	def __init__(self, reset_pin=22, program_pin=23, fw_file = "/tmp/latest_UPER_firmware.bin"):
		reset_pin_str = str(reset_pin)
		program_pin_str = str(program_pin)
		self._gpio(reset_pin_str, "/sys/class/gpio/export")
		self._gpio(program_pin_str, "/sys/class/gpio/export")
		self._gpio("out","/sys/class/gpio/gpio"+reset_pin_str+"/direction")
		self._gpio("out","/sys/class/gpio/gpio"+program_pin_str+"/direction")
		self.uper_reset = "/sys/class/gpio/gpio"+reset_pin_str+"/value"
		self.uper_program = "/sys/class/gpio/gpio"+program_pin_str+"/value"
		self.fw_file = fw_file

	def _gpio(self, content, file_name):
		try:
			file_id = os.open(file_name, os.O_WRONLY)
			os.write(file_id, content)
			os.close(file_id)
		except OSError:
			pass

	def _reset_uper(self):
		self._gpio("1",self.uper_reset)
		self._gpio("0",self.uper_reset)

	def upgrade_firmware(self, fwUrl = "https://github.com/8devices/UPER/raw/master/dist/UPER-Release.bin"):
		uper_flash_pattern = "CRP DISABLD"

		if not os.path.isfile(self.fw_file):
			# download firmware file
			print "Will get firmware from URL:", fwUrl
			try:
				req = urllib2.Request(fwUrl)
				handle = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print "UPER: Can't download firmware, error code - %s." % e.code
				self._reset_uper()
				return
			except urllib2.URLError:
				print "UPER: Bad URL for firmware file: %s" % fwUrl
				self._reset_uper()
				return
			else:
				urllib.urlretrieve(fwUrl, self.fw_file + '.new')
				if os.path.isfile(self.fw_file + '.new'):
					os.rename(self.fw_file + '.new', self.fw_file)

		# put UPER in to programming mode
		self._gpio("1",self.uper_reset)
		self._gpio("1",self.uper_program)
		self._gpio("0",self.uper_reset)
		time.sleep(2) # wait for linux to settle after UPER reboot in to pgm state
		self._gpio("0",self.uper_program)

		# find UPER block device
		list_block_devs = glob.glob("/sys/block/sd*")
		block_device_name = ''
		header = ''
		for try_device_name in list_block_devs:
			try_device_name = "/dev/" + try_device_name.split('/')[-1]
			try:
				block_device = os.open(try_device_name, os.O_RDWR)
				os.lseek(block_device, 3 * 512, os.SEEK_SET)
				header = os.read(block_device,11)
				time.sleep(0.35) # reading can be slowww
				os.close(block_device)
			except OSError:
				pass
			if header == uper_flash_pattern: # "CRP DISABLD"
				block_device_name = try_device_name # found UPER
				break;
		if block_device_name == '':
			print "UPER firmware upgrade error, no UPER was found."
			return

			#os.system("dd if="+fw_file+" of="+new_dev_list[0]+" seek=4")

		# read the fw from file	
		fw_file_id = open(self.fw_file)
		firmware = fw_file_id.read()
		fw_file_id.close()

		block_device = os.open( block_device_name, os.O_RDWR)
		os.lseek(block_device, 4 * 512, os.SEEK_SET)
		os.write(block_device, firmware)
		os.close(block_device)

		# reset UPER
		self._reset_uper()
		time.sleep(.2)
		return

if __name__ == '__main__':
		#for WeIO up =
		up = Upgrader(17, 22) # GPIO17 = UPER reset, GPIO22 = UPER program
		#up = Upgrader()- carambola2 dev board settings
		up.upgrade_firmware()
