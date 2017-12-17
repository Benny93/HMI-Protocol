#!/usr/bin/python3
import can
import time
import constants as const
from app_c import AppController, start_app


class NavigationApp(AppController):
    def __init__(self, ):
        self.filter = [{"can_id": const.NAV_HMI_RESP, "can_mask": 0x7FF}]
        self.request_arbitration_id = const.NAV_HMI_REQ
        super().__init__()

    def process_application_logic(self):
        # Obtain destination from Driver
        for i in range(0, 10):
            destination = self.send_request(request_code=const.NAV_REQ_DESTINATION)
            print ("Destination of user " + destination)
            time.sleep(1)


start_app(NavigationApp())
