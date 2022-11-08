# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:09:51 2022

@author: Triton
"""
from moku.instruments import MultiInstrument
import json
Moku = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb0:0470%12]', platform_id=4,force_connect = True)
connections = Moku.get_connections()
print(connections)
with open('connections.txt', 'w') as f:
    f.write(json.dumps(connections))