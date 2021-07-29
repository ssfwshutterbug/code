#!/bin/bash
# this cript will guide u how to edit the correct port and also
# help u to quickly get firewall command and install commmand's 
# args after you edit QCC.yml
# date: 20210517
# author: healer


# render txt with color: colorTxt red "hello"
function colorTxt(){
    cor=$1
    shift 1
    txt=$@
    case $cor in
        "red")
            echo -ne "\\033[0;31m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "green")
            echo -ne "\\033[0;32m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "yellow")
            echo -ne "\\033[0;33m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "blue")
            echo -ne "\\033[0;34m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "purple")
            echo -ne "\\033[0;35m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "cyan")
            echo -ne "\\033[0;36m${txt}"
            echo -e "\\033[0;39m"
            ;;
        "white")
            echo -ne "\\033[0;39m${txt}"
            echo -e "\\033[0;39m"
            ;;
    esac
}

# edit message
port_info="
<add `colorTxt red -pubport xxx` at end of `colorTxt red cmd`>    \n
443     `colorTxt green "->"`      webservice                     \n
8000    `colorTxt green "->"`      beainstall                     \n
8080    `colorTxt green "->"`      restfulapi                     \n
10001   `colorTxt green "->"`      userserver                     \n    
60001   `colorTxt green "->"`      probenat                       \n
60011   `colorTxt green "->"`      nodeserver                     \n
60021   `colorTxt green "->"`      collectserver                  \n
60031   `colorTxt green "->"`      fwserver                       \n
"

# show edit message
if [[ $# == 1 && $1 == "info" ]];then
    echo -e $port_info
    exit
fi


# show command message
if [[ $# != 0 ]];then
    colorTxt red "error parameter!"
    exit
else
    # get edit port info
    edit_info=`grep pubport QCC.yml |awk '{print $2 "\t" $NF}' |cut -d/ -f2-`
    # get zone message
    zone=`firewall-cmd --get-default-zone`

    # show firewall message
    for i in `echo $edit_info |tr -d [:alpha:]`
    do
        echo  "firewall-cmd --permanent --zone=${zone} --add-port=`colorTxt blue ${i}/tcp`"
    done
    echo "firewall-cmd `colorTxt blue --reload`"
    echo ""

    # show install command message
    for i in $edit_info;do
        serv=`echo $edit_info |cut -d" " -f1`
        port=`echo $edit_info |cut -d" " -f2`
        edit_info=`echo $edit_info |cut -d" " -f3-`
        case $serv in
            "beainstall")
                echo -n `colorTxt purple " --repo-http-port ${port}"`" "
                ;;
            "probenat")
                echo -n `colorTxt purple " -pport ${port}"`" "
                ;;
            "nodeserver")
                echo -n `colorTxt purple " -mport ${port}"`" "
                ;;
            "collectserver")
                echo -n `colorTxt purple " -cport ${port}"`" "
                ;;
            "fwserver")
                echo -n `colorTxt purple " -fport ${port}"`" "
                ;;
        esac
    done
    echo ""
fi