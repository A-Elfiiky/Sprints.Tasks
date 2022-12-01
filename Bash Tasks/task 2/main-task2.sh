#!/bin/bash
source ./task2.sh

while true
do
	read -p "choose one of the following numbers:
		 1)check if the user have root privilage
		 2)change ssh port
		 3)disable root login
		 4)add user
                 5)backup home directory
		 6)check if a file exist
 		 " S
	case $S in
		1)IS_SUDOER;;
		2)change_port;;
		3)root_disable;;
		4)add_user;;
		5)cron;;
		6)file_check;;
	esac

	read -p "do you need anything else [y/n] : " ANS
	if [ $ANS == "n" ];then
		echo "have a good day ->->"
		break
	fi

done

