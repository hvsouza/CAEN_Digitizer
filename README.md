
# Table of Contents

1.  [Introduction](#orgbac2816)
2.  [Table of Contents](#org5d1443b)
3.  [Wavedump](#org850d290)
    1.  [Installation](#org76b3243)
    2.  [Configuration file](#org4392d9b)
    3.  [Using wavedump](#org4e52e78)
    4.  [Debugging USB](#org2fef6d5)
4.  [QtCreator GUI](#orgc2cc6b1)
    1.  [Installation](#orgb14eec1)
    2.  [Creating the project](#org2692da2)
    3.  [Debugging installation](#org3262dba)
    4.  [Using the GUI](#org5522997)
5.  [Extra: Creating a shortcut for Wavedump](#orgb5472d6)
6.  [Extra: Wavedump decreased sampling](#orgf48dab8)
7.  [Extra: File structure](#org93c9447)
8.  [Extra: Common variables](#orgbe522ce)



<a id="orgbac2816"></a>

# Introduction

Author: Henrique Vieira de Souza, APC – Paris   
henriquevieira.souza@gmail.com 

This documents servers do clarify and help the data acquisition with CAEN digitizers. All the softwares, drivers and manuals are availabe at [caen.it](http:://caen.it). 

The acquisition is done with Wavedump, a free software distributed by CAEN. The versions modified by me have two minor implementations: (1) continuous writing will save only 10,000 waveforms and stop and (2) one can change the number of points per waveform saved, this decreases the sampling rate from 2 ns to 4 ns, for example, by skipping one point.

Please, keep in mind that the implementation (2) will not reduce the acquisition rate of the digitizer, just of the saved waveforms. 

If you search "Added by Henrique Souza" in the WaveDump.c file, you will find all the modifications made by me.

Wavedump saved data in a file named `wave0.dat` when saving as BINARY (or `wave0.txt` when saving as ASCII). I am assuming you have wisely chosen binary as format.  
`wave0.dat` refers to the waveforms of channel 0, while `wave1.dat` refers to channel 1.

If you want to save several .dat data files you need to move these `waveX.dat` files to another folder before saving new ones. As this task can be very tedious,  I’ve created a GUI with QtCreator to transfer the files and menage data taking more efficiently. The GUI is not mandatory, it should just make your life easier! 

Please, make sure you have “make” and “cmake” installed. The software “gnuplot” is also necessary but it will be installed in the installation scripts.

Please, if you find any bug, miss information or some nasty mistake, feel free to talk to me by email.


<a id="org5d1443b"></a>

# Table of Contents

-   [BROKEN LINK: introduction]
-   [BROKEN LINK: table-of-contents]
-   [BROKEN LINK: wavedump]
    -   [BROKEN LINK: installation]
    -   [BROKEN LINK: configuration-file]
    -   [BROKEN LINK: using-wavedump]
    -   [BROKEN LINK: debugging-usb]
-   [BROKEN LINK: qtcreator-gui]
    -   [BROKEN LINK: installation]
    -   [BROKEN LINK: creating-the-project]
    -   [BROKEN LINK: debugging-installation]
    -   [BROKEN LINK: using-the-gui]
-   [BROKEN LINK: extra-creating-a-shortcut-for-wavedump]
-   [BROKEN LINK: extra-wavedump-decreased-sampling]
-   [BROKEN LINK: extra-file-structure]
-   [BROKEN LINK: extra-common-variables]


<a id="org850d290"></a>

# Wavedump


<a id="org76b3243"></a>

## Installation

Clone this repositiory inside the "Documents" folder:

    cd ~/Documents
    git clone https://github.com/hvsouza/CAEN_Digitizer.git
    cd CAEN_Digitizer

To install the digitizer drivers and wavedump there are a few requirements and steps. I invite the user to read the manual of the digitizer and wavedump and also to search about the installation.

  The script `caen_installation.sh` will install the required softwares and drivers and applied the changes to customize to the version created by me. As this is done in a single step, there will be 3 seconds pause so you can check for errors output. If you see any, please, try to fix it before installing everything.   
NOTE: you need to disable “Secure Boot” at the BIOS.

    ./caen_installation.sh

If you are installing for the first time, you probably need to restart the computer.  
If the digitizer is connected and installation was successfully, open a terminal and just type “wavedump”, it should show you something like this output:

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/startup_ex.png)

Wavedump cannot run if there is no ADC connected. If wavedump failed to start, try to reboot the digitizer.

The script has also created the folder: `~/Desktop/WaveDumpData`. To use the GUI, you need to execute wavedump while inside that folder, so wavedump will save the data there. 

You can create a shortcut to execute Wavedump inside the correct folder, you can find instructions at0 [BROKEN LINK: extra-creating-a-shortcut-for-wavedump]

If you want to enable the option to decrease wavedump writing sample rate, please look at [BROKEN LINK: extra-wavedump-decreased-sampling]


<a id="org4392d9b"></a>

## Configuration file

Please, refer to the wavedump manual to better understand the acquisition configuration.

The configuration file of wavedump is located at `/etc/wavedump/WaveDumpConfig.txt`.   
If you cd in the WaveDumpData folder `cd ~/Desktop/WaveDumpData` and execute `./WaveDumpExe.sh`, the configuration file should open together with wavedump.

The current important parameters to take care are reported at [BROKEN LINK: extra-common-variables].


<a id="org4e52e78"></a>

## Using wavedump

Using wavedump is quite simple, just type `wavedump` at the terminal. By pressing [SPACE] the help menu is printed as bellow. Please keep in mind that [T] means “shift + t key”, for instance.

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/help_ex.png)

The ones you will use most are:   
Test&#x2026;   

Why?   
[R]\\
[s]  
[w] (repeating this will overwrite the file with only one waveform)   
[W] (After the 10,000 events you can press it again to save 10,000 more and so on)   
[P] also [p]   
[T] also [t]

Please, take a time to understand the acquisition by playing around and making some plots before moving forward. Make sure you memorize the shortcuts.

When pressing [W], my modifications will save 10,000 waveforms in the .dat files. When it finishes, you should see this in your screen: 

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/continuous_ex.png)

When you press [P] for continuous plot, what can happen is that gnuplot window will keep in your way (that is very annoying!). One way to stop this is to make sure that the plot is not over the windows you are trying to use, for example the terminal. If the windows are not overlapping you should be able to use the it normally. Another way is to enable “Prevent windows which require attention from stealing focus” (search this configuration for your Linux distribution). 

For using the GUI, the user should do the following during the acquisition:   
Assuming you have [s] already running, user’s chosen setup done and triggering events.

[w] create a .dat file   
[w] make sure you have created it (you can even press [w] once again.   
[W] save 10,000 or as many waveforms you want   
Move the .dat files by yourself or with GUI (see [BROKEN LINK: using-the-gui])   
For acquire more data, repeat this. 

If you want to understand the binary file structure, please check [BROKEN LINK: extra-file-structure]. 


<a id="org2fef6d5"></a>

## Debugging USB

Some times, the digitizer will not be recognized by the computer (this usually happens after using different digitizers, usb devices or cables). One way to fix it:

Disconnect the digitizer, turn it off 

    cd ~/Documents/ CAEN_Digitizer
    ./fix_usb.sh

Connect the digitizer and turn it on. Cross your fingers and try again. 


<a id="orgc2cc6b1"></a>

# QtCreator GUI


<a id="orgb14eec1"></a>

## Installation

Requirements to install QtCreator:   
`sudo apt-get update && sudo apt-get upgrade`   
`sudo apt-get -y install build-essential openssl libssl-dev libssl1.0 libgl1-mesa-dev libqt5x11extras5`

Install QtCreator following the instructions (<https://www.qt.io/download-qt-installer>).


<a id="org2692da2"></a>

## Creating the project

Open QtCreator, click at "Open Project" at the right side options (bellow Create Project), open the file `Documents/QtCreator/move_files/move_file.pro` and click at Configure Project.

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/qtcreator_proj.png)

Now, on the bottom left, change the building from Debug to Release. Run the project (Green arrow or Ctrl+R). 

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/qtcreator_release.png)

This should pop the project in the screen, close it and close the project.    
Now, navigate to WaveDumpData `cd ~/Desktop/WaveDumpData` and run the GUI by executing `. ./move_files.sh` the GUI window should pop-out, by executing this way the terminal is closed but the GUI keeps running.    


<a id="org3262dba"></a>

## Debugging installation

If the GUI did not pop-out after executing move<sub>files.sh</sub>, check that the file `~/Documents/QtCreator/build-move_files-Desktop_Qt_6_2_4_GCC_64bit-Release` exist.   
If the name of the file is different, you need to update it at `~/Desktop/WaveDumpData/move_files.sh`


<a id="org5522997"></a>

## Using the GUI

The GUI is just an interface to automatically move files from the WaveDumpData folder to another folder. It will keep a track of run and subrun number for you naming it with a standard. “Run” is the run number, “subrun” is the subrun number, “Voltage” is the bias voltage of the SiPMs (always leave a number with one or two decimal numbers only), “Threshold” is the the threshold set at the ADC (this should always be a integer number). “Trigger Ch” is the channel in which you are triggering, HOWEVER, the field there can be any text, so you can write, for instance, “Ch0<sub>and</sub><sub>Ch1</sub>” or even include some extra information and write something like this “Ch0<sub>and</sub><sub>Ch1</sub><sub>cosmic</sub><sub>run</sub><sub>after</sub><sub>lunch</sub><sub>break</sub>”. “Extra info” is any extra information that will be written at the end of the files (not folders), see bellow. 

In the example bellow, the GUI will create a folder named `new_data` at `~/Documents/ADC_data/coldbox_data` (the lock option is just to not change the name by mistake, you don’t need to lock it).   
After taking data with two channels, for example, you should have “wave0.dat” and “wave1.dat” at WaveDumpData.

When pressing “Move files”, a folder named “run0<sub>42V30</sub><sub>20ADC</sub><sub>Ch0</sub>” will be created (note: “extra info” will not be placed in the name of the folder), inside the folder “new<sub>data</sub>” and the two files will be moved there as:   
0<sub>wave0</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>   
0<sub>wave1</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>   
(note: if you have written “some<sub>comments</sub>” at the “Extra info” field, the name of the file would be “0<sub>wave0</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0</sub><sub>some</sub><sub>comments</sub> .dat)

In the GUI, the subrun number should have been changed from 0 to 1. If you take another set of data and click “Move files” again, you should have now four files in total named as:   
0<sub>wave0</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>   
0<sub>wave1</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>   
1<sub>wave0</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>   
1<sub>wave1</sub><sub>42V30</sub><sub>20ADC</sub><sub>Ch0.dat</sub>

And subrun should be equal 2.

Whenever you are finished with this run (lets say, changing SiPM bias, threshold or just because you want a different run in which you will give details on a README file later), you click “Finish run”, a message will pop-out saying “Warning: calibration might not exist. Finish run anyway?”, if you are not using the calibration “feature” you can just click “yes”.    
(otherwise click “no” and take the calibration that you forgot) 

This should put subrun back to 0 and Run now will be equal 1. 

(A way to play with the GUI is to simply create empty waveX.dat files and transfer they to see the structure of the data). 

The Calibration tab will simply transfer the file to a folder named “Calibration” inside the current run folder. It can only support one Calibration file per channel. This is an old and unused feature that I used for placing the waveforms that I would use for the SiPM gain estimation, I would not bother using it and just creating a new “Run” as calibration.    
At “More”, if you have data with different extension of .dat, you can change to anything you need (“.txt”, “.csv”, “.pdf”, etc).

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/qtcreator_gui.png)

Please, keep in mind the the run and subrun numbers can be changed by hand. So if you commit any mistake you can change the value back there, however, the move is done with the tag “-n” so the data is not overwritten, if you need to replace subrun 0, for instance, delete the wrong one first. 


<a id="orgb5472d6"></a>

# Extra: Creating a shortcut for Wavedump

Inside the folder `~/Documents/CAEN_Digitizer/installation_files/install_by_hand` you will find the file WaveDump.desktop. Replace the user from “henrique” to yours. Copy the .desktop file into `~.local/share/applications/` (the tumbnail should be already placed at `~/Pictures`. Now, of you open the menu (windows key) and search for CAEN you should find the shortcut (if not, try login out and login in). You can place this short cut at your dock/panel, this makes much easier to launch wavedump in a way that is saves the data at `~/Desktop/WaveDumpData/`. 


<a id="orgf48dab8"></a>

# Extra: Wavedump decreased sampling

If you want to decrease the sampling rate of the saved data, for example from 500 MS/s to 250 MS/s, or to 125 MS/s and so on, you need to edit the WaveDump.c file and "enable" my modifications. 

    cd ~/Documents/CAEN_Digitizer/wavedump-3.10.4/src

Open the file WaveDump.c, set the factor which you want to devide the sample rate at line 1511:

    int factor = 2; // Added by Henrique Souza

comment line 1537:

    // ns = (int)fwrite(Event16->DataChannel[ch] , 1 , Size*2, WDrun->fout[ch]) / 2;

and uncomment lines 1540 to 1546:

    /* Added by Henrique Souza */
    /* This allows to write at half of the rate*/  
    ns = 0;
    int aux = 0;
    for(j=0; j<Size; j++) {
      if(aux < 1) ns += (int)fwrite(&Event16->DataChannel[ch][j] , 1 , 2, WDrun->fout[ch])*(factor-1);
      else if (aux == (factor-1)) aux = -1;
      aux++;
    }
    /* End of addition */

Now you just need to compile wavedump again:   
(**NOTE**: by doing this, WaveDumpConfig.txt will be overwritten with the default version. Make sure you backup your version if that is important)

    cd ~/Documents/CAEN_Digitizer/wavedump-3.10.4
    ./configure
    make
    sudo make install

Now, if your digitizer have 500 MHz and you set factor = 2, by setting 

    RECORD_LENGTH  5000

in the config file, wavedump will save 2500 points per waveform, spaced 4 ns instead of 2 ns. 


<a id="org93c9447"></a>

# Extra: File structure

The binary file structure is presented at the wavedump manual. Each waveform saved is composed by 6 headers (each header with 4 bytes) and `n = RECORD_LENGTH` (each point with 2 bytes). Here is an illustration:

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/data_structure.png)


<a id="orgbe522ce"></a>

# Extra: Common variables

Bellow are the the most used variables configuration at the /etc/wavedump/WaveDumpConfig.txt, not all variables are being displayed.

NOTE: In the example above, trigger is made with Ch0 and Ch1 as or. Ch0, Ch1 and Ch2 are acquired and Ch3  is not.    
Please note that the original config file doesn’t have the individual CHANNEL<sub>TRIGGER</sub> option.   
When acquiring with external trigger, one should set   
EXTERNAL<sub>TRIGGER</sub>   ACQUISITION<sub>ONLY</sub>   
and set to DISABLED each channel trigger.

    # OPEN: open the digitizer
    # options: USB 0 0      			Desktop/NIM digitizer through USB              
    OPEN USB 0 0 
    (if you have some USB devices connected, you might need to change this value to 1 or 2) 
    
    # RECORD_LENGTH = number of samples in the acquisition window
    RECORD_LENGTH  2000
    
    # POST_TRIGGER: post trigger size in percent of the whole acquisition window
    # options: 0 to 100
    # On models 742 there is a delay of about 35nsec on signal Fast Trigger TR; the post trigger is added to
    # this delay  
    POST_TRIGGER  50
    
    #PULSE_POLARITY: input signal polarity.
    #options: POSITIVE, NEGATIVE
    #
    PULSE_POLARITY  POSITIVE
    
    # EXTERNAL_TRIGGER: external trigger input settings. When enabled, the ext. trg. can be either 
    # propagated (ACQUISITION_AND_TRGOUT) or not (ACQUISITION_ONLY) through the TRGOUT
    # options: DISABLED, ACQUISITION_ONLY, ACQUISITION_AND_TRGOUT
    EXTERNAL_TRIGGER   DISABLED	
    
    # FPIO_LEVEL: type of the front panel I/O LEMO connectors 
    # options: NIM, TTL
    FPIO_LEVEL  NIM
    
    # OUTPUT_FILE_FORMAT: output file can be either ASCII (column of decimal numbers) or binary 
    # (2 bytes per sample, except for Mod 721 and Mod 731 that is 1 byte per sample)
    # options: BINARY, ASCII
    OUTPUT_FILE_FORMAT  BINARY
    
    # OUTPUT_FILE_HEADER: if enabled, the header is included in the output file data
    # options: YES, NO
    OUTPUT_FILE_HEADER  YES
    
    # ENABLE_INPUT: enable/disable one channel
    # options: YES, NO
    ENABLE_INPUT          NO
    
    #BASELINE_LEVEL: baseline position in percent of the Full Scale. 
    # POSITIVE PULSE POLARITY (Full Scale = from 0 to + Vpp)
    # 0: analog input dynamic range = from 0 to +Vpp 
    # 50: analog input dynamic range = from +Vpp/2 to +Vpp 
    # 100: analog input dynamic range = null (usually not used)*
    # NEGATIVE PULSE POLARITY (Full Scale = from -Vpp to 0) 
    # 0: analog input dynamic range = from -Vpp to 0 
    # 50: analog input dynamic range = from -Vpp/2 to 0 
    # 100: analog input dynamic range = null (usually not used)*
    #
    # options: 0 to 100
    BASELINE_LEVEL  50
    
    # TRIGGER_THRESHOLD: threshold for the channel auto trigger (ADC counts)
    # options 0 to 2^N-1 (N=Number of bit of the ADC)
    # *The threshold is relative to the baseline:
    # 	POSITIVE PULSE POLARITY: threshold = baseline + TRIGGER_THRESHOLD
    # 	NEGATIVE PULSE POLARITY: threshold = baseline - TRIGGER_THRESHOLD
    #
    TRIGGER_THRESHOLD      100
    
    # CHANNEL_TRIGGER: channel auto trigger settings. When enabled, the ch. auto trg. can be either 
    # propagated (ACQUISITION_AND_TRGOUT) or not (ACQUISITION_ONLY) through the TRGOUT
    # options: DISABLED, ACQUISITION_ONLY, ACQUISITION_AND_TRGOUT, TRGOUT_ONLY
    # NOTE: since in x730 boards even and odd channels are paired, their 'CHANNEL_TRIGGER' value
    # will be equal to the OR combination of the pair, unless one of the two channels of
    # the pair is set to 'DISABLED'. If so, the other one behaves as usual.
    CHANNEL_TRIGGER        DISABLED
    
    [0]
    ENABLE_INPUT           YES
    BASELINE_LEVEL         10
    TRIGGER_THRESHOLD      500
    CHANNEL_TRIGGER        ACQUISITION_ONLY
    
    [1]
    ENABLE_INPUT           YES
    BASELINE_LEVEL         10
    TRIGGER_THRESHOLD      500
    CHANNEL_TRIGGER        ACQUISITION_ONLY
    
    
    [2]
    ENABLE_INPUT           YES
    BASELINE_LEVEL         10
    TRIGGER_THRESHOLD      500
    CHANNEL_TRIGGER        DISABLED
    
    
    
    [3]
    ENABLE_INPUT           NO
    BASELINE_LEVEL         10
    TRIGGER_THRESHOLD      500
    CHANNEL_TRIGGER        DISABLED

