# Amorphous Semiconductors Analysis Library

This is a Python library created for my master thesis on amorphous semiconductors. It is composed by many files, each one to perform a different kind of analysis. 

At the moment it is possible to analyze capacitance - voltage, photocurrent and Kelvin Probe Force Microscopy data.

## Installation

To install simply write

	pip install AmorphSC
	
All dependecies should be automatically installed, but if something goes wrong it is possible to find the list in *AmorphSC.egg-info -> requires.txt*

If you want to update the installed package at the latest version use

	pip install --upgrade AmorphSC

## Structure

The package is divided into different files that can be used for both analysis and input/output. A detailed description of every function is present in the wiki.

Now a general description of every file will be given.

### in_out.py

This is a file that contains functions dedicated to input and output. For example with **import_file** it is possible to import more than one file per time with the same prefix and path. 
Here you can also find functions called **s** that can print any number in scientific notation.

### CV.py

This file contains all the functions to analyze CV data. It is possible to plot CV characteristics, density of states and more.

### photocurrent.py

This module contains functions to permorm analysis on photocurrent data. More in detail, it is possible to calculate photocurrent spectra, lamp spectra, tauc plots,...
 
