

# CAEN DIGITIZER

Author: Henrique Vieira de Souza, APC – Paris

henriquevieira.souza@gmail.com 


# Table of Contents


# Introduction

This documents servers do clarify and help the data acquisition with the CAEN digitizer. All the softwares and drivers are availabe at [caen.it](http:://caen.it). 

The acquisition is done with Wavedump, a free software distributed by CAEN. The versions modified by the me have two minor implementations: (1) continuous writing will save only 10,000 waveforms and stop and (2) one can change the number of points per waveform saved, this decreases the sampling rate from 2 ns to 4 ns, for example, by skipping one point.

Please, keep in mind that the implementation (2) will not reduce the acquisition rate of the digitizer, just of the saved waveforms. 

Wavedump will only save data in a file named wave0.dat when saving as BINARY (or wave0.txt when saving as ASCII). I am assuming you have wisely chosen binary as format. 
Wave0.dat refers to the waveforms of channel 0, while wave1.dat refers to channel 1.

If you want to save several .dat data files you need to move these waveX.dat files to another folder before saving new ones. As this task can be very tedious,  I’ve created a GUI with QtCreator to transfer the files and menage data taking more efficiently. The GUI is not mandatory, it should just make your life easier! 

Text in italic and quoted are commands you can copy and paste at the terminal.

Please, make sure you have “make” and “cmake” installed. The software “gnuplot” is also necessary but it will be installed in the installation scripts.
Please, if you find any bug, miss information or some nasty mistake, please feel free to talk to me by email.

`come codes`


# Wavedump


## Installation

![img](https://github.com/hvsouza/CAEN_Digitizer/blob/master/.repo_img/continuous_ex.png) 

