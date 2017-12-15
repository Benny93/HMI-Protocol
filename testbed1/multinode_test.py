#!/usr/bin/python3
import time
import can

bustype = 'socketcan_native'
channel = 'vcan0'

def produce(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    for i in range(30):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], extended_id=False)
        bus.send(msg)
    # Issue #3: Need to keep running to ensure the writing threads stay alive. ?
    time.sleep(1)

def produceForever(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    while True:
        msg = can.Message(arbitration_id=id, data=b'SPAM', extended_id=False)
        bus.send(msg)

