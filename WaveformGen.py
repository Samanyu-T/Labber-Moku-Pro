# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:40:52 2022
Jai Ganesha

@author: Samanyu Tirumala
"""

from moku.instruments import WaveformGenerator
import numpy as np
import InstrumentDriver

def Prefix_Converter(prefix):
    if prefix == 'G':
        return 1e9
    elif prefix == 'M':
        return 1e6
    elif prefix == 'k':
        return 1e3
    elif prefix == '':
        return 1
    elif  prefix == 'm':
        return 1e-3
    elif  prefix == 'u':
        return 1e-6
    elif  prefix == 'n':
        return 1e-9
    elif  prefix == 'p':
        return 1e-12    
    
class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Instrument
        Instrument = WaveformGenerator('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', force_connect = True)
        
        #for i in range(1,5):
        #    text = ' - (Ch ' + str(i) + ')'        
        #    self.setValue('Function' + text, 'Off')        
        # for i in range(1,5):
        #     Instrument.generate_waveform(channel = i,
        #                                  type = 'Off')
        
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
        for i in range(1,5):
            Instrument.generate_waveform(channel = i,
                                         type = 'Off')
        Instrument.relinquish_ownership()

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""

                
        channel = int(self.getValue('Channel'))
        
        text = ' - Ch' + str(channel)
        
        func = self.getValue('Function' + text)
        modulation = self.getValue('Modulation' + text)
        
        if func == 'Off':
            Instrument.generate_waveform(channel = channel,
                                         type = func)
        
        elif func == 'Sine':
            amp = self.getValue('Amplitude' + text)
            freq = self.getValue('Frequency' + text)
            phase = self.getValue('Phase' + text)
            dc_offset = self.getValue('DC Offset' + text)
            Instrument.generate_waveform(channel = channel,
                                         type = func,
                                         amplitude=amp,
                                         frequency=freq,
                                         offset = dc_offset,
                                         phase = phase)
        
        elif func == 'Square':
            amp = self.getValue('Amplitude' + text)
            freq = self.getValue('Frequency' + text)
            phase = self.getValue('Phase' + text)
            duty = self.getValue('Duty Cycle' + text)
            dc_offset = self.getValue('DC Offset' + text)
            Instrument.generate_waveform(channel = channel,
                                         type = func,
                                         amplitude=amp,
                                         frequency=freq,
                                         phase= phase,
                                         offset = dc_offset,
                                         duty=duty)
            
        elif func == 'Ramp':
            amp = self.getValue('Amplitude' + text)
            freq = self.getValue('Frequency' + text)
            phase = self.getValue('Phase' + text)
            symm = self.getValue('Ramp Symmetry' + text)
            dc_offset = self.getValue('DC Offset' + text)
            Instrument.generate_waveform(channel = channel,
                                         type = func,
                                         amplitude=amp,
                                         frequency=freq,
                                         phase = phase,
                                         offset = dc_offset,
                                         symmetry=symm)
            
        elif func == 'Pulse':
            amp = self.getValue('Amplitude' + text)
            freq = self.getValue('Frequency' + text)
            phase = self.getValue('Phase' + text)
            edg_time = self.getValue('Edge Time' + text)
            dc_offset = self.getValue('DC Offset' + text)
            pulse_width = self.getValue('Pulse Width' + text)
            Instrument.generate_waveform(channel = channel,
                                         type = func,
                                         amplitude=amp,
                                         frequency=freq,
                                         phase = phase,
                                         edge_time=edg_time,
                                         offset = dc_offset,
                                         pulse_width = pulse_width)
            
            
        elif func == 'DC':
            dc = self.getValue('DC Level' + text)
            Instrument.generate_waveform(channel = channel,
                                         type = func,
                                         dc_level=dc)

        '''MODULATION SECTION'''
        
        if modulation == 0:
            Instrument.disable_modulation(channel = channel)
            
        else:
            
            modulation_type = self.getValue('Mod Type' + text)
            modulation_freq = self.getValue('Mod Freq' + text)
            
            if modulation_type == 'Amplitude':
                am_depth = self.getValue('AM Depth' + text)
                Instrument.set_modulation(channel=channel, 
                                          type='Amplitude', 
                                          source='Internal', 
                                          depth=am_depth,
                                          frequency= modulation_freq)
                
            elif modulation_type == 'Frequency':
                fm_depth = self.getValue('FM Depth' + text)
                freq = self.getValue('Frequency' + text)

                if fm_depth > freq:
                    fm_depth = freq
                    
                Instrument.set_modulation(channel=channel, 
                                          type='Frequency', 
                                          source='Internal', 
                                          depth=fm_depth,
                                          frequency= modulation_freq)
                
            elif modulation_type == 'Phase':
                pm_depth = self.getValue('PM Depth' + text)               
                Instrument.set_modulation(channel=channel, 
                                          type='Phase', 
                                          source='Internal', 
                                          depth=pm_depth,
                                          frequency= modulation_freq)          
                
            elif modulation_type == 'Burst':
                pass
            
            elif modulation_type == 'Sweep':
                pass
                

    def performGetValue(self, quant, options={}):
        
        '''Using the Summary() Function to determine the various parameters set
        on the Instrument'''
        summary = Instrument.summary()
        temp = summary.split('\n')
        val = []
        for i in range(len(temp)-1):
            val.append(temp[i].split(','))
        
        channel = int(quant.name[-1])
        
        if quant.name in ('Function - Ch1, Function - Ch2, Function - Ch3, Function - Ch4'):
            temp2 = val[channel][0].split(' ')
            value = temp2[-1]
            
            
        elif quant.name in ('Frequency - Ch1, Frequency - Ch2, Frequency - Ch3, Frequency - Ch4'):
            
            temp2 = val[channel][1].split(' ')
            prefix_str = temp2[-1].split('Hz')
            value_str = ''
            for i in range(1,len(temp2)-1):
                value_str = value_str + temp2[i]
            value = float(value_str)
            prefix = Prefix_Converter(prefix_str[0])
            value = prefix*value
            
            
            
        else:
            value = quant.getValue()
        return value
if __name__ == '__main__':
    pass

