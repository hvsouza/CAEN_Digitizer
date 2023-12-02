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

if [ -x "$(command -v apt)" ]; then
    myapt=$(command -v apt)
elif [ -x "$(command -v yum)" ]; then
    myapt=$(command -v yum)
elif [ -x "$(command -v pacman)" ]; then
    myapt=$(command -v pacman)
else
    echo "Failed to find package manager. Please, edit the caen_digitizer.sh script"
    exit 1
fi


INSTALLPATH=Installation
PreInstall=PreInstallThis
SOURCEFILES=installation_files
ROOTPATH=$( pwd )
sleeptime=3

check_n_exec "sudo rm -r $INSTALLPATH"
check_n_exec "sudo rm -r wavedump*"


while true; do
    echo "What is the original sampling rate of the digitizer (in MSamples/s)?"
    read original_rate
    if [ -z "$original_rate" ]; then
       continue
    fi
    # echo "The original sampling rate is $original_rate MHz."

    echo "Do you want to change the sampling rate of the digitizer? (yes/no)"
    echo "NOTE: for the coldbox, data is being taking with 250 MSamples/s."
    read answer

    if [ "$answer" == "yes" ]; then
        echo "Enter the desired sampling rate (in MSamples/s):"
        read rate

        factor=$(echo "$original_rate / $rate" | bc -l)
        int_factor=$( LC_ALL=C printf '%.0f' "$factor" ) # some annoying thing about integer conversion

        if [ $(expr $int_factor % 2) -ne 0 ] || [ $int_factor -lt 1 ]; then
            echo "Error: Sampling rate must be changed by a factor of 2. Example:"
            echo "Original: $original_rate MSamples/s"
            echo "Set: $original_rate / 2 MHz, $original_rate / 4 MHz, etc."
        else
            echo "The new sampling rate is $rate MHz."
            echo "Sampling rate is being reduced by a factor of $int_factor."
            break
        fi
    else
        rate=$original_rate
        echo "The sampling rate will remain unchanged ($original_rate MSamples/s)."
        int_factor=1
        break
    fi
done

sleep $sleeptime


mkdir -p $INSTALLPATH/$PreInstall


cd $ROOTPATH/$SOURCEFILES

tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENComm* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENVMELib* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH/$PreInstall -xvf $( /bin/ls CAENUSB* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/$INSTALLPATH -xvf $( /bin/ls CAENUpgrader* | grep -e ".tgz" -e ".tar.gz" -e ".tar")
tar -C $ROOTPATH/$INSTALLPATH -xvf $( /bin/ls CAENDigitizer* | grep -e ".tgz" -e ".tar.gz")
tar -C $ROOTPATH/ -xvf $( /bin/ls *wavedump* | grep -e ".tgz" -e ".tar.gz")

echo "Installing cmake and build-essentials"
sudo $myapt install cmake build-essential
sleep $sleeptime

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
echo "Installing CAENDigitizer"
cd $ROOTPATH/$INSTALLPATH
cd $( /bin/ls | grep CAENDigitizer* )
sudo bash install_64

echo "CAENDigitizer hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing CAENUpgrader"
cd $ROOTPATH/$INSTALLPATH
cd $( /bin/ls | grep CAENUpgrader* )
./configure
sudo make
sudo make install


echo "CAENUpgrader hopefully installed, check for errors"
echo ""
sleep $sleeptime
echo "Installing Wavedump"
cd $ROOTPATH
cd $( /bin/ls | grep wavedump* )
cd src
#replacing the .c file with my custom one
cp $ROOTPATH/$SOURCEFILES/WaveDump.c .
linenumber_factor=$(eval "sed -n '/int factor/=' WaveDump.c") # search line with pathern
sed -i "$linenumber_factor d" WaveDump.c
sed -i "$linenumber_factor i \ \ \ \ \ \ \ \ int factor = $int_factor; \/\/ Added by Henrique Souza\r" WaveDump.c
cp $ROOTPATH/$SOURCEFILES/WDconfig.c .
cp $ROOTPATH/$SOURCEFILES/WDplot.c .
cp $ROOTPATH/$SOURCEFILES/WDconfig.h ../include/
cp $ROOTPATH/$SOURCEFILES/WaveDump.h ../include/
cd ..

echo "Installing gnuplot"
sudo $myapt install gnuplot
sleep $sleeptime

./configure
make
sudo make install

# replacing config file
cp -r $ROOTPATH/$SOURCEFILES/WaveDumpConfig.txt /etc/wavedump/
cp -r $ROOTPATH/$SOURCEFILES/WaveDumpConfig.txt .

# creates a shortcut at Desktop. The move_files GUI must be installed by hand
mkdir -p ~/Desktop/WaveDumpData
cp $ROOTPATH/$SOURCEFILES/WaveDumpExe.sh ~/Desktop/WaveDumpData/
> ~/Desktop/WaveDumpData/daq_gui.sh
echo '#!/bin/bash' >> ~/Desktop/WaveDumpData/daq_gui.sh
echo '' >> ~/Desktop/WaveDumpData/daq_gui.sh
echo "python3 $ROOTPATH/pythonQt/daq_gui.py &" >> ~/Desktop/WaveDumpData/daq_gui.sh


# copying file to create short cut
cp -r $ROOTPATH/$SOURCEFILES/install_by_hand/WAVEDump.png ~/Pictures


cd $ROOTPATH/pythonQt
> .state
echo "# Sampling rate set" >> .state
echo "$rate MSamples/s" >> .state
echo "# Sampling rate original" >> .state
echo "$original_rate MSamples/s" >> .state

cd $ROOTPATH
