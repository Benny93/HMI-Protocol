#!/usr/bin/python3
import can
import constants as const
from app_c import AppController, start_app

"""
Automobile air conditioning

"""


class AirConditioningApp(AppController):
    def __init__(self):
        self.filter = [{"can_id": const.AC_HMI_RESP, "can_mask": 0x7FF}]
        super().__init__()

    def listen_for_reply(self):
        super().listen_for_reply()

    def send_request(self):
        msg = can.Message(arbitration_id=const.AC_HMI_REQ, data=b'REQ', extended_id=False)
        print(str(msg))
        self.bus.send(msg)
        # when done sending
        self.listen_for_reply()

    def process_application_logic(self):
        super().process_application_logic()


start_app(AirConditioningApp())
