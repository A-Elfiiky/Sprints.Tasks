#!/bin/bash

echo "check if the directory found or not"

if [ -d ~/Reports ]
then
	echo "the directory already exists"
else
	##mkdir -p ~/Reports/2022
	D1=$(date -d "2022-12-31" "+%D")
 	D2=$(date  -d "2022-01-01" "+%D")
	echo "files creating >>> "
	while [ $D1 != $D2 ]
	do
		mkdir -p ~/Reports/2022/$(date -d "$D2" "+%m")
		touch ~/Reports/2022/$(date -d "$D2" "+%m")/$(date -d "$D2" "+%d").xls
		D2=$(date -d "$D2 + 1 day" "+%D")
	done
	echo "your files are created"


fi

######################back up####################

if [ $(date +%H) -ge 0 ] && [ $(date +%H) -le 5 ];
then
	mkdir -p ~/backup
	cp -R ~/Reports/* ~/backup
	echo "backing up your files"

else
        echo "Backup must be from 00 to 5:00 AM"
fi


