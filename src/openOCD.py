#!/usr/bin/env python3
import telnetlib as tn
import struct
from time import sleep
import re

class openOCD():
	
	def __init__(self, ip="127.0.0.1", port=4444):
		"""Connect to OpenOCD over telnet. OpenOCD telnet server ip=localhost port=4444"""
		self.ip = ip
		self.port = port
		self.conn = tn.Telnet(self.ip, self.port)

	def __exit__(self):
		"""On program exit, try to close the telnet server socket"""
		try:
			cmd = "exit"
			self.conn.write(cmd.encode("ascii"))
		except  Exception as e:
			print(e)
		finally:
			self.conn.close()

	def parseOutput(self):
		"""Parse lines of output until terminating string"""
		buf = ''
		lines = []
		
		while True:
			buf += self.conn.read_some().decode("ascii") #try to read some bytes from scoket
			parsed = buf.splitlines() #parse out lines
			no_eof = parsed[:-1] #leave off terminator if it is in this data set

			if len(parsed) > 1:
				for l in no_eof:
					if(len(l) > 0):
						lines.append(l) #add line to list
				
				if parsed[-1] == '> ': #last line is terminator
					return lines #return

	def reset(self):
		"""reset the CPU and start running again."""
		self.conn.write("reset run\n")

	def memread(self, addr, count, fmt):
		"""
		Read some bytes of memory from the target
	   	@addr: address to begin read from
	   	@count: number of data elements to read
	   	@fmt: size of elements to read, word, half word, byte
	   	@endianess: endianess of memory
		"""
		cmd = "%s " + str(addr) + " " + str(count) + "\n"
		data = []

		if(fmt == 'w'): #word addressable, 4 bytes
			cmd = cmd % ("mdw")
			self.conn.write(cmd.encode("ascii"))
		elif(fmt == 'h'): #halfword addressable, 2 bytes
			cmd = cmd % ("mdh")
			self.conn.write(cmd.encode("ascii"))
		elif(fmt == 'b'): #byte addressable, 1 byte
			cmd = cmd % ("mdb")
			self.conn.write(cmd.encode("ascii"))
		else:
			print("Error: invalid format!")

		while(data == []):
			data = self.parseOutput()
			data = re.findall(r'0x[0-9]+:(.*)', data[-1])

		return data[0].split()

	def memwrite(self, addr, data, fmt, endianess):
		"""
		Write some bytes of memory from the target
	   	@addr: address to begin read from
	   	@data: data element to write
	   	@fmt: size of elements to write, word, half word, byte
	   	@endianess: endianess of memory
		"""
		cmd = "%s " + str(addr) + " " + "%d " + "\n"
		end_fmt = ''
		offset = 0 #data offset to next element
		length = len(data)
		block = 1 #blocksize in bytes

		if(endianess == 'little'):
			end_fmt = '<'
		elif(endianess == 'big'):
			end_fmt = '>'
		else:
			end_fmt = '@'

		while(offset < length):
			rem = length - offset	

			if(fmt == 'w'):
				block = 4
				arg = end_fmt + 'L'
				d, = struct.unpack_from(arg, data, offset)
				cmd = cmd % ("mww", d)
				self.conn.write(cmd.encode("ascii"))
			elif(fmt == 'h'):
				block = 2
				arg = end_fmt + 'H'
				d, = struct.unpack_from(arg, data, offset)
				cmd = cmd % ("mwh", d)
				self.conn.write(cmd.encode("ascii"))
			elif(fmt == 'b'):
				block = 1
				arg = end_fmt + 'B'
				d, = struct.unpack_from(arg, data, offset)
				cmd = cmd % ("mwb", d)
				self.conn.write(cmd.encode("ascii"))
			else:
				print("Error: invalid format!")
				return		
	
			addr += block #increment address
			offset += block #increment offset

	def io_profile(self, seconds, filename):
		"""Profile access speed by reading the NPC reg over and over"""
		cmd = "profile " + str(seconds) + " " + filename + "\n"
		self.conn.write(cmd.encode("ascii"))

	def halt(self):
		"""Halt the CPU program execution"""
		cmd = "halt\n"
		self.conn.write(cmd.encode("ascii"))

	def resume(self):
		"""Resume normal CPU program execution"""
		cmd = "resume\n"
		self.conn.write(cmd.encode("ascii"))

if __name__ == '__main__':
	ocd = openOCD()
	
	done = False
	halted = False
	
	usage = '''
	Commands:
	profile <seconds> <file name> - performs an I/O profiling test for <seconds> and writes results to <file name> in gmon format.
	halt - Halts the CPU preventing further instruction execution.
	resume - Resumes normal CPU execution.
	memread <address> <count> <format> - Reads <count> data elements from <address>. Format can be word, half word, or byte <w, h, b>.
	memwrite <address> <data> <format> <endianess> - Writes <data> to <address> with the specified endianess <big, little>. Format can be word, half word, or byte <w, h, b>.
	exit - Terminate this program.		
	'''
	
	while not done:
		inp = input("Enter a command")
		inp = inp.split()
		if(inp[0].lower() == "exit"):
			done = True
		elif(inp[0].lower() == "profile"):
			if not halted:
				print("Halting CPU...")
				ocd.halt()
				halted = True
			ocd.profile(inp[1], inp[2])
			sleep(int(inp[1]))
			print("Profiling done!")
		elif(inp[0].lower() == "halt"):
			print("Halting CPU...")
			ocd.halt()
			halted = True
		elif(inp[0].lower() == "resume"):
			print("Resuming execution")
			halted = False
			ocd.resume()
		elif(inp[0].lower() == "memread"):
			if not halted:
				print("Halting CPU...")
				ocd.halt()
				halted = True
			print(ocd.memread(inp[1], inp[2], inp[3]))
		elif(inp.lower() == "memwrite"):
			if not halted:
				print("Halting CPU...")
				ocd.halt()
				halted = True
			memwrite(inp[1], inp[2], inp[3], inp[4])
			print("Write complete.")
		else:
			print(usage)
	
	#data = 0xdeadbeef
	#data = struct.pack("<L", data)
	#ocd.halt();
	#ocd.memwrite(int("0x80000000", 0), data, 'w', 'little')
	#sleep(0.025)
	#print(ocd.memread(int("0x80000000", 0), 2, 'w'))


