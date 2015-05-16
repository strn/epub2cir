#!/bin/sh

srcdir="$1"
destdir="$2"
namebase=renamed
startnum=1
step=2

usage="Usage: $0 srcdir destdir namebase startnum step

Copies files from srcdir into destdir according to
this rule:

First  file is named namebase-(startnum)
Second file is named namebase-(startnum+step)
Third  file is named namebase-(startnum+step+step)

Default values:

namebase='${namebase}'
startnum=${startnum}
step=${step}
"

test $# -lt 2 && echo "$usage" && exit 1



if [ $# -eq 3 ]; then
	namebase="$3"
fi

if [ $# -eq 4 ]; then
	namebase="$3"
	startnum=$4
fi

if [ $# -eq 5 ]; then
	namebase="$3"
	startnum=$4
	step=$5
fi

if [ ! -d ${srcdir} ]; then
	echo Source directory ${srcdir} does not exist, aborting ...
	exit 1
fi

if [ ! -d ${destdir} ]; then
	echo Destination directory ${srcdir} does not exist, aborting ...
	exit 1
fi

count=${startnum}

find "${srcdir}"/* -prune -type f -print0 | while read -d '' -r file
do
	ext=${file##*.}
	countf=`printf "%04d" ${count}`
	cp "$file" "${destdir}"/${namebase}-${countf}.${ext}
	((count+=step))
done