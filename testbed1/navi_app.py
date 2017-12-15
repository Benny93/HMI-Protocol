#!/usr/bin/python3
from app_c import AppController, start_app


class NavigationApp(AppController):
    def __init__(self, identifier):
        super().__init__(identifier)

    def listen_for_reply(self):
        super().listen_for_reply()

    def send_request(self):
        super().send_request()

    def process_application_logic(self):
        super().process_application_logic()

start_app(NavigationApp(0xc0ffe2))