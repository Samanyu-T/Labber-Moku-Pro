# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:15:40 2022

@author: Triton
"""

from moku.instruments import (MultiInstrument, Oscilloscope, WaveformGenerator,
ArbitraryWaveformGenerator,  SpectrumAnalyzer, LockInAmp, FrequencyResponseAnalyzer)
import json
import matplotlib.pyplot as plt
import time 

import numpy as np
import scipy.stats as stats


mu = 0
sigma = 1
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
wave = stats.norm.pdf(x, mu, sigma)

#Read the Connections file
with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/connections.txt') as f:
    data = f.read()
global connections
connections = json.loads(data)

#Init the Instrument 
Instrument = [[], [] , [] ,[]]
Moku = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', platform_id=4,force_connect = True)

Instr = ['WaveformGenerator', 'Oscilloscope','LockInAmp','FrequencyResponseAnalyzer']

#Set up the Instruments 
for i in range(len(Instrument)):
    Instrument[i] = Moku.set_instrument(slot=i+1, 
                                        instrument = eval(Instr[i]))

#Set up the connections
Moku.set_connections(connections= connections)       

#Create a wave and measure that wave
Instrument[0].generate_waveform(1,type = 'Sine', frequency = 1e2)
Instrument[1].set_timebase(0,1e-1)
time.sleep(1)
data1 = Instrument[1].get_data()

#wait 10 sec
time.sleep(1)

#Change the Wvg to an AWG
Instr = ['ArbitraryWaveformGenerator', 'Oscilloscope','LockInAmp','FrequencyResponseAnalyzer']

#Set up the Instruments 
for i in range(len(Instrument)):
    Instrument[i] = Moku.set_instrument(slot=i+1, 
                                        instrument = eval(Instr[i]))
    
Instrument[0].generate_waveform(channel=1, sample_rate= 'Auto', lut_data=list(wave), 
                             frequency=1e2, amplitude=1)
Moku.set_connections(connections= connections)       
#Read the data
time.sleep(1)

data2 = Instrument[1].get_data()

#Plot the data
fig, axs = plt.subplots(2)
fig.suptitle('Test Changing in Mult-Instrument')
axs[0].plot(data1['time'], data1['ch1'])
axs[1].plot(data2['time'], data2['ch1'])
plt.show()

Moku.relinquish_ownership()
