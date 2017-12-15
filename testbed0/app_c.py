#!/usr/bin/python3
import time
import can
from random import uniform

"""
Generic application controller for testing

"""

bustype = 'socketcan_native'
channel = 'vcan0'

identifier = 0xc0ffee
bus = can.interface.Bus(channel=channel, bustype=bustype)


def listen_for_reply():
    print("Listening for reply")
    #TODO : Should send again if waited to long for a response (only wrong frames received)
    while True:
        msg = bus.recv(timeout=3.0)
        if msg is  None:
            # timeout
            print("Timeout! ")
            send_request()
            return
        if msg.arbitration_id == 0x0:
            # received msg from hmi controller
            # TODO: This does not work with multiple app controllers
            print("received reply from hmi controller")
            break;

    # done listening
    # continue processing the application
    process_application_logic()


def send_request():
    print('Sending a request to the hmi controller')
    # TODO: split big messages into multiple
    msg = can.Message(arbitration_id=identifier, data=b'REQ', extended_id=False)
    print(str(msg))
    # TODO: Manage timeout
    bus.send(msg)
    # when done sending
    listen_for_reply()


def process_application_logic():
    processTime = uniform(0.5, 2.0)
    print('Processing app for {} seconds'.format(processTime))
    time.sleep(processTime)
    send_request()


try:
    process_application_logic()
except KeyboardInterrupt:
    print("Received keyboard interrupt. Exiting...")
