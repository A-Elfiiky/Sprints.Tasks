#!/bin/bash

source ./task3

while true
do
        read -p "choose one of the following numbers:
                 1)check if the user have sudoer.
                 2)change ssh port.
                 3)disable root login.
                 4)change selinux and firewall port.
                 5)add Audit group.
		 6)add_user with function args.
		 7)create reports.
		 8)update system.
		 9)enable EPEL.
		 10)create manager user.
		 11)enable fail2ban.
		 12)chron backup.
		 13)sync files. :   " S
        case $S in
                1)IS_SUDOER;;
                2)change_port;;
                3)root_disable;;
                4)selinux_firewall_port;;
                5)add_group;;
                6)add_user;;
		7)reports;;
		8)system_update;;
		9)EPEL_ENABLE;;
		10)MANEGER;;
		11)fail2ban;;
		12)report_cron;;
		13)sync;;

        esac

        read -p "do you want to excute another function [y/n] : " ANS
        if [ $ANS == "n" ];then
                echo "exiting the script .........."
                break
        fi

done
