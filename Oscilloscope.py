# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:52:19 2022

@author: Triton
"""

from moku.instruments import Oscilloscope
import numpy as np
import InstrumentDriver

class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Instrument
        Instrument = Oscilloscope('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', force_connect = True)
        Instrument.generate_waveform(1, 'Sine', amplitude=0.5, frequency=10e3)
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
 
        '''
        ch1 = self.getValue('Disable Input - Ch1')
        ch2 = self.getValue('Disable Input - Ch2')
        ch3 = self.getValue('Disable Input - Ch3')
        ch4 = self.getValue('Disable Input - Ch4')
        
        if ch1 == 1:
            Instrument.disable_input(1)
        elif ch2 == 1:
            Instrument.disable_input(2)
        elif ch3 == 1:
            Instrument.disable_input(3)
        elif ch4 == 1:
            Instrument.disable_input(4)
        '''
        
        time_span = self.getValue('Time Span')
        Instrument.set_timebase(0, time_span)
        
        
    def performGetValue(self, quant, options={}):
        
        data = Instrument.get_data()
        if quant.name in ('Data - Ch1', 'Data - Ch2', 'Data - Ch3', 'Data - Ch4'):
            channel = int(quant.name[-1])

            if self.getValue('Disable Input - Ch%d' % channel) == 0:
                value = data['ch%d' % channel]
            else:
                value = []
        elif quant.name in ('Time Span'):
            summary = Instrument.summary()
            temp = summary.split('\n')
            val = []
            for i in range(len(temp)-1):
                val.append(temp[i].split(','))
            
        return value
                
