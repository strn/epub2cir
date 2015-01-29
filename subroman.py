#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import collections
import re
import sys
from optparse import OptionParser


HELPTEXT = """subroman.py <opcije>"""

ROMANDICT = {
	u'ИИ'     : u'II',
	u'ИИИ'    : u'III',
	u'ИВ'     : u'IV',
	u'В'      : u'V',
	u'ВИ'     : u'VI',
	u'ВИИ'    : u'VII',
	u'ВИИИ'   : u'VIII',
	u'ИX'     : u'IX',
	u'XИ'     : u'XI',
	u'XИИ'    : u'XII',
	u'XИИИ'   : u'XIII',
	u'XИВ'    : u'XIV',
	u'XВ'     : u'XV',
	u'XВИ'    : u'XVI',
	u'XВИИ'   : u'XVII',
	u'XВИИИ'  : u'XVIII',
	u'XИX'    : u'XIX',
	u'XXИ'    : u'XXI',
	u'XXИИ'   : u'XXII',
	u'XXИИИ'  : u'XXIII',
	u'XXИВ'   : u'XXIV',
	u'XXВ'    : u'XXV',
	u'XXВИ'   : u'XXVI',
	u'XXВИИ'  : u'XXVII',
	u'XXВИИИ' : u'XXVIII',
	u'XXИX'   : u'XXIX',
	u'XXXИ'   : u'XXXI',
}


def multiple_replacer(*key_values):
	replace_dict = dict(key_values)
	replacement_function = lambda match: replace_dict[match.group(0)]
	pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
	return lambda string: pattern.sub(replacement_function, string)


if __name__ == "__main__":
	parser = OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input-file", action="store", type="string", dest="inputFile", default=sys.stdin,
		help="Ulazna datoteka sa tekstom koji treba pretvoriti. Standardni ulaz ako nije navedeno.")
	parser.add_option("-o", "--output-file", action="store", type="string", dest="outputFile", default=sys.stdout,
		help="Ulazna datoteka u koju ce se smestiti rezultat pretvaranja. Standardni izlaz ako nije navedeno.")
	parser.add_option("-f", "--force", action="store_true", dest="forceOverwrite", default=False,
		help="Prepisati izlaznu datoteku cak i ako ona postoji")
	(opts, args) = parser.parse_args()

	#print options
	
	# Check inputfile
	if opts.inputFile != sys.stdin:
		try:
			opts.inputFile = codecs.open( opts.inputFile, 'rb', 'utf-8' )
		except:
			print "Ne mogu da otvorim ulaznu datoteku, prekid obrade."
			sys.exit(1)
	
	# Check outputfile
	if opts.outputFile != sys.stdout:
		try:
			opts.outputFile = open( opts.outputFile, 'wb' )
		except:
			print "Ne mogu da otvorim izlaznu datoteku, prekid obrade."
			sys.exit(2)
	
	orDict = collections.OrderedDict(sorted(ROMANDICT.items(), reverse=True))
	compDict = re.compile('|'.join(orDict))

	for line in opts.inputFile:
		convLine = compDict.sub(lambda m:orDict[m.group()], line)
		opts.outputFile.write(convLine)


	if opts.inputFile != sys.stdin:
		opts.inputFile.close()
	if opts.outputFile != sys.stdout:
		opts.outputFile.close()
