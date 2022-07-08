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
sleeptime=3

check_n_exec "sudo rm -r $INSTALLPATH"

mkdir -p $INSTALLPATH/$PreInstall

cd $ROOTPATH/$SOURCEFILES

tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( ls CAENComm* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( ls CAENVMELib* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( ls CAENUSB* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH -xvf $( ls CAENUpgrader* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH -xvf $( ls CAENDigitizer* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/ -xvf $( ls CAENwavedump* | grep -e ".tgz" -e ".tar.gz")

#installing requirements
echo ""
echo "Installing CAENVMELib"
cd $ROOTPATH/$INSTALLPATH/$PreInstall
cd $( ls | grep CAENVMELib* )/lib
sudo bash install_x64

echo "CAENVMELib hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENComm"
cd ../../
cd $( ls | grep CAENComm* )/lib
sudo bash install_x64


echo "CAENComm hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENUSB"
cd ../../
cd $( ls | grep CAENUSB* )
make
sudo make install

echo "CAENUSB hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENDigitizer"
cd $ROOTPATH/$INSTALLPATH
cd $( ls | grep CAENDigitizer* )
sudo bash install_64

echo "CAENDigitizer hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENUpgrader"
cd $ROOTPATH/$INSTALLPATH
cd $( ls | grep CAENUpgrader* )
./configure
sudo make
sudo make install


echo "CAENUpgrader hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing Wavedump"
cd $ROOTPATH
cd $( ls | grep wavedump* )
cd src
#replacing the .c file with my custom one
cp $ROOTPATH/$SOURCEFILES/WaveDump.c .
cd ..

echo "Installing gnuplot"
sudo apt install gnuplot

./configure
make
sudo make install

# creates a shortcut at Desktop. The move_files GUI must be installed by hand
mkdir -p ~/Desktop/WaveDumpData
cp $ROOTPATH/$SOURCEFILES/{WaveDumpExe.sh,move_files.sh} ~/Desktop/WaveDumpData/

mkdir -p ~/Documents/QtCreator
cp -r $ROOTPATH/$SOURCEFILES/install_by_hand/move_files ~/Documents/QtCreator/

cd $ROOTPATH
