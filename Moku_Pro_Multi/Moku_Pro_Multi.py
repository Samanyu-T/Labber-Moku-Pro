# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:44:28 2022

@author: Triton
"""

from moku.instruments import (MultiInstrument, Oscilloscope, WaveformGenerator,
ArbitraryWaveformGenerator,  SpectrumAnalyzer, LockInAmp, FrequencyResponseAnalyzer)

import numpy as np
import InstrumentDriver
import json

class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Moku
        Moku = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', platform_id=4,force_connect = True)
        global Instrument
        Instrument = [[], [] , [] ,[]]
        with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/connections.txt') as f:
            data = f.read()
        global connections
        connections = json.loads(data)

    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
        Moku.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        
        
        quant.setValue(value)
        
        
        slot = int(quant.name[-1])
        text_slt = ' - Slot' + str(slot)
        
        
        
        ''' Set up the Instruments in their desired Slots and allocate their 
            respective connections using the connections.txt file'''
            
        if quant.name.startswith('Instrument'):
            Instrument[slot-1] = Moku.set_instrument(slot=slot, 
                                                     instrument = eval(self.getValue('Instrument' + text_slt)))
            #Only set up the connections once there are instruments set up
            check = 0
            for i in range(len(Instrument)):
                if Instrument[i]:
                    check = check + 1
            if check == 4:
                Moku.set_connections(connections = connections)
                
                
        #Set up the parameters for the Oscilloscope
        elif quant.name.startswith('OSC') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
            
            timebase = self.getValue('OSC TimeSpan - ' + str(slot))
            Instrument[slot-1].set_timebase(0, timebase)
            
            
        #Set up the parameters for the Waveform Generator
        elif quant.name.startswith('WVG') and self.getValue('Instrument' + text_slt) == 'WaveformGenerator':
            
            channel = int(quant.name[6])
            text_wvg1 = 'WVG Ch' + str(channel) + ' '
            text_wvg2 = ' - ' + str(slot)
            
            func = self.getValue(text_wvg1 + 'Function' + text_wvg2)
            modulation = self.getValue(text_wvg1 + 'Modulation' + text_wvg2)
            
            if func == 'Off':
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func)
            
            elif func == 'Sine':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             offset = dc_offset,
                                             phase = phase)
            
            elif func == 'Square':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                duty = self.getValue(text_wvg1 + 'Duty Cycle' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase= phase,
                                             offset = dc_offset,
                                             duty=duty)
                
            elif func == 'Ramp':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                symm = self.getValue(text_wvg1 + 'Ramp Symmetry' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             offset = dc_offset,
                                             symmetry=symm)
                
            elif func == 'Pulse':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                edg_time = self.getValue(text_wvg1 + 'Edge Time' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                pulse_width = self.getValue(text_wvg1 + 'Pulse Width' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             edge_time=edg_time,
                                             offset = dc_offset,
                                             pulse_width = pulse_width)
                
                
            elif func == 'DC':
                dc = self.getValue(text_wvg1 + 'DC Level' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             dc_level=dc)

            '''MODULATION SECTION'''
            
            if modulation == 0:
                Instrument[slot-1].disable_modulation(channel = channel)
                
            else:
                
                modulation_type = self.getValue(text_wvg1 + 'Mod Type' + text_wvg2)
                modulation_freq = self.getValue(text_wvg1 + 'Mod Freq' + text_wvg2)
                
                if modulation_type == 'Amplitude':
                    am_depth = self.getValue(text_wvg1 + 'AM Depth' + text_wvg2)
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Amplitude', 
                                              source='Internal', 
                                              depth=am_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Frequency':
                    fm_depth = self.getValue(text_wvg1 + 'FM Depth' + text_wvg2)
                    freq = self.getValue('Frequency' + text_wvg2)

                    if fm_depth > freq:
                        fm_depth = freq
                        
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Frequency', 
                                              source='Internal', 
                                              depth=fm_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Phase':
                    pm_depth = self.getValue(text_wvg1 + 'PM Depth' + text_wvg2)               
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Phase', 
                                              source='Internal', 
                                              depth=pm_depth,
                                              frequency= modulation_freq)          
                    
                elif modulation_type == 'Burst':
                    pass
                
                elif modulation_type == 'Sweep':
                    pass
        
        #Set up the parameters for the Arbritrary Waveform Generator
        elif quant.name.startswith('AWG') and self.getValue('Instrument' + text_slt) == 'ArbitraryWaveformGenerator':
            
            channel = int(quant.name[6])
            text_1 = 'AWG Ch' + str(channel) + ' '
            text_2 = ' - ' + str(slot)
            
            if not self.getValue(text_1 +'Premade File?'+ text_2):
                
                x = eval(self.getValue(text_1 +'Range of x'+ text_2))
                wave = eval(self.getValue(text_1 + 'f(x) in Python'+ text_2))
                
            elif self.getValue(text_1 +'Premade File?'+ text_2):
                wave = np.genfromtxt(self.getValue(text_1 +'Filename'+ text_2))
                
            amp = self.getValue(text_1 + 'Amplitude' + text_2)
            freq = self.getValue(text_1 + 'Frequency' + text_2)
            sample_rate = self.getValue(text_1 +'Sample Rate'+ text_2)
            Instrument[slot-1].generate_waveform(channel=channel, sample_rate= sample_rate, lut_data=list(wave), 
                                         frequency=freq, amplitude=amp)
            
            if self.getValue(text_1 +'Modulate'+ text_2) == 'Burst':
                trigger_src = self.getValue(text_1 + 'Trigger Source' + text_2)
                trigger_mode = self.getValue(text_1 + 'Trigger Mode' + text_2)
                trigger_lvl = self.getValue(text_1 + 'Trigger Level' + text_2)
                input_rng = self.getValue(text_1 + 'Input Range' + text_2)
                burst_cycles = int(self.getValue(text_1 + 'Burst Cycles' + text_2))
    
                Instrument[slot-1].burst_modulate(channel = channel,
                                             trigger_source = trigger_src,
                                             trigger_mode=trigger_mode,
                                             burst_cycles=burst_cycles,
                                             trigger_level = trigger_lvl,
                                             input_range = input_rng)
                
                
            elif self.getValue(text_1 +'Modulate'+ text_2) == 'Pulse':
                dead_cyc = int(self.getValue(text_1 +'Dead Cycles'+ text_2))
                dead_volt = self.getValue(text_1 +'Dead Voltage'+ text_2)
                Instrument[slot-1].pulse_modulate(channel = channel, dead_cycles=dead_cyc, dead_voltage=dead_volt)


            elif self.getValue(text_1 +'Modulate'+ text_2) == 'Off':
                Instrument[slot-1].disable_modulation(channel=channel)
                
                
        return value 
    
    
    def performGetValue(self, quant, options={}):
        
        
        slot = int(quant.name[-1])
        text_slt = ' - Slot' + str(slot)        
        
        if quant.name.startswith('OSC Ch') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
            channel = int(quant.name[6])
            data = Instrument[slot-1].get_data()
            value = data['ch%d' % channel]
        else:
            value = quant.getValue()
            
        return value
                