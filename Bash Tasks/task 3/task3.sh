#!/bin/bash

CHECK=$(sudo -v &> /dev/null && echo "Sudoer" || echo "Not sudoer")

function IS_SUDOER() {
        if [ $CHECK == "Sudoer" ];then
                echo "you have sudoer previlages"
        else
                echo "sorry you need sudoer previlages"
        fi
}


function change_port(){
        if [ $CHECK == "Sudoer" ];then
                echo "you entered $1 "
                if [ $1 -ge 1024 ] && [ $1 -le 32767 ] || [ $1 -eq 22];then
                        sudo sed -i -e "s/#^Port 22/Port $1/" /etc/ssh/sshd_config
                        sudo sed -i -e "s/Port [0-9]*/Port $1/" /etc/ssh/sshd_config
                        sleep 5
                        systemctl reload sshd.service
                        echo done
                else
                        echo "choose another port number, the choosen one not acceptable"
                        change_port
                fi
        else
                echo "sorry you need sudoer previlages"
        fi
}

function root_disable(){
        if [ $CHECK == "Sudoer" ];then
                sudo sed -i -e "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config
                echo "root disabeled"
        else
                echo "sorry you need sudoer previlages"
        fi
}

function selinux_firewall_port(){
	if [ $CHECK == "Sudoer" ];then
		sudo semanage port -a -t ssh_port_t -p tcp $1
		echo "selinux is updated to $1"
		sudo firewall-cmd --add-port=$1/tcp --permanent
		sudo firewall-cmd --reload
		sudo systemctl reload firewalld.service
		echo "firewall is updated to $1"
	else
                echo "sorry you need sudoer previlages"
        fi

}



function add_group(){
	if [ $CHECK == "Sudoer" ];then
		sudo groupadd -g 20000 Audit
		echo "group Audit added"
	else
                echo "sorry you need sudoer previlages"
        fi

}



function add_user(){
	if [ $(getent group Audit) ];then
        	 echo "group exists"
	else
         	 add_group
	fi
	pass=$(perl -e 'print crypt($ARGV[0],"password")' $2)

	if [ $CHECK == "Sudoer" ];then
                useradd -m -p "$pass"  "$1" -g Audit
        else
                echo "sorry you need sudoer previlages"
        fi



}

function reports(){
	if [ $CHECK == "Sudoer" ];then
		if [ -d /home/USER/reports ]
		then
       			echo "directory exists"
		else
        		##mkdir -p ~/Reports/2022
        		D1=$(date -d "2022-12-31" "+%D")
        		D2=$(date  -d "2022-01-01" "+%D")
        		echo "creating your files please wait >>> "
        		while [ $D1 != $D2 ]
        		do
                		sudo mkdir -p /home/USER/reports
				DAY=$(date -d "$D2" "+%d")
				MONTH=$(date -d "$D2" "+%m")
				FILE="2022-$DAY-$MONTH.xls"
				sudo touch /home/USER/reports/$FILE
                		D2=$(date -d "$D2 + 1 day" "+%D")
        		done
			sudo chmod -R 660  /home/USER/reports
        		echo "your files are created"


		fi
	else
                echo "sorry you need sudoer previlages"
        fi
}




function system_update(){
        if [ $CHECK == "Sudoer" ];then
                sudo yum update -y
                echo "System updated"
        else
                echo "sorry you need sudoer previlages"
        fi

}



function EPEL_ENABLE(){
        if [ $CHECK == "Sudoer" ];then
                sudo yum install epel-release -y
                echo "System EPEL updated"
        else
                echo "sorry you need sudoer previlages"
        fi

}



function MANEGER(){
	if [ $CHECK == "Sudoer" ];then
                sudo useradd -u 30000 manager
                echo "User Maneger is added"
        else
                echo "sorry you need sudoer previlages"
        fi
}



function fail2ban(){
        if [ $CHECK == "Sudoer" ];then
		system_update
                sudo yum install fail2ban
		sudo systemctl enable fail2ban
		systemctl start fail2ban
                echo "fail2ban is enabled"
        else
                echo "sorry you need sudoer previlages"
        fi
}



function report_cron(){
	if  [ $CHECK == "Sudoer" ];then
		echo "0 1 * * 1-4 tar -cf /root/backups/reports-$(date +%U)-$(date +%u).tar  ~/reports" >> /var/spool/cron/root
	else
		(crontab -1 2>/dev/null;echo "0 1 * * 1-4 tar -cf /root/backups/reports-$(date +%U)-$(date +%u).tar  ~/reports")| crontab -
	fi
	echo "backup schedule is successfully done"
}






function sync()
{
	mkdir -p  ~/manager/audit/reports
	if  [[ $CHECK == "Sudoer" ]];then
		echo "0 2 * * 1-4 sync ~/reports/* ~/manager/audit/reports" >> /var/spool/cron/root

	else
		(crontab -1 2>/dev/null;echo "0 2 * * 1-4 sync ~/reports/* ~/manager/audit/reports")|crontab -
	fi
	echo "synced successfully"
}
