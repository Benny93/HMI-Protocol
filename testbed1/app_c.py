#!/usr/bin/python3
import time
import can
import constants as const
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
    request_arbitration_id = const.LOW_PRIO

    def __init__(self, ):
        self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
        self.bus.set_filters(self.filter)

    def listen(self, expected_type=None, timeout=None):
        if timeout == 0:
            # blocking wait
            timeout = None

        msg = self.bus.recv(timeout=timeout)
        if msg is None:
            # timeout
            print("Timeout. Retry")
            return None
        elif len(msg.data) == 0:
            print("Data len is null")
            print(msg)
        elif msg.data[0] != expected_type:
            # continue listen
            return self.listen(expected_type, timeout)
        else:
            return msg

    def send_request(self, request_code=None):
        """
        :param request_code: code of the request
        :return: user input received via request
        """
        # assemble data
        data = [const.REQUEST, 0, request_code]
        self.send_frame(data)
        # when done sending
        req_ack = self.listen(const.REQUEST_ACK, self.recv_timeout)
        if req_ack is None:
            return self.send_request(request_code)
        # received req_ack, send ack
        #print("received req_ack, send ack")
        print ("Establishing Connection")
        self.send_ack(req_ack)
        # listen for response info
        timeout = req_ack.data[2]
        resp_info = self.listen(const.RESPONSE_INFO, timeout)
        if resp_info is None:
            # timeout, begin from start!
            # Cold start
            self.send_request(request_code)
            return
        resp_num_frames = resp_info.data[2]
        #print("received response_info, send ack")
        self.send_ack(resp_info)
        # start receiving data frames
        user_input = self.receive_multipart_msg(resp_num_frames)
        if user_input is None:
            print("Too many Timeouts while receiving data! Restarting Request")
            return self.send_request(request_code)
        print("Successful received user input")
        # TODO reasonable timeout
        # Close connection
        print("Closing connection")
        fin = self.listen(const.REQUEST_FIN)
        if fin is None:
            # fin timeout, not guarantee, that communication is complete: coldstart
            self.send_request(request_code)
        # ack session end
        self.send_ack(fin)
        return user_input

    def receive_data_frame(self, tries):
        if tries > 2:
            # two unsuccessfull tries
            return None
        data_frame = self.listen(const.DATA)
        if data_frame is None:
            print("Data Timeout!")
            return self.receive_data_frame(tries + 1)
        #print("Received Data")
        #print(data_frame)
        user_input = ""
        for i in range(2, len(data_frame.data)):
            user_input = user_input + chr(data_frame.data[i])
        # ack data
        self.send_ack(data_frame)
        return user_input

    def receive_multipart_msg(self, resp_num_frames):
        user_input = ""
        for i in range(0, resp_num_frames):
            data = self.receive_data_frame(1)
            if data is None:
                # timeout !
                return None
            user_input = user_input + data
        return user_input

    def send_frame(self, data):
        msg = can.Message(arbitration_id=self.request_arbitration_id, data=data, extended_id=False)
        #print("Sending frame:")
        #print(str(msg))
        self.bus.send(msg)

    def send_ack(self, msg):
        """
        Acknowledge the receiving of a message
        """
        data = [const.ACK, msg.data[1]]
        self.send_frame(data)

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
