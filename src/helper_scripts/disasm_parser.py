#! /usr/bin/env python3

import json
import re
import sys

#check if input file is specified
if(len(sys.argv) < 2):
	print("No file specified. Please call as follows:\n./disasm_parser.py <file name>")
	quit()

#grab file name and create json file
filename = sys.argv[1]
json_file = "memmap.json"
jf = open(json_file, 'w+')

#setup json data map
data = {}
data["function"] = []

size = 0
function = ''
first = True

with open(filename) as fp:
	line = fp.readline() #read line
	while line:
		match = re.findall(r'<(.*?)>:', line) #find function label
		size += 1
		if(match != []): #if function label match
			if(first is False): #not first iteration, write data and continue
				data["function"].append({"name":function,"base":base,"size":size-3}) #decrement size by 3, accounts for label, newline and new label
				size = 1
				function = match[0]
				base = re.findall(r'[0-9a-z]{8}', line) #find base address
				base = base[0]
			else: #first iteration, reset size and find function values
				size = 0
				function = match[0] #function name (label)
				base = re.findall(r'[0-9a-z]{8}', line) #base address
				base = base[0]
				first = False
		line = fp.readline()


#print last function sice it was skipped
data["function"].append({"name":function,"base":base,"size":size-1})
json.dump(data, jf, indent=4, sort_keys=True) #write json data to file
