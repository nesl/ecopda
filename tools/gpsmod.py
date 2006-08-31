import socket, thread, e32, sys

class gpsModule:
	def __init__(self, gpsAddress):
		self.lat = ""
		self.long = ""
		self.time = ""
		self.lock = thread.allocate_lock()
		self.gpsAddress = '00:08:1B:C1:75:F2'
		self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
		self.target = (self.gpsAddress, 1)
		self.sock.connect(self.target)
		self.threadID = thread.start_new_thread(self.worker, ())

	def generate_checksum(self, data):
        	csum = 0
        	for c in data:
                	csum = csum ^ ord(c)
        	hex_csum = "%02x" % csum
        	return hex_csum.upper()

	def format_time(self, time):
        	hh = time[0:2]
        	mm = time[2:4]
        	ss = time[4:]
        	return "%s:%s:%s UTC" % (hh,mm,ss)

	def format_date(self, date):
        	months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        	dd = date[0:2]
        	mm = date[2:4]
        	yy = date[4:6]
        	yyyy = int(yy) + 2000
        	return "%s %s %d" % (dd, months[(int(mm)-1)], yyyy)

	def readline(self):
        	"""Read one single line from the socket"""
		print "test"
        	line = ""
        	while 1:
			print "test2"
                	char = self.sock.recv(1)
			print "test3"
                	if not char: break
                	line += char
                	if char == "\n": break
        	return line 

	# Get the location from a GGA sentence
	def get_gga_location(self, data):
        	d = data.split(',')
        	ret = {}
        	ret['type'] = 'GGA'
       		ret['lat'] = "%s%s" % (d[1],d[2])
        	ret['long'] = "%s%s" % (d[3],d[4])
        	ret['time'] = format_time(d[0])
        	return ret

	# Get the location from a GLL sentence
	def get_gll_location(self, data):
        	d = data.split(',')
        	ret = {}
        	ret['type'] = 'GLL'
        	ret['lat'] = "%s%s" % (d[0],d[1])
        	ret['long'] = "%s%s" % (d[2],d[3])
        	ret['time'] = format_time(d[4])
        	return ret

	# Get the location from a RMC sentence
	def get_rmc_location(self, data):
        	d = data.split(',')
        	ret = {}
        	ret['type'] = 'RMC'
        	ret['lat'] = "%s%s" % (d[2],d[3])
        	ret['long'] = "%s%s" % (d[4],d[5])
        	ret['time'] = format_time(d[0])
        	return ret

	def worker(self):
		while 1:
			print "1"
			self.lock.acquire() 
			print "2"
		        rawdata = self.readline()
        		if not rawdata: break
			print "3"
        		data = rawdata.strip()			
			print "4"

		        # Ensure it starts with $GP
        		if not data[0:3] == '$GP':
                		continue

			print "3"
		        # If it has a checksum, ensure that's correct
        		# (Checksum follows *, and is XOR of everything from
        		#  the $ to the *, exclusive)
	        	if data[-3] == '*':
        	        	exp_checksum = self.generate_checksum(data[1:-3])
                		if not exp_checksum == data[-2:]:
                        		print "Invalid checksum %s, expecting %s" % (data[-2:], exp_checksum)
                        		continue

		                # Strip the checksum
        		        data = data[:-3]

		        # Grab the parts of the sentence
        		talker = data[1:3]
        		sentence_id = data[3:6]
        		sentence_data = data[7:]

	        	# The NMEA sentences we're interested in are:
        		#  GGA - Global Positioning System Fix Data
        		#  GLL - Geographic Position
	        	#  RMC - GPS Transit Data
        		location = {}
        		if sentence_id == 'GGA':
                		location = self.get_gga_location(sentence_data)

		                # Log GGA packets periodically
        		        gga_log_count = gga_log_count + 1
                		if gga_log_count == gga_log_interval:
                     			gga_log_count = 0
                        		gga_log_fh.write(rawdata)
		 	if sentence_id == 'GLL':
        			        location = self.get_gll_location(sentence_data)
		        if sentence_id == 'RMC':
        	        	location = self.get_rmc_location(sentence_data)

		        # If we got a location, print it
        		if not location == {}:
                		# Check the location is valid
                		if location['lat'] == '0000.0000N' and location['long'] == '0000.0000E':
                        		print "Invalid GPS location found"
	                	else:
					self.type = location['type']
					self.lat = location['lat']
					self.long = location['long']
					self.time = location['time']

        	                	print "Source of location is %s" % location['type']
                	        	print "Lat is %s" % location['lat']
                        		print "Long is %s" % location['long']
                        		print "Time is %s" % location['time']
                		print ""
			self.lock.release()        
			e32.ao_sleep(1)

	def getGPSvalues(self):
		self.lock.acquire()
		(type, lat, long, time) = (self.lat, self.long, self.time)
		self.lock.release()
		return (type, lat, long, time)

