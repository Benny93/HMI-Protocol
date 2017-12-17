#!/usr/bin/python3
import can
import time
import constants as const
from app_c import AppController, start_app

"""
Automobile air conditioning

"""


class AirConditioningApp(AppController):
    def __init__(self):
        self.filter = [{"can_id": const.AC_HMI_RESP, "can_mask": 0x7FF}]
        self.request_arbitration_id = const.AC_HMI_REQ
        super().__init__()

    def process_application_logic(self):
        for i in range(0, 5):
            print('Sending request "Set Temperature"')
            temp = self.send_request(request_code=const.AC_REQ_TEMPERATURE)
            print("Temperature selected by user " + temp)
            print('-' * 80)
            time.sleep(1)


start_app(AirConditioningApp())
