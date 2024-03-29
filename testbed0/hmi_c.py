#!/usr/bin/python3
import time
import can
from random import uniform

"""
hmi controller prototype that acts like a server

"""

bustype = 'socketcan_native'
channel = 'vcan0'

identifier = 0x0
bus = can.interface.Bus(channel=channel, bustype=bustype)


# TODO: Catch if instance fails

def send_response(data):
    """
    Answers with a response
    :param data:
    :return:
    """
    print('Sending a reply to the application controller')
    # TODO: split big messages into multiple
    msg = can.Message(arbitration_id=identifier, data=data, extended_id=False)
    # wait until ready to send
    bus.send(msg)
    # return listenining
    listen()


def process_msg(msg):
    """
    Processes received messages
    :param msg:
    :return:
    """
    print("Received msg:")
    print(str(msg))
    process_time = uniform(0.5, 3.0)
    time.sleep(process_time)
    data = b'RESP'
    send_response(data)


def listen():
    """
        blocking read on the bus
        no timeout

    """
    print("Listening...")
    msg = bus.recv()
    process_msg(msg)


try:
    listen()
except KeyboardInterrupt:
    print("Received keyboard interrupt. Exiting...")
