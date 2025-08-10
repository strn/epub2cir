#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Menja odredjene pojave regularnog izraza u datoteci novim izrazom
# Izmena se moze ponoviti za veci broj regularnih izraza

import re
import sys
from optparse import OptionParser


HELPTEXT = """
Program se koristi na sledeci nacin:
           
	   regexconv.py -t tip_prevoda -d datoteka_u_utf-8_kodu
"""

INPUTFILE = None
OUTPUTFILE = None

def get_page_number(aMatch):
	return aMatch.group(0).replace(aMatch.group(1), '%03d' % int(aMatch.group(1)))

def get_underline(aMatch):
	return aMatch.group(0).replace(aMatch.group(1), 'em' )

def change_roman_numbers(aMatch):
	#print("NASAO RIMSKE BROJEVE!!!")
	#print(aMatch)
	return "POMAH"
	
REPLACE_LIST = (
	( re.compile(r'<a\s*href="p?(\d*)\.html?"\s*/>') , get_page_number ),
	( re.compile(r'<(u)>'), get_underline ),
	( re.compile(r'</(u)>'), get_underline ),
	( re.compile(r'\b(?=[МДЦЛXВИ]+\b)М{0,4}(ЦМ|ЦД|Д?Ц{0,3})(XЦ|XЛ|Л?X{0,3})(ИX|ИВ|В?И{0,3})\b',re.UNICODE), change_roman_numbers)
)

if __name__ == "__main__":
	parser = OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input-file", action="store", type="string", dest="inputFile",
		help="Input file containing text that needs to be converted")
	parser.add_option("-o", "--output-file", action="store", type="string", dest="outputFile",
		help="Output file that will be created as a result of conversion")
	parser.add_option("-f", "--force", action="store_false", dest="forceOverwrite", default=False,
		help="Overwrite output file even if it exists")
	(options, args) = parser.parse_args()
	
	# Check inputfile
	if not options.inputFile:
		INPUTFILE = sys.stdin
	else:
		try:
			INPUTFILE = open( options.inputFile, 'rb' )
		except:
			sys.exit(1)
	
	# Check outputfile
	if not options.outputFile:
		OUTPUTFILE = sys.stdout
	else:
		try:
			OUTPUTFILE = open( options.outputFile, 'wb' )
		except:
			sys.exit(2)

	for line in INPUTFILE:
		convLine = line.decode('utf-8')
		for (regComp, regFunc) in REPLACE_LIST:
			matchExp = regComp.search(convLine)
			if matchExp:
				#print regComp.findall(convLine)
				convLine = regComp.sub(regFunc(matchExp), convLine)		
		OUTPUTFILE.write(convLine.encode('utf-8'))

	INPUTFILE.close()
	OUTPUTFILE.close()
