#!/bin/sh

# Prepares ebook for translation
# Input: epub file

if [ $# -eq 0 ]; then
	echo You must provide eBook name
	exit 1
fi

EBOOK_NAME=$1
EBOOK_BASENAME=`basename "${EBOOK_NAME}" .epub`
EBOOK_CLEAN_NAME=`echo "$EBOOK_BASENAME" | tr [[:upper:]] [[:lower:]] | tr [[:punct:]] '-' | tr [[:blank:]] '-' | tr -s '-'`-sr

if [ -d ${EBOOK_CLEAN_NAME} ]; then
	echo Directory ${EBOOK_CLEAN_NAME} already exists, exiting ...
	exit 2
fi

mkdir ${EBOOK_CLEAN_NAME}
cp "${EBOOK_NAME}" ${EBOOK_CLEAN_NAME}/"${EBOOK_NAME}".zip
OLDPWD=`pwd`
cd ${EBOOK_CLEAN_NAME}
unzip "${EBOOK_NAME}".zip
rm -f "${EBOOK_NAME}".zip
cd "${OLDPWD}"
echo ${EBOOK_CLEAN_NAME} is ready for editing.
