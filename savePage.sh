#!/bin/bash



# Verify file argument - !Exists ==> print to stderr ^ return status code
[ "$#" -eq 0 -o ! -f "$1" ] && >&2 echo "ERROR exit $1"

#Exists when input argument and file found
[ $# -ge 1 -a -f "$1" ] && echo "$1" found and currently saving data


if [ ! -f "$1" ]; then
	
	touch "$1"
	chmod +755 "$1"
fi


printf "Year:\t%s\nPage:\t%s\n" "$2" "$3" > "$1"


if [ $? -eq 0 ]; then
	echo "Successfully saved current web location"
	exit 0
else
	echo "Couldn't save data properly" >&2
	exit 1
fi

