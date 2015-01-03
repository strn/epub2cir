#!/bin/sh

# Priprema e-knjigu za preslovljavanje
# Ulazni parametar 1: Ime EPUB datoteke 

if [ $# -eq 0 ]; then
	echo Morate zadati naziv elektronske knjige.
	exit 1
fi

EBOOK_NAME=$1
EBOOK_BASENAME=`basename "${EBOOK_NAME}" .epub`
EBOOK_CLEAN_NAME=`echo "$EBOOK_BASENAME" | tr [[:upper:]] [[:lower:]] | tr [[:punct:]] '-' | tr [[:blank:]] '-' | tr -s '-'`-sr

if [ -d ${EBOOK_CLEAN_NAME} ]; then
	echo Direktorijum ${EBOOK_CLEAN_NAME} vec postoji, izlazim ...
	exit 2
fi

mkdir ${EBOOK_CLEAN_NAME}
cp "${EBOOK_NAME}" ${EBOOK_CLEAN_NAME}/"${EBOOK_NAME}".zip
OLDPWD=`pwd`
cd ${EBOOK_CLEAN_NAME}
unzip "${EBOOK_NAME}".zip
rm -f "${EBOOK_NAME}".zip
cd "${OLDPWD}"
echo E-knjiga ${EBOOK_CLEAN_NAME} spremna je za uredjivanje.
