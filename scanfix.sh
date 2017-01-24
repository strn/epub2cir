#!/bin/bash

# This program tries to fix as many problems with OCRed text as possible

if [ $# -eq 0 ]; then
	echo "No input file specified"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "Undefined input file"
	exit 1
fi

inplace="-i"

sed $inplace -e 's/·//g;s/"/“/g;s/[[:blank:]]\{2,\}/ /g;s/\. \. \./\.\.\./g;s/^\d+\s*$//g;/^ *[0-9]\+ *$/d;/•/d' "$1"
sed $inplace -e ':a;N;$!ba;s/\([абвгдђежзијклљмнњопрстћуфхцчџш]\)[-–—]\n/\1/g' "$1"
sed $inplace -e ':a;N;$!ba;s/\([абвгдђежзијклљмнњопрстћуфхцчџш,]\)\n/\1 /g' "$1"

exit 0
