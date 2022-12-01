#!/bin/bash

CHECK=$(sudo -v &> /dev/null && echo "Sudoer" || echo "Not sudoer")


function IS_SUDOER() {
	if [ $CHECK == "Sudoer" ];then
		echo "you have sudoer previlages"
	else
		echo "you aren't a sudoer"
	fi
}

function change_port(){
	if [ $CHECK == "Sudoer" ];then
		read -p "enter port number between 1024 and 32,767 : " PORT
		if [ $PORT -ge 1024 ] && [ $PORT -le 32767 ] || [ $PORT -eq 22];then
			sudo sed -i -e "s/#^Port 22/Port $PORT/" /etc/ssh/sshd_config
			sudo sed -i -e "s/Port [0-9]*/Port $PORT/" /etc/ssh/sshd_config
			sleep 5
			systemctl reload sshd.service
			echo done
		else
			echo "you need to enter a correct number"
			change_port
		fi
	else
		echo "you need sudo previlages"
	fi
}

function root_disable(){
        if [ $CHECK == "Sudoer" ];then
                sudo sed -i -e "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config
		echo "root disabeled"
        else
                echo "you need sudo previlages"
        fi
}


function add_user(){
        if [ $CHECK == "Sudoer" ];then
		read -p "enter user name : " USER
                sudo adduser $USER
		echo "you have created a user with the name : $USER"
		read -p "do you want the user to have sudo previlages [y/n] : " ANS
		if [ $ANS == 'y' ];then
			echo "$USER	ALL=(ALL)	ALL" >>/etc/sudoers
			echo "a sudoer user has been added"
		fi
        else
                echo "you need sudo previlages"
        fi
}

function cron(){

	if [ $CHECK == "Sudoer" ];then 
		echo "0 12 1 * *  tar -cf homeback.tar $HOME " >> "/var/spool/cron/${USER}"
	else
		echo "need sudoer privilage"
	fi 
	echo "done"
}
function file_check(){
	read -p "enter the file directory : " DIR
	while [ ! -f "$DIR" ];do
		continue
	done
	echo "file exist"
}
