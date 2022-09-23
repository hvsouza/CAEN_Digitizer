#!/bin/bash

if [ -z $1 ]; then
    npts=10000
else
    npts=$1
fi

if [ -z $2 ]; then
    factor=2
else
    factor=$2
fi

ROOTPATH=~/Documents/CAEN_Digitizer
CURRENT=$( pwd )


cd $ROOTPATH
cd $( /bin/ls | grep wavedump* )
cd src
linenumber=$(eval "sed -n '/uint64_t mymaximum/=' WaveDump.c") # search line with pathern
sed -i "$linenumber d" WaveDump.c
sed -i "$linenumber i \ \ \ \ uint64_t mymaximum = $npts; \/\/ Added by Henrique Souza" WaveDump.c

linenumber_factor=$(eval "sed -n '/int factor/=' WaveDump.c") # search line with pathern
sed -i "$linenumber_factor d" WaveDump.c
sed -i "$linenumber_factor i \ \ \ \ \ \ \ \ \ \ \ \ int factor = $factor; \/\/ Added by Henrique Souza" WaveDump.c



sleeptime=3
echo "Recompiling wavedump with a maximum of $npts waveforms and factor of $factor"
echo ""
sleep $sleeptime
cd ..


./configure
sudo make
sudo make install

cd $CURRENT
