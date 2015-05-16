#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re
import sys
import xml.sax
from lxml import etree
from optparse import OptionParser


HELPTEXT = "uniconv.py <opcije>"

LATLISTS = {
	'utf-8' : [ u"Đ", u"Dž", u"DŽ", u"LJ", u"Lj", u"NJ", u"Nj", u"A", u"B", u"V", u"G", u"D", u"E", u"Ž", u"Z", u"I", u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"R", u"S", u"T", u"Ć", u"U", u"F", u"H", u"C", u"Č", u"Š", u"a", u"b", u"v", u"g", u"dž", u"d", u"e", u"ž", u"z", u"i", u"j", u"k", u"lj", u"l", u"m", u"nj", u"n", u"o", u"p", u"r", u"s", u"t", u"ć", u"u", u"f", u"h", u"c", u"č", u"š", u"đ", u"Ð" ],
	'yuscii' : [ '', '', '', '', '', '' ],
	'tanjug' : [ '', '', '', '', '', '' ],
	'ascii'  : [ 'D', 'Dz', 'DZ', 'LJ', 'Lj', 'NJ', 'Nj', 'A' ]
}

CIRUTFLIST = [ u"Ђ", u"Џ", u"Џ", u"Љ", u"Љ", u"Њ", u"Њ", u"А", u"Б", u"В", u"Г", u"Д", u"Е", u"Ж", u"З", u"И", u"Ј", u"К", u"Л", u"М", u"Н", u"О", u"П", u"Р", u"С", u"Т", u"Ћ", u"У", u"Ф", u"Х", u"Ц", u"Ч", u"Ш", u"а", u"б", u"в", u"г", u"џ", u"д", u"е", u"ж", u"з", u"и", u"ј", u"к", u"љ", u"л", u"м", u"њ", u"н", u"о", u"п", u"р", u"с", u"т", u"ћ", u"у", u"ф", u"х", u"ц", u"ч", u"ш", u"ђ", u"Ђ" ]

ENCODINGS = {
	'cp1250'    : ['cp1250', 'windows-1250', 'cp1250p', 'win-1250', 'win1250'],
	'cp1251'    : ['cp1251', 'windows-1251', 'win-1251', 'win1251'],
	'cp852'     : ['cp852', 'ibm852'],
	'iso8859_2' : ['iso8859_2', 'iso-8859-2', 'latin2', 'l2', 'iso8859-2'],
	'iso8859_5' : ['iso8859_5', 'iso-8859-5', 'cyrillic', 'iso8859-5'],
	'ascii'     : ['ascii', 'yuscii', 'tanjug', 'srpscii', 'qwyx', 'qwyx-de-luxe'],
	'utf-8'     : ['utf-8', 'utf8']
}

# Special tags for eBook files
EBOOK_TAGS = ( 'text', 'creator', 'contributor', 'description', 'meta', 'publisher', 'subject', 'title' )
EBOOK_TAGS_ATTRIBUTES = { 'meta' : { 'name' : ('calibre:series', 'calibre:title_sort') } }
# HTML tags that can contain text requireing transliteration
HTML_TAGS = ('a', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'img', 'p', 'br', 'b', 'i', 'em', 'span', 'sub', 'sup', 'title', 'th', 'td', 'li', 'strong')
GLOBAL_HTML4_ATTRS = ('accesskey', 'class', 'dir', 'id', 'lang', 'style', 'tabindex', 'title',)
# Dictionary that specifies which attributes are supported by which HTML tags
ALLOWED_ATTRIBS = {
	'br' : GLOBAL_HTML4_ATTRS,
	'body' : GLOBAL_HTML4_ATTRS,
	'table' : ('align', 'bgcolor', 'border', 'cellpadding', 'cellspacing', 'frame', 'rules', 'sortable', 'summary', 'width',),
	'td' : ('abbr', 'align', 'axis', 'bgcolor', 'char', 'charoff', 'colspan', 'headers', 'height', 'nowrap', 'rowspan', 'scope', 'valign', 'width',) + GLOBAL_HTML4_ATTRS,
	'tr' : ('align', 'bgcolor', 'char', 'charoff', 'valign',) + GLOBAL_HTML4_ATTRS,
	'img' : ( 'alt', 'class', 'ismap', 'src', 'style', 'width',) + GLOBAL_HTML4_ATTRS,
	'svg' : ( 'xmlns', 'xmlns:link', 'height', 'version', 'width',)
}
# Dictionary that says what attribute can be added to what tag, if missing
ADD_IF_MISSING_ATTRS = {
	'img' : ( ('alt', 'img'), )
}
INPUTFILE = None
OUTPUTFILE = None


