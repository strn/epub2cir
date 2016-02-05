#!/bin/sh

# Zavrsava obradu EPUB datoteke
# Ulazni parametar 1: Ime EPUB datoteke

if [ $# -eq 0 ]; then
	echo Morate zadati naslov elektronske knjige
	exit 1
fi

# Verzija programa EPUB
EPUBCHECK_VERSION=3.0.1

# Lokacija Epubcheck JAR datoteke (podesiti za vas sistem)
EPUB_PATH=/opt/app/e/epubcheck-${EPUBCHECK_VERSION}/epubcheck-${EPUBCHECK_VERSION}.jar

# Uzeti parametar
EBOOK_NAME=$1
EBOOK_BASENAME=`basename "${EBOOK_NAME}" .epub`
# "Normalizovati" ime e-knjige pretvaranjem svih slova u mala i uklanjanjem svih razmaka i interpunkcijskih znakova
EBOOK_CLEAN_NAME=`echo "$EBOOK_BASENAME" | tr [[:upper:]] [[:lower:]] | tr [[:punct:]] '-' | tr [[:blank:]] '-' | tr -s '-'`-sr

if [ ! -d ${EBOOK_CLEAN_NAME} ]; then
	echo Direktorijum ${EBOOK_CLEAN_NAME} ne postoji, izlazim ...
	exit 2
fi

# Opet napraviti e-knjigu
OLDPWD=`pwd`
cd ${EBOOK_CLEAN_NAME}
EBOOK_SERBIAN_NAME="${EBOOK_BASENAME}-cirilica"

# mimetype mora biti prva datoteka
zip -X -0 "${EBOOK_SERBIAN_NAME}".zip mimetype

# Najveca kompresija (-9)
zip -X -9 -r "${EBOOK_SERBIAN_NAME}".zip * -x mimetype "*~" "*.bak" "*.epub"
mv "${EBOOK_SERBIAN_NAME}".zip "${EBOOK_SERBIAN_NAME}".epub

# Obisati sve OSIM novo-kreirane e-knjige
find . ! '(' -name '*.epub' -o -name '.' -o -name '..' ')' -exec rm -rf {} \;

# Provera novo-kreirane e-knjige
# Ako je promenljiva definisana, provera knjige se ne radi
if [ -z ${EPUBCHECK_VALIDATE} ]; then
	if [ -f "${EPUB_PATH}" ]; then
		echo "Provera elektronske knjige  ..."
		java -jar ${EPUB_PATH} "${EBOOK_SERBIAN_NAME}".epub
		RETVAL=$?
		echo
		if [ ${RETVAL} -ne 0 ]; then
			echo "Provera nije uspela, knjiga je ostavljena otpakovana."
			unzip -qq "${EBOOK_SERBIAN_NAME}".epub
			rm -f "${EBOOK_SERBIAN_NAME}".epub
		else
			echo Knjiga "${EBOOK_SERBIAN_NAME}"-ur.epub je spremna u direktorijumu "${EBOOK_CLEAN_NAME}".
			mv "${EBOOK_SERBIAN_NAME}".epub "${EBOOK_SERBIAN_NAME}"-ur.epub
		fi
	else
		echo EPUCheck JAR '${EPUB_PATH}' ne postoji, izlazim ...
		exit 3
	fi
else
	echo Knjiga "${EBOOK_SERBIAN_NAME}".epub je spremna u direktorijumu "${EBOOK_CLEAN_NAME}".
fi
cd "${OLDPWD}"

