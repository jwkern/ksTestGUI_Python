"""
Name: Joshua W. Kern
Date: 5/1/17

This program works in congruence with kosmira3.o (written in fortran) 
to produce confidence intervals for the KS-test of a star given 
a list of g-mode pulsation periods. It loads a GUI interface 
in which a stars period list (columnar form) can be input. 

Randomized period lists over the same range and quantity of numbers as the 
star are generated and ran through the KS-test. 

The GUI allows the user to specify the 99.9%, 99%, 95%, or 90% 
confidence levels they wish to plot on the KS-test plot for the stars g-mode period list. 
"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import random
from tkinter import *

class GUIInter(Frame):
    """creates the GUI interface and its consequent methods"""
    def __init__(self):
        """sets up the window and widgets"""
        Frame.__init__(self)
        self.master.title("KS-Test")
        self.grid()
        frame1 = Frame(self)
        frame1.grid(row = 2, column = 0, columnspan = 2)

        """label and field for period list"""
        self._perLabel = Label(self, text = "Period List:")
        self._perLabel.grid(row = 1, column = 0)
        self._starLabel = Label(self, text = "Star Name:")
        self._starLabel.grid(row = 0, column = 0)
        self._perVar = StringVar()
        self._starname = StringVar()
        self._starEntry = Entry(self, textvariable = self._starname)
        self._starEntry.grid(row = 0, column = 1)
        self._perEntry = Entry(self, textvariable = self._perVar)
        self._perEntry.grid(row = 1, column = 1)

        """checkbutton for confidence intervals"""
        self.var999 = StringVar(value= "Off")
        cb = Checkbutton(frame1, text = "99.9%", variable=self.var999,
                         onvalue="On",offvalue="Off")
        cb.grid(row = 0, column = 0, pady = 2)

        self.var99 = StringVar(value= "Off")
        cb = Checkbutton(frame1, text = "99%", variable=self.var99,
                         onvalue="On",offvalue="Off")
        cb.grid(row = 0, column = 1, pady = 2)

        self.var95 = StringVar(value= "Off")
        cb = Checkbutton(frame1, text = "95%", variable=self.var95,
                         onvalue="On",offvalue="Off")
        cb.grid(row = 0, column = 2, pady = 2)

        self.var90 = StringVar(value= "Off")
        cb = Checkbutton(frame1, text = "90%", variable=self.var90,
                         onvalue="On",offvalue="Off")
        cb.grid(row = 0, column = 3, pady = 2)

        """creates button to intiate main loop"""
        self._button = Button(frame1,
                              text = "Generate KS-Plot",
                              command = self._run)
        self._button.grid(row = 1, column = 1, columnspan = 2, pady = 8, sticky = S)      

    def _run(self):
        """main loop for GUI"""
        global perVar
        global starname
        starname = self._starname.get()
        perVar = self._perVar.get()
        PeriodList().randlists()     #creates the random period lists
        PeriodList().starinput()     #creates input file for star
        PeriodList().randinput()     #creates input file for rand list
        Shell().randshell()          #creates call to KS test for rand list
        Shell().starshell()          #creates call to KS test for star list
        KS_test().randtest()         #executes KS test on rand list
        KS_test().startest()         #executes KS test on star list
        KS_test().minfind()          #finds the minimum KS stat of each rand KS test
        KS_test().confint()          #finds stated confidence intervals
        Shell().cleanshell()         #removes superfluous files
        sec, ksstat, thirdvar = np.loadtxt('ks_star.out', unpack = True)
        sec1, confint1 = np.loadtxt('confint99_9.txt', unpack = True)
        sec2, confint2 = np.loadtxt('confint99.txt', unpack = True)
        sec3, confint3 = np.loadtxt('confint95.txt', unpack = True)
        sec4, confint4 = np.loadtxt('confint90.txt', unpack = True)
        plt.plot(sec, ksstat)
        if self.var999.get() == "On":
            plt.plot(sec1, confint1, 'r--', linewidth = 2.0, label = '99.9%')
        if self.var99.get() == "On":
            plt.plot(sec2, confint2, 'r--', linewidth = 1.5, label = '99%')
        if self.var95.get() == "On":
            plt.plot(sec3, confint3, 'r--', linewidth = 1.0, label = '95%')
        if self.var90.get() == "On":
            plt.plot(sec4, confint4, 'r--', linewidth = 0.5, label = '90%')
        plt.legend(loc = 'lower right')
        plt.xlabel('Period Spacings (seconds)')
        plt.xlim(28, 302)
        plt.ylabel('KS-Statistic')
        plt.title('Kolmogorov-Smirnov Test of ' + starname)
        plt.show()                   #plots the KS-Test of the stars with conf. int.



class PeriodList(GUIInter):
    """creates methods used on period lists"""
    def __init__(self):
        """initializes variables"""
    def randlists(self):
        """creates 1000 randomized period lists of a specified length length"""
        j = 0
        while j < 1000:
            j = j + 1
            i = 0
            star = np.loadtxt(perVar, unpack = True)
            limit = len(star)
            while i < limit:
                i = i + 1
                a = random.randrange(3000, 10000, 1)
                file = open('rand' + str(j) + '.txt', 'a')
                file.write(str(a) + "\n")
                file.close()

    def starinput(self):
        """creates input file for star"""
        file = open('input_star.txt', 'a')
        file.write(perVar + '\n')
        file.write('8' + '\n')
        file.write('30' + '\n')
        file.write('300' + '\n')
        file.close()

    def randinput(self):
        """creates 1000 input files for 1000 random period lists"""
        k = 0
        while k < 1000:
            k = k + 1
            file = open('input' + str(k) + '.txt', 'a')
            file.write('rand' + str(k) + '.txt' + '\n')
            file.write('8' + '\n')
            file.write('30' + '\n')
            file.write('300' + '\n')
            file.close()


class KS_test(object):
    """performs the Kolmogorov-Smirnov test using input file parameters"""
    def __init__(self):
        """initializes variables"""

    def startest(self):
        """calls the shell script and runs the KS test on star"""
        subprocess.call(['chmod +x ks_gen_star.sh'], shell = True)
        subprocess.call(['./ks_gen_star.sh'], shell = True)

    def randtest(self):
        """calls the shell script and runs the KS test on random period lists"""
        m = 0
        subprocess.call(['chmod +x ks_gen_*.sh'], shell=True)
        while m < 1000:
            m = m + 1
            subprocess.call(['./ks_gen_' + str(m) + '.sh'], shell=True)

    def minfind(self):
        """finds the minimum KS statistic in each random KS test and saves them to a file"""
        n = 0
        file = open('min_ksstat.txt', 'a')
        while n < 1000:
            n = n + 1
            sec, ksstat, thirdvar = np.loadtxt('kosmira' + str(n) + '.out', unpack=True)
            min_ksstat = min(ksstat)
            file.write(str(min_ksstat) + '\n')
        file.close()

    def confint(self):
        """finds the 99.9%, 99%, 95%, and 90% condifidence intervals"""
        ksstat = np.loadtxt('min_ksstat.txt', unpack = True)
        ksstat.sort()
        global con99_9
        global con99
        global con95
        global con90
        con99_9 = ksstat[0]
        con99 = ksstat[9]
        con95 = ksstat[49]
        con90 = ksstat[99]
        file = open('confint99_9.txt', 'w')
        file.write('28 ' + str(con99_9) + '\n')
        file.write('302 ' + str(con99_9) + '\n')
        file.close()
        file = open('confint99.txt', 'w')
        file.write('28 ' + str(con99) + '\n')
        file.write('302 ' + str(con99) + '\n')
        file.close()
        file = open('confint95.txt', 'w')
        file.write('28 ' + str(con95) + '\n')
        file.write('302 ' + str(con95) + '\n')
        file.close()
        file = open('confint90.txt', 'w')
        file.write('28 ' + str(con90) + '\n')
        file.write('302 ' + str(con90) + '\n')
        file.close()



class Shell(object):
    """creates the shell scripts used to call KS test (kosmira3.o)"""
    def __init__(self):
        """initializes variables"""

    def randshell(self):
        """creates 1000 shell scripts which dictate to run the KS test"""
        l = 0
        while l < 1000:
            l = l + 1
            file = open('ks_gen_' + str(l) + '.sh', 'a')
            file.write('python ks_test.py < input' + str(l) + '.txt \n')
            file.write('mv kosmira.out kosmira' + str(l) + '.out \n')
            file.write('rm kosmir.out2 \n')
            file.close()

    def starshell(self):
        """creates shell script to run KS test on star"""
        file = open('ks_gen_star.sh', 'a')
        file.write('python ks_test.py < input_star.txt \n')
        file.write('mv kosmira.out ks_star.out \n')
        file.write('rm kosmir.out2 \n')
        file.close()

    def cleanshell(self):
        """creates and executes a shell script to remove superfluous files 
              after the minimum KS statistics have been found"""
        file = open('cleanup.sh', 'a')
        file.write('rm input*.txt \n')
        file.write('rm rand*.txt \n')
        file.write('rm ks_gen_*.sh \n')
        file.write('rm kosmir*.out \n')
        file.write('rm cleanup.sh \n')
        file.close()
        subprocess.call(['chmod +x cleanup.sh'], shell = True)
        subprocess.call(['./cleanup.sh'], shell = True)




def main():
    GUIInter().mainloop()         #calls GUI interface

main()
