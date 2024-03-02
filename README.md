___________________________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________________________
# ksTestGUI_Python

___________________________________________________________________________________________________________________________________________________________________
GENERAL DESCRIPTION:
This Python GUI is meant to create confidence intervals for the Kolmogorov-Smirnov test. !WARNING! Only works on Python 2.7 and its associated version of NumPy. If you do not have the appropriate package versions installed, this GUI will generate thousands of .txt and .sh and will not complete the clearing function. 

___________________________________________________________________________________________________________________________________________________________________
DATA DESCRIPTION:
The data for this GUI is a simple list of user generated numbers. In application, this list of numbers were pulsation periods from variable stars.   

___________________________________________________________________________________________________________________________________________________________________
CODE DESCRIPTION:
The code uses matplotlib, numpy, subprocess, random, and tkinter Python packages to compute the the 99.9%, 99%, 95%, or 90% confidence levels for a series of 
KS-tests. 

This program works in congruence with kosmira3.o (written in fortran) to produce confidence intervals for the KS-test of a list of g-mode pulsation periods. 
It loads a GUI interface in which a user specified period list (columnar form) can be input. 

Randomized period lists over the same range and quantity of numbers as the user's list are generated and imported into the KS-test.  

The results can be interpretted as the greatest magnitude KS statistic being attributed to the empirical spacing in the user's list. 

___________________________________________________________________________________________________________________________________________________________________
RUNNING THE CODE:
1) I just wouldn't. It's not harmful to your machine, just obnoxious. 

2) This is effectively a template for a new, functional GUI in the most recent Python version.

3) Seriously, don't run this unless you want to manually delete the thousands of .txt and .sh files it generates.

   
___________________________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________________________
