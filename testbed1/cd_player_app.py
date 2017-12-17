#!/usr/bin/python3
import time
import constants as const
from app_c import AppController, start_app


class CDPlayerApp(AppController):
    def __init__(self):
        self.filter = [{"can_id": const.CDP_HMI_RESP, "can_mask": 0x7FF}]
        self.request_arbitration_id = const.CDP_HMI_REQ
        super().__init__()

    def process_application_logic(self):
        for i in range(0, 10):
            temp = self.send_request(request_code=const.CDP_REQ_TRACK_NO)
            print("CD Track selected by user " + temp)
            time.sleep(1)


start_app(CDPlayerApp())