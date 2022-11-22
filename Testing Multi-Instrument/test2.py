from moku.instruments import (MultiInstrument, Oscilloscope, WaveformGenerator,
ArbitraryWaveformGenerator,  SpectrumAnalyzer, LockInAmp, FrequencyResponseAnalyzer)
import json
import matplotlib.pyplot as plt
import time 

import numpy as np
import scipy.stats as stats


#Read the Connections file
with open('connections.txt') as f:
    data = f.read()
global connections
connections = json.loads(data)

#Init the Instrument 
Instrument = [[], [] , [] ,[]]
Moku = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', platform_id=4,force_connect = True)

Instr = ['WaveformGenerator', 'Oscilloscope','Oscilloscope','WaveformGenerator']

#Set up the Instruments 

wvg1 = Moku.set_instrument(1, WaveformGenerator)
osc1 = Moku.set_instrument(2, Oscilloscope)
osc2 = Moku.set_instrument(3, Oscilloscope)
wvg2 = Moku.set_instrument(4, WaveformGenerator)

#Set up the connections
Moku.set_connections(connections= connections)       

#Create a wave and measure that wave
w1.generate_waveform(1,'Sine')
w1.generate_waveform(2,'Sine')
w2.generate_waveform(1,'Sine')
w2.generate_waveform(2,'Sine')

o1.set_timebase(0,1e-3)
o2.set_timebase(0,1e-3)

#measure the wave using both oscilloscopes
for i in range(10):
    print(i)
    data1 = o1.get_data()
    data2 = o2.get_data()
    time.sleep(1)
    fig, axs = plt.subplots(2)
    fig.suptitle('Test Changing in Mult-Instrument')
    axs[0].plot( data1['time'], data1['ch1'])
    axs[1].plot(data2['time'], data2['ch1'])
    plt.savefig('test1.jpg')
    
    
  
Moku.relinquish_ownership()
