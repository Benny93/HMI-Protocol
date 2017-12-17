#!/usr/bin/python3
import can
import constants as const
from app_c import AppController, start_app


class NavigationApp(AppController):
    def __init__(self, ):
        self.filter = [{"can_id": const.NAV_HMI_RESP, "can_mask": 0x7FF}]
        super().__init__()

    def listen(self, expected_type=None, timeout=None):
        msg = self.bus.recv(timeout=timeout)
        if msg is None:
            # timeout
            print("Timeout! ")
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
        print("received req_ack, send ack")
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
        print("received response_info, send ack")
        self.send_ack(resp_info)
        # start receiving data frames
        user_input = self.receive_multipart_msg(resp_num_frames)
        if user_input is None:
            print("Too many Timeouts while receiving data! Restarting Request")
            return self.send_request(request_code)

        print("Successful received user input: " + user_input)
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
        print("Received Data")
        print(data_frame)
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
        msg = can.Message(arbitration_id=const.NAV_HMI_REQ, data=data, extended_id=False)
        print("Sending frame:")
        print(str(msg))
        self.bus.send(msg)

    def send_ack(self, msg):
        """
        Acknowledge the receiving of a message
        """
        data = [const.ACK, msg.data[1]]
        self.send_frame(data)

    def process_application_logic(self):
        # Obtain destination from Driver
        self.send_request(request_code=const.NAV_REQ_DESTINATION)


start_app(NavigationApp())
