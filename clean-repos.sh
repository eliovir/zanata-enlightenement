# Clean and remove modifications from repositories.
SRC=$(pwd)

source projects.sh
for PROJECT in $PROJECTS; do
	cd $SRC
	[[ $PROJECT =~ $RE ]] && REPO="${BASH_REMATCH[1]}" && BRANCH="${BASH_REMATCH[2]}"
	SRC_REPO=src/$REPO
	echo - $SRC_REPO
	if [ ! -d $SRC_REPO/ ]; then
		continue;
	fi
	cd $SRC_REPO/ ;
	git clean -df &> /dev/null
	git reset --hard HEAD &> /dev/null
done
