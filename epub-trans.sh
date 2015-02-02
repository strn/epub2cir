#!/bin/sh

# Preslovljava e-knjigu
# Ulazni parametar 1: Ime EPUB datoteke 

# Dodeliti bilo koju drugu vrednost (osim 1)
# ako se ne zeli zamena praznina u HTML datotekama
REPLACE_HTML_SPACES=1

# Podesiti putanje ukoliko se razlikuju na ovom sistemu
# Put do komande "file"
FILE_CMD=/usr/bin/file
# Put do komande "tr"
TR_CMD=/usr/bin/tr

if [ $# -eq 0 ]; then
	echo Morate zadati naziv elektronske knjige.
	exit 1
fi

function trans_toc {
# Translate toc.ncx
if [ -f toc.ncx ]; then 
	echo "Pretvaram toc.ncx (pronadjen u $1) ..."
	uniconv.py -i toc.ncx -t xml -b -o toc-roman.ncx
	echo "  Obrada rimskih brojeva ..."
	subroman.py -i toc-roman.ncx -o toc-sr.ncx
	if [ "${REPLACE_HTML_SPACES}" -eq 1 ]; then
		sed -i 's/%20/-/g' toc-sr.ncx
	fi
	if [ -f toc-sr.ncx ]; then
		mv toc-sr.ncx toc.ncx
		rm -f toc-roman.ncx
	fi
fi
}

function trans_content {
# Translate content.opf
if [ -f content.opf ]; then 
	echo "Pretvaram content.opf (pronadjen u $1) ..."
	# Use flag -b for handling tags in eBooks
	uniconv.py -i content.opf -t xml -b -o content-sr.opf
	if [ "${REPLACE_HTML_SPACES}" -eq 1 ]; then
		sed -i 's/%20/-/g' content-sr.opf
	fi
	if [ -f content-sr.opf ]; then
		mv content-sr.opf content.opf
	fi
fi
}

function remove_spaces_in_file_names {
	echo "Uklanjam razmake iz naziva datoteka ..."
	for extension in css jpg jpeg png gif
	do
		find . -type f -name "*.${extension}" -print0 | while read -d '' -r file
		do
			filenosp=`echo "${file}" | tr [[:blank:]] '-' | tr -s '-'`
			if [ "${filenosp}" != "${file}" ]; then
				mv "${file}" "${filenosp}"
				echo Datoteka "${file}" preimenovana u "${filenosp}"
			fi
		done
	done
}

function trans_xhtml {
	find . \( -name "*ml" -o -name "*ML" -o -name "*htm" \) -type f -print0 | while read -d '' -r file
	do
		# Uzmi prezime datoteke
		file_ext_orig=${file##*.}
		filext=`echo "$file_ext_orig" | tr [[:upper:]] [[:lower:]]`
		if [ "${filext}" == "xml" ]; then
			uniconv.py -i "${file}" -t xml -o "${file}".sr
		else
			uniconv.py -i "${file}" -t html -o "${file}".sr
		fi
		# Ukloni &#13;
		sed -i 's/&#13;//g' "${file}".sr
		# Ukloni prazne linije
		sed -i 's///g' "${file}".sr
		sed -i '/^$/d' "${file}".sr
		# Ukloni praznine - OPREZ!!!
		if [ "${REPLACE_HTML_SPACES}" -eq 1 ]; then
			sed -i 's/%20/-/g' "${file}".sr
		fi
		# Zameni odredjene regularne izraze
		regexconv.py -i "${file}".sr -o "${file}".regex
		
		filenosp=`echo "${file}" | ${TR_CMD} [[:blank:]] '-' | ${TR_CMD} -s '-'`
		[ -f "${file}" ] && mv "${file}".regex "${filenosp}"
		rm -f "${file}".sr
		if [ "${filenosp}" != "${file}" ]; then
			rm -f "${file}"
		fi
	done
}

EBOOK_NAME=$1
EBOOK_BASENAME=`basename "${EBOOK_NAME}" .epub`
EBOOK_CLEAN_NAME=`echo "$EBOOK_BASENAME" | tr [[:upper:]] [[:lower:]] | tr [[:punct:]] '-' | tr [[:blank:]] '-' | tr -s '-'`-sr

if [ ! -d ${EBOOK_CLEAN_NAME} ]; then
	echo Direktorijum ${EBOOK_CLEAN_NAME} ne postoji, izlazim ...
	exit 2
fi
OLDPWD=`pwd`

cd ${EBOOK_CLEAN_NAME}

echo "Pretvaram poglavlja ..."
trans_xhtml
trans_toc ${EBOOK_CLEAN_NAME}
trans_content ${EBOOK_CLEAN_NAME}

for dir in OEBPS OPS
do
	if [ -d $dir ]; then
		cd $dir
		trans_toc $dir
		trans_content $dir
		remove_spaces_in_file_names
	fi
done

cd "${OLDPWD}"
echo ${EBOOK_BASENAME} je preslovljena na cirilicu.
