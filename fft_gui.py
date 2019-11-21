###########################################################################
# program: fft_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.4
# date: September 12, 2013
# description:  FFT
#
###########################################################################
# 
# Note:  for use within Spyder IDE, set: 
#    
# Run > Configuration > Interpreter >
#    
# Excecute in an external system terminal
#
###########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename,askopenfilename

           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename,askopenfilename    

import os
import re
import numpy as np


import matplotlib.pyplot as plt

from scipy.fftpack import fft

from math import atan2

from sys import stdin

################################################################################

class tk_FFT:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.mstring=''
        self.num=0
        self.num_fft=0
        self.nhalf=0
        self.freq=[]
        self.ff=[]
        self.zz=[]
        self.z=[]
        self.ph=[]
        
        self.a=[]
        self.b=[]
        
        self.hwtext1=tk.Label(top,text='Fast Fourier Transform (FFT)')
        self.hwtext1.grid(row=0, column=0, columnspan=6, pady=7,sticky=tk.W)

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=1, column=0, columnspan=6, pady=7,sticky=tk.W)

################################################################################

        crow=2

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=7,sticky=tk.W)

################################################################################

        crow=3
        

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)  

################################################################################

        crow=4

        self.hwtext4=tk.Label(top,text='Mean Removal')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=7)

        self.hwtext5=tk.Label(top,text='Window')
        self.hwtext5.grid(row=crow, column=2, columnspan=1, pady=7)

################################################################################

        crow=5

        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "Yes")
        self.Lb1.insert(2, "No")
        self.Lb1.grid(row=crow, column=0, pady=4)
        self.Lb1.select_set(0) 

        self.Lb2 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb2.insert(1, "Rectangular")
        self.Lb2.insert(2, "Hanning")
        self.Lb2.grid(row=crow, column=2, pady=4)
        self.Lb2.select_set(0) 

################################################################################


        crow=6

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)
        self.hwtextf1.config(state='disabled')

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=2,padx=5, pady=8)
        self.hwtextf2.config(state='disabled')
        
################################################################################

        crow=7

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=5, pady=1)
        self.f1_entry.config(state='disabled')

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=2,padx=5, pady=1)
        self.f2_entry.config(state='disabled')

################################################################################

        crow=8

        self.button_calculate = tk.Button(top, text="Calculate FFT", command=self.fft_calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=2, padx=10,pady=20)

################################################################################

        crow=9

        self.s=tk.StringVar()
        self.hwtext5=tk.Label(top,textvariable=self.s)
        self.hwtext5.grid(row=crow, column=0, columnspan=3, pady=7)  

################################################################################

        crow=10

        self.hwtextext_exfft=tk.Label(top,text='Export FFT Data')
        self.hwtextext_exfft.grid(row=crow, column=0,pady=10)  
        self.hwtextext_exfft.config(state = 'disabled')

################################################################################
    
        crow=11

        self.button_fftm = tk.Button(top, text="Magnitude", command=self.export_fftm)
        self.button_fftm.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftm.grid(row=crow, column=0,columnspan=2, pady=1, padx=1)  

        self.button_fftmp = tk.Button(top, text="Magnitude & Phase", command=self.export_fftmp)
        self.button_fftmp.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftmp.grid(row=crow, column=2,columnspan=2, pady=1, padx=0) 

        self.button_fftc = tk.Button(top, text="Complex", command=self.export_fftc)
        self.button_fftc.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftc.grid(row=crow, column=4,columnspan=2, pady=1, padx=14) 
        
################################################################################


    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File')
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal') 
        
        self.hwtextf1.config(state='normal')
        self.hwtextf2.config(state='normal')
        self.f1_entry.config(state='normal')
        self.f2_entry.config(state='normal')
        
        out1='%8.4g' %(self.sr/2.)        
        
        self.f1r.set('0')  
        self.f2r.set(out1)          

################################################################################
        
    def fft_calculation(self):

        noct=int(np.log(self.num)/np.log(2))

        self.num_fft=2**noct
    
        dur_fft=self.a[self.num_fft-1]-self.a[0]

        bb=self.b[0:self.num_fft]
    
        imr=int(self.Lb1.curselection()[0]) 
        iw=int(self.Lb2.curselection()[0]) 

        if(imr==0 or iw==1):
            bb=bb-np.mean(bb)
    
        if(iw==1):
            H=self.Hanning_initial(self.num_fft)
            bb=bb*H    
    
        df=1/dur_fft
      
        self.z =fft(bb)

        self.nhalf=self.num_fft/2

        print (" ")
        print (" %d samples used for FFT " %self.num_fft)
        print ("df = %8.4g Hz" %df)

        self.zz=np.zeros(self.nhalf,'f')
        self.ff=np.zeros(self.nhalf,'f')
        self.ph=np.zeros(self.nhalf,'f')

        self.freq=np.zeros(self.num_fft,'f')

        self.z/=float(self.num_fft)

        for k in range(0,int(self.num_fft)):
            self.freq[k]=k*df
    
            self.ff=self.freq[0:self.nhalf]
        
    
        for k in range(0,int(self.nhalf)):    

            if(k > 0):			 
                self.zz[k]=2.*abs(self.z[k])
            else:    
                self.zz[k]= abs(self.z[k])

            self.ph[k]=atan2(self.z.real[k],self.z.imag[k])
  

        idx = np.argmax(np.abs(self.zz))        
 
        print (" ")
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])) 
        
        mstring=" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])
        self.s.set(mstring) 

        sx1= self.f1r.get()   
        sx2= self.f2r.get() 
  
        if sx1:
            if sx2:
                x1=float(sx1)  
                x2=float(sx2)  
    
        plt.ion()
        plt.close(2)
        plt.figure(2)     
        plt.plot(self.ff,self.zz)
        plt.grid(True)
        plt.title(' FFT Magnitude ')
        plt.ylabel(self.y_string.get()) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.draw()  

        plt.close(3)
        plt.figure(3)
        plt.plot(self.ff,self.ph*(180./np.pi))
        plt.grid(True)
        plt.title(' FFT Phase ')
        plt.ylabel(' Phase (deg) ')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])    
        plt.draw()  
    
        self.hwtextext_exfft.config(state = 'normal')
        self.button_fftm.config(state = 'normal')
        self.button_fftmp.config(state = 'normal')
        self.button_fftc.config(state = 'normal')    
    


    def export_fftm(self):
        output_file_path = asksaveasfilename(parent=root,\
                            title="Enter the output FFT filename (freq, mag): ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.nhalf,self.ff,self.zz,output_file) 

    def export_fftmp(self):
        output_file_path = asksaveasfilename(parent=root,\
                title="Enter the output FFT filename (freq, mag, phase(rad)): ")       
        output_file = output_file_path.rstrip('\n')
        WriteData3(self.nhalf,self.ff,self.zz,self.ph,output_file)

    def export_fftc(self):
        output_file_path = asksaveasfilename(parent=root,\
                              title="Enter the output FFT (freq, real, imag): ")           
        output_file = output_file_path.rstrip('\n')
        WriteData3(self.num_fft,self.freq,self.z.real,self.z.imag,output_file)
        
        
    @classmethod         
    def Hanning_initial(cls,mmm):
        H=np.zeros(mmm,'f')
        tpi=2*np.pi    
        alpha=np.linspace(0,tpi,mmm)
        ae=np.sqrt(8./3.)
        H=ae*0.5*(1.-np.cos(alpha))                
        return H     

################################################################################
    
################################################################################

     

def quit(root):
    root.destroy()

def read_two_columns_from_dialog(label):
    """
    Read data from file using a dialog box
    """ 
    while(1):

        input_file_path = askopenfilename(parent=root,title=label)

        file_path = input_file_path.rstrip('\n')
#
        if not os.path.exists(file_path):
            print ("This file doesn't exist")
#
        if os.path.exists(file_path):
            print ("This file exists")
            print (" ")
            infile = open(file_path,"rb")
            lines = infile.readlines()
            infile.close()

            a = []
            b = []
            num=0
            for line in lines:
#
                if sys.version_info[0] == 3:            
                    line = line.decode(encoding='UTF-8')    
                    
                if re.search(r"(\d+)", line):  # matches a digit
                    iflag=0
                else:
                    iflag=1 # did not find digit
#
                if re.search(r"#", line):
                    iflag=1
#
                if iflag==0:
                    line=line.lower()
                    if re.search(r"([a-d])([f-z])", line):  # ignore header lines
                        iflag=1
                    else:
                        line = line.replace(","," ")
                        col1,col2=line.split()
                        a.append(float(col1))
                        b.append(float(col2))
                        num=num+1
            break

            a=np.array(a)
            b=np.array(b)

            print ("\n samples = %d " % num)
            
    return a,b,num

def sample_rate_check(a,b,num,sr,dt):
    dtmin=1e+50
    dtmax=0

    for i in range(1, int(num-1)):
        if (a[i]-a[i-1])<dtmin:
            dtmin=a[i]-a[i-1];
            if (a[i]-a[i-1])>dtmax:
                dtmax=a[i]-a[i-1];

    print ("  dtmin = %8.4g sec" % dtmin)
    print ("     dt = %8.4g sec" % dt)
    print ("  dtmax = %8.4g sec \n" % dtmax)

    srmax=float(1/dtmin)
    srmin=float(1/dtmax)

    print ("  srmax = %8.4g samples/sec" % srmax)
    print ("     sr = %8.4g samples/sec" % sr)
    print ("  srmin = %8.4g samples/sec" % srmin)

    if((srmax-srmin) > 0.01*sr):
        print(" ")
        print(" Warning: sample rate difference ")
        sr = None
        while not sr:
            try:
                print(" Enter new sample rate ")
                s = stdin.readline()
                sr=float(s)
                dt=1/sr
            except ValueError:
                print ('Invalid Number')
    return sr,dt

########################################################################

def WriteData2(nn,aa,bb,output_file_path):
    """
    Write two columns of data to an external ASCII text file
    """
    output_file = output_file_path.rstrip('\n')
    outfile = open(output_file,"w")
    for i in range (0, int(nn)):
        outfile.write(' %10.6e \t %8.4e \n' %  (aa[i],bb[i]))
    outfile.close()

########################################################################


def WriteData3(nn,aa,bb,cc,output_file_path):
    """
    Write three columns of data to an external ASCII text file
    """
    outfile = open(output_file_path,"w")
    for i in range (0, int(nn)):
        outfile.write(' %8.4e \t %8.4e \t %8.4e \n' %  (aa[i],bb[i],cc[i]))
    outfile.close()

################################################################################
           
root = tk.Tk()

root.minsize(400,400)
root.geometry("600x550")

root.title("fft_gui.py ver 1.4  by Tom Irvine") 

tk_FFT(root)
root.mainloop()    