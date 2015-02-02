#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import collections
import re
import sys
from optparse import OptionParser


HELPTEXT = "subroman.py <opcije>"

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
	u'XXИИИ'    : u'XXIII',
	u'XXИВ'     : u'XXIV',
	u'XXВ'      : u'XXV',
	u'XXВИ'     : u'XXVI',
	u'XXВИИ'    : u'XXVII',
	u'XXВИИИ'   : u'XXVIII',
	u'XXИX'     : u'XXIX',
	u'XXXИ'     : u'XXXI',
	u'XXXИИ'    : u'XXXII',
	u'XXXИИИ'   : u'XXXIII',
	u'XXXИВ'    : u'XXXIV',
	u'XXXВ'     : u'XXXV',
	u'XXXВИ'    : u'XXXVI',
	u'XXXВИИ'   : u'XXXVII',
	u'XXXВИИИ'  : u'XXXVIII',
	u'XXXИX'    : u'XXXIX',
	u'XЛ'       : u'XL',
	u'XЛИ'      : u'XLI',
	u'XЛИИ'     : u'XLII',
	u'XЛИИИ'    : u'XLIII',
	u'XЛИВ'     : u'XLIV',
	u'XЛВ'      : u'XLV',
	u'XЛВИ'     : u'XLVI',
	u'XЛВИИ'    : u'XLVII',
	u'XЛВИИИ'   : u'XLVIII',
	u'XЛИX'     : u'XLIX',
	u'ЛИ'       : u'LI',
	u'ЛИИ'      : u'LII',
	u'ЛИИИ'     : u'LIII',
	u'ЛИВ'      : u'LIV',
	u'ЛВ'       : u'LV',
	u'ЛВИ'      : u'LVI',
	u'ЛВИИ'     : u'LVII',
	u'ЛВИИИ'    : u'LVIII',
	u'ЛИX'      : u'LIX',
	u'ЛX'       : u'LX',
	u'ЛXИ'      : u'LXI',
	u'ЛXИИ'     : u'LXII',
	u'ЛXИИИ'    : u'LXIII',
	u'ЛXИВ'     : u'LXIV',
	u'ЛXВ'      : u'LXV',
	u'ЛXВИ'     : u'LXVI',
	u'ЛXВИИ'    : u'LXVII',
	u'ЛXВИИИ'   : u'LXVIII',
	u'ЛXИX'     : u'LXIX',
	u'ЛXX'      : u'LXX',
	u'ЛXXИ'     : u'LXXI',
	u'ЛXXИИ'    : u'LXXII',
	u'ЛXXИИИ'   : u'LXXIII',
	u'ЛXXИВ'    : u'LXXIV',
	u'ЛXXВ'     : u'LXXV',
	u'ЛXXВИ'    : u'LXXVI',
	u'ЛXXВИИ'   : u'LXXVII',
	u'ЛXXВИИИ'  : u'LXXVIII',
	u'ЛXXИX'    : u'LXXIX',
	u'ЛXXX'     : u'LXXX',
	u'ЛXXXИ'    : u'LXXXI',
	u'ЛXXXИИ'   : u'LXXXII',
	u'ЛXXXИИИ'  : u'LXXXIII',
	u'ЛXXXИВ'   : u'LXXXIV',
	u'ЛXXXВ'    : u'LXXXV',
	u'ЛXXXВИ'   : u'LXXXVI',
	u'ЛXXXВИИ'  : u'LXXXVII',
	u'ЛXXXВИИИ' : u'LXXXVIII',
	u'ЛXXXИX'   : u'LXXXIX',
	u'XЦ'       : u'XC',
	u'XЦИ'      : u'XCI',
	u'XЦИИ'     : u'XCII',
	u'XЦИИИ'    : u'XCIII',
	u'XЦИВ'     : u'XCIV',
	u'XЦВ'      : u'XCV',
	u'XЦВИ'     : u'XCVI',
	u'XЦВИИ'    : u'XCVII',
	u'XЦВИИИ'   : u'XCVIII', # 98
	u'XЦИX'     : u'XCIX', # 99
}


if __name__ == "__main__":
	parser = OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input-file", action="store", type="string", dest="inputFile", default=sys.stdin,
		help="Ulazna datoteka sa tekstom koji treba pretvoriti. Standardni ulaz ako nije navedeno.")
	parser.add_option("-o", "--output-file", action="store", type="string", dest="outputFile", default=sys.stdout,
		help="Izlazna datoteka u koju ce se smestiti rezultat pretvaranja. Standardni izlaz ako nije navedeno.")
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
