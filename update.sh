#!/bin/bash

rm -fr polib/tests/

GIT_URL="git://git.enlightenment.org"
source packages.sh

DEFAULT_XGETTEXT_OPTIONS="--keyword=_ --keyword=D_:1 --keyword=d_:1 --keyword=N_ \
--keyword=P_:1,2 --keyword=dP_:1,2 --keyword=NP_:1,2 \
--keyword=EVRY_PLUGIN_BASE:1 --keyword=EVRY_ACTION_NEW:1 \
--from-code=UTF-8 \
--foreign-user"
DEFAULT_COPYRIGHT_HOLDER="Enlightenment development team"
DEFAULT_MSGID_BUGS_ADDRESS="enlightenment-devel@lists.sourceforge.net"

RE="^([^-]+):(.*)$"

SRC=$(pwd)

echo "Update submodules"
#git submodule update --remote

for PACKAGE in $PACKAGES; do
	cd $SRC ;
	[[ $PACKAGE =~ $RE ]] && REPO="${BASH_REMATCH[1]}" && BRANCH="${BASH_REMATCH[2]}"
	DOMAIN=$(basename $REPO)
	SRC_REPO=src/$REPO
	echo - $SRC_REPO
	if [ ! -d $SRC_REPO/ ]; then
		echo "  Adding git submodule $PACKAGE"
		mkdir -p $SRC_$REPO ;
		git submodule add -b master $GIT_URL/$REPO $SRC_REPO
	fi
	cd $SRC_REPO/
	git clean -df &> /dev/null
	git reset --hard HEAD &> /dev/null
	# create the .pot file
	# get $XGETTEXT_OPTIONS from Makevars
	XGETTEXT_OPTIONS=$DEFAULT_XGETTEXT_OPTIONS
	COPYRIGHT_HOLDER=$DEFAULT_COPYRIGHT_HOLDER
	MSGID_BUGS_ADDRESS=$DEFAULT_MSGID_BUGS_ADDRESS
	if [ -f $SRC/$SRC_REPO/po/Makevars ]; then
		sed -e 's/ = /="/g' -e 's/$/"/g' -e 's/\\"//g' -e 's/ ="$/=""/g' $SRC/$SRC_REPO/po/Makevars | grep = | grep -v DOMAIN= > params.sh
		source params.sh
		rm -f params.sh
	fi
	#
	if [ ! -d $SRC/$SRC_REPO/po/ ]; then
		mkdir -p $SRC/$SRC_REPO/po/
	fi
	if [ -f po/POTFILES.in ]; then
		xgettext $XGETTEXT_OPTIONS --add-comments=TRANSLATORS: --default-domain=$DOMAIN --files-from=po/POTFILES.in \
			--copyright-holder='$COPYRIGHT_HOLDER' --msgid-bugs-address='$MSGID_BUGS_ADDRESS' \
			--output=$SRC/$SRC_REPO/po/$DOMAIN.pot
	else
		if [ ! -d src/ ]; then
			continue;
		fi
		find src -type f -name "*.c" | xgettext $XGETTEXT_OPTIONS --add-comments=TRANSLATORS: --default-domain=$DOMAIN -f - \
			--copyright-holder='$COPYRIGHT_HOLDER' --msgid-bugs-address='$MSGID_BUGS_ADDRESS' \
			--output=$SRC/$SRC_REPO/po/$DOMAIN.pot

	fi
	if [ ! -f $SRC/$SRC_REPO/po/$DOMAIN.pot ]; then
		echo "  $SRC_REPO/po/$DOMAIN.pot does not exist!" ;
		continue;
	fi
done

cd $SRC
rm -fr src/desktop
./update-e17-l10n-from-desktop.py src --import-po
mv desktop src/

echo "Done."
