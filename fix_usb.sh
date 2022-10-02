#!/bin/bash


function check_n_exec(){
    echo "The following command will be executed:"
    mycommand=$1
    echo $mycommand
    read -p "Are you sure (y/n)? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
    eval $mycommand
    
}


INSTALLPATH=Installation
PreInstall=PreInstallThis
SOURCEFILES=installation_files
ROOTPATH=$( pwd )
sleeptime=2

check_n_exec "sudo rm -r $INSTALLPATH/$PreInstall"

mkdir -p $INSTALLPATH/$PreInstall

cd $ROOTPATH/$SOURCEFILES

tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENComm* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENVMELib* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENUSB* | grep -e ".tgz" -e ".tar.gz")

#installing requirements
echo ""
echo "Installing CAENVMELib"
cd $ROOTPATH/$INSTALLPATH/$PreInstall
cd $( /bin/ls | grep CAENVMELib* )/lib
sudo bash install_x64

echo "CAENVMELib hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENComm"
cd ../../
cd $( /bin/ls | grep CAENComm* )/lib
sudo bash install_x64


echo "CAENComm hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENUSB"
cd ../../
cd $( /bin/ls | grep CAENUSB* )
make
sudo make install

echo "CAENUSB hopefully installed, check for errors"
echo ""
sleep $sleeptime

cd $ROOTPATH