if __name__ == "__main__":
	parser = OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input-file", action="store", type="string", dest="inputFile", default='',
		help="Ulazna datoteka sa tekstom koji se preslovljava")
	parser.add_option("-o", "--output-file", action="store", type="string", dest="outputFile", default='',
		help="Izlazna datoteka u koju ce biti upisan rezultat pretvaranja")
	parser.add_option("-u", "--input-enc", action="store", type="string", dest="inputEnc", default='utf-8',
		help="Ulazni kodni raspored")
	parser.add_option("-e", "--output-enc", action="store", type="string", dest="outputEnc", default='utf-8',
		help="Izlazni kodni raspored")
	parser.add_option("-f", "--force", action="store_true", dest="forceOverwrite", default=False,
		help="Nasilno prepisivanje izlazne datoteke, ukoliko ona postoji")
	parser.add_option("-d", "--direction", action="store", type="string", dest="direction", default='luc',
		help="Smer pretvaranja: luc = latinica-u-cirilicu, cul = cirilica-u-latinicu")
	parser.add_option("-t", "--type", action="store", type="string", dest="documentType", default='txt',
		help="Tip dokumenta koji se pretvara (TXT, XML ili HTML)")
	parser.add_option("-b", "--ebook", action="store_true", dest="ebook", default=False,
		help="Pretvaranje teksta u posebnim tag-ovima, koji se mogu naci u EPUB datotekama")
	(options, args) = parser.parse_args()

	# Determine how to open input and output file
	for (inputEnc, aliases) in ENCODINGS.items():
		if options.inputEnc.lower() in aliases:
			options.inputEnc = inputEnc
			break

	for (outputEnc, aliases) in ENCODINGS.items():
		if options.outputEnc.lower() in aliases:
			options.outputEnc = outputEnc
			break
	
	#print options
	
	# Check inputfile
	if options.inputFile == '':
		INPUTFILE = codecs.getreader( options.inputEnc )( sys.stdin )
	else:
		try:
			if options.documentType in ( 'txt' ):
				INPUTFILE = codecs.open( options.inputFile, 'rb', options.inputEnc )
			else:
				INPUTFILE = open( options.inputFile, 'rb' )
		except:
			sys.exit(1)
	
	# Check outputfile
	if options.outputFile == '':
		OUTPUTFILE = codecs.getwriter( options.outputEnc )( sys.stdout )
	else:
		try:
			OUTPUTFILE = open( options.outputFile, 'wb' )
		except:
			sys.exit(2)

	# Construct dictionary based on input and output encoding
	if options.direction == 'luc':
		convDict = dict(zip( LATLISTS[ options.inputEnc ], CIRUTFLIST))
	else:
		convDict = dict(zip( CIRUTFLIST, LATLISTS[ options.inputEnc ]))
	
	#print 'Convdict:'
	#print "%r" % convDict
	
	# Compile dictionary
	compDict = re.compile('|'.join(convDict))
	
	if options.documentType == 'txt':
		for line in INPUTFILE:
			convLine = compDict.sub(lambda m:convDict[m.group()], line)
			OUTPUTFILE.write( convLine )
			
	elif options.documentType == 'html':
		parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True, encoding=options.inputEnc)
		tree = etree.parse(INPUTFILE, parser)
		
		# Add META tag with correct encoding
		metaEl = tree.xpath("//meta[@charset or @content]")
		if not metaEl:
			# Add META tags that define content
			headEl = tree.find( 'head' )
			if headEl is not None:
				metachr = etree.SubElement( headEl, 'meta' )
				metachr.set( u'http-equiv', u"content-type" )
				metachr.set( u'content', u"text/html; charset=%s" % options.outputEnc )
				metachr.text = ''
				
		# Walk over tree, changing text nodes
		for elem in tree.getiterator():
			if elem.tag in HTML_TAGS:
				if elem.text is not None:
					elem.text = compDict.sub(lambda m:convDict[m.group()], elem.text)
				if elem.tail is not None:
					elem.tail = compDict.sub(lambda m:convDict[m.group()], elem.tail)
			if elem.tag in ADD_IF_MISSING_ATTRS:
				for (attr, values) in ADD_IF_MISSING_ATTRS.items():
					for val in values:
						if val[0] not in elem.attrib.keys():
							#print 'Elementu %s nedostaje %s' % (elem.tag, attr)
							elem.attrib[ val[0] ] = val[1]
			# Check if all attributes are in list of allowed/supported
			if ALLOWED_ATTRIBS.has_key( elem.tag ):
				for attr in elem.attrib.keys():
					if attr not in ALLOWED_ATTRIBS[ elem.tag ]:
						del elem.attrib[ attr ]
					
		result = etree.tostring(tree.getroot(), pretty_print=True, method="xml", encoding=options.outputEnc )
		OUTPUTFILE.write( result )
		
	elif options.documentType == 'xml':

		parser = etree.XMLParser(remove_blank_text=True, encoding=options.inputEnc)
		tree = etree.parse(INPUTFILE, parser)
		# Walk over tree, changing text nodes
		for elem in tree.getiterator():
			if options.ebook:
				# Remove namespace
				leftbr = elem.tag.find('{')
				rightbr = elem.tag.find('}')
				if leftbr > -1 and rightbr > -1 and rightbr > leftbr:
					tag = elem.tag[rightbr+1:]
				else:
					tag = elem.tag
					
				if tag in EBOOK_TAGS:
					if elem.text is not None:
						elem.text = compDict.sub(lambda m:convDict[m.group()], elem.text)
					# Convert some attributes
					if tag == 'meta' and elem.attrib.has_key( 'name' ):
						condList = EBOOK_TAGS_ATTRIBUTES[ 'meta' ][ 'name' ]
						if elem.attrib[ 'name' ] in condList:
							elem.attrib[ 'content' ] = compDict.sub(lambda m:convDict[m.group()], elem.attrib[ 'content' ])

			else:
				if elem.text is not None:
					elem.text = compDict.sub(lambda m:convDict[m.group()], elem.text)
					
		result = etree.tostring(tree.getroot(), method='xml', pretty_print=True, encoding=options.outputEnc)
		#print result
		OUTPUTFILE.write( result )
		
	else:
		print "Document type %s not recognized, exiting ..." % (options.documentType)
		sys.exit(3)

	INPUTFILE.close()
	OUTPUTFILE.close()
