#!/usr/bin/python3
import time
import can
from random import uniform

"""
Generic application controller for testing

"""


class AppController():
    bustype = 'socketcan_native'
    channel = 'vcan0'

    bus = None
    filter = [{"can_id": 0x0, "can_mask": 0x7FF}]
    recv_timeout = 5.0

    def __init__(self, ):
        self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
        self.bus.set_filters(self.filter)

    def listen_for_reply(self):
        print("Listening for reply")
        # TODO : Should send again if waited to long for a response (only wrong frames received)
        msg = self.bus.recv(timeout=self.recv_timeout)
        if msg is None:
            # timeout
            print("Timeout! ")
            self.send_request()
        else:
            # received msg from hmi controller
            # TODO: This does not work with multiple app controllers
            print("received reply from hmi controller")
            print(msg)
            # done listening
            # continue processing the application
            self.process_application_logic()


    def send_request(self):
        print('Sending a request to the hmi controller')
        # TODO: split big messages into multiple
        msg = can.Message(arbitration_id=0x0, data=b'REQ', extended_id=False)
        print(str(msg))
        # TODO: Manage timeout
        self.bus.send(msg)
        # when done sending
        self.listen_for_reply()

    def process_application_logic(self):
        process_time = uniform(0.5, 2.0)
        print('Processing app for {} seconds'.format(process_time))
        time.sleep(process_time)
        self.send_request()


def start_app(app):
    try:
        app.process_application_logic()
    except KeyboardInterrupt:
        print("Received keyboard interrupt. Exiting...")
