#!/usr/bin/python3

import can

bustype = 'socketcan_native'
channel = 'vcan0'
bus = can.interface.Bus(channel=channel, bustype=bustype)
try:
    while True:
        print(bus.recv())
except:
    # Possible interrupt received
    print("Stopped listening");
