import math
import numpy as np
import matplotlib.pyplot as plt
#import sounddevice as sd
from scipy.fftpack import fft

t = np.linspace(0 , 3 , 12 * 1024)
octave3= [130.81,146.83,164.81,174.61]
octave4= [261.63,293.66,329.63,349.23]

n=3
i=0
x=0
Timeofnote= [0, 1.2, 1.6, 2]
noteduration=[1.3, 1 , 1.6, 0.2]
#iterate and generate signal for each note
while(i<n):
    currnote3= octave3[i]
    currnote4= octave4[i]
    Tstart= Timeofnote[i]
    Tlength= noteduration[i]
    Tend = Tstart+Tlength
    notes = np.sin(2* currnote3*np.pi*t) + np.sin(2* currnote4*np.pi*t)
    x= x + (notes*((t>=Tstart) & (t<= Tend)))
    i=i+1
    
N= 3*1024
f= np.linspace(0,512,int(N/2))
f1= octave3[3]
f2= octave4[0]

#frequency domain of sound
x_f = fft(x)
x_f= 2/N * np.abs(x_f[0:int(N/2)]) #only positive results 

#generating random noise frequencies
fn_1= np.random.randint(0,512,1)
fn_2= np.random.randint(0,512,1)
noise= np.sin(2*fn_1*np.pi*t) + np.sin(2*fn_2*np.pi*t)
x_n = x+noise

#frequency domain of sound + noise
x_nf = fft(x_n)
x_nf= 2/N * np.abs(x_nf[0:int(N/2)]) #only positive results


maxpeak = math.ceil(np.max(x_f))
j=0
frequency=[]
#iterate and add values > maxpeak to array
for j in range(0,np.size(x_nf),1):
    if(x_nf[j]>maxpeak):
        frequency=np.append(frequency,math.floor(f[j]))
    j= j+1

#remove frequencies higher than maxpeak
xfiltered= x_n-( (np.sin(2*frequency[0]*np.pi*t)) + (np.sin(2*frequency[1]*np.pi*t)) )

#frequency domain of filtered sound
x_nfiltered= fft(xfiltered)
x_nfiltered= 2/N * np.abs(x_nfiltered[0:int(N/2)])  #positive results only


#sd.play(x,3*1024) #play unfiltered
#sd.play(x_filtered,3*1024) #play filtered

plt.subplot(3,2,1)
plt.plot(t,x)
plt.xlabel("time no noise")
plt.subplot(3,2,2)
plt.plot(f,x_f)
plt.xlabel("frequency no noise")
plt.subplot(3,2,3)
plt.plot(t,x_n)
plt.xlabel("time noise")
plt.subplot(3,2,4)
plt.plot(f,x_nf)
plt.xlabel("frequency noise")
plt.subplot(3,2,5)
plt.plot(t,xfiltered)
plt.xlabel("Filtered time ")
plt.subplot(3,2,6)
plt.plot(f,x_nfiltered)
plt.xlabel("Filtered frequency")

"""
plt.figure()
plt.plot(t,x)
plt.xlabel("Song in time domain without noise")
plt.figure()
plt.plot(f,x_f)
plt.xlabel("Song in freq domain without noise")
plt.figure()
plt.plot(t,x_n)
plt.xlabel("Song in time domain with noise")
plt.figure()
plt.plot(f,x_nf)
plt.xlabel("Song in freq domain with noise")
plt.figure()
plt.plot(t,xfiltered)
plt.xlabel("Filtered Song in time domain")
plt.figure()
plt.plot(f,x_nfiltered)
plt.xlabel("Filtered Song in freq domain")
"""




