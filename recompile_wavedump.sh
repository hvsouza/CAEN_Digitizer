#!/bin/bash

if [ -z $1 ]; then
    npts=10000
else
    npts=$1
fi

ROOTPATH=~/Documents/CAEN_Digitizer
SOURCEFILES=installation_files
CURRENT=$( pwd )


cd $ROOTPATH/$SOURCEFILES
linenumber=$(eval "sed -n '/uint64_t mymaximum/=' WaveDump.c") # search line with pathern
sed -i "$linenumber d" WaveDump.c
sed -i "$linenumber i \ \ \ \ uint64_t mymaximum = $npts; \/\/ Added by Henrique Souza" WaveDump.c


sleeptime=3
echo "Recompiling wavedump with a maximum of $npts waveforms"
echo ""
sleep $sleeptime

cd $ROOTPATH
cd $( /bin/ls | grep wavedump* )
cd src
#replacing the .c file with my custom one
cp $ROOTPATH/$SOURCEFILES/WaveDump.c .
cd ..

./configure
sudo make
sudo make install

cd $CURRENT
