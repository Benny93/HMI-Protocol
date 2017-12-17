#!/usr/bin/python3
import time
import can
import constants as const
from random import uniform

"""
hmi controller prototype that acts like a server

"""
# TODO: Mapping is send by the requesting app-controller
response_id_by_sender_id = {const.NAV_HMI_REQ: const.NAV_HMI_RESP,
                            const.AC_HMI_REQ: const.AC_HMI_RESP,
                            const.CDP_HMI_REQ: const.CDP_HMI_RESP}

ctlr_name_by_arbitration_id = {const.NAV_HMI_REQ: "Navigation App Controller",
                               const.AC_HMI_REQ: "Air Conditioning App Controller",
                               const.CDP_HMI_REQ: "CD Player App Controller"}
req_name_by_req_code = {const.NAV_REQ_DESTINATION: "Set Destination",
                        const.AC_REQ_TEMPERATURE: "Set Temperature",
                        const.CDP_REQ_TRACK_NO: "Set Track Number"}

bustype = 'socketcan_native'
channel = 'vcan0'

bus = can.interface.Bus(channel=channel, bustype=bustype)
server_timeout = 10


# TODO: Catch if instance fails

def send_frame(data, arbitraton_id):
    """
    Answers with a response
    :param arbitraton_id: Identifier of the request
    :param data:
    :return:
    """
    identifier = response_id_by_sender_id[arbitraton_id]
    # print('Sending a reply to the application controller with id: {} answer on {}'.format(arbitraton_id, identifier))
    msg = can.Message(arbitration_id=identifier, data=data, extended_id=False)
    # print(msg)
    # wait until ready to send
    bus.send(msg)


def acquire_user_input(request_code):
    """
    Stub
    :param request_code:
    :return: predefined test user inputs
    """
    if request_code == const.NAV_REQ_DESTINATION:
        return "Schwaerzlocherstrasse 109, Tuebingen"
    if request_code == const.AC_REQ_TEMPERATURE:
        return "25"
    if request_code == const.CDP_REQ_TRACK_NO:
        return "4"
    return "missing test user input"


def create_frames(user_input):
    # create byte array from user input
    msg_bytes = bytearray(user_input, "utf-8")
    payload_length = 5
    chunks = [msg_bytes[x:x + payload_length] for x in range(0, len(msg_bytes), payload_length)]
    frames = []
    for i in range(0, len(chunks)):
        frame = [const.DATA, i]
        for b in chunks[i]:
            frame.append(b)
        frames.append(frame)
    if len(frames) is 0:
        return None
    return frames


def send_mulipart_data(frames, arbitration_id, tries):
    if tries > 2:
        # too many timeouts: listen for new request
        process_request(listen(const.REQUEST))
    for i in range(0, len(frames)):
        send_frame(frames[i], arbitration_id)
        # Wait for data ack
        data_ack = listen(const.ACK, server_timeout)
        if data_ack is None:
            # timeout
            send_mulipart_data(frames[i:], arbitration_id, tries + 1)
            return


def process_request(msg):
    # optional check to accept request
    # send request accept
    ctlr_arbitration_id = msg.arbitration_id
    timeout = 100
    request_code = msg.data[2]
    data = [const.REQUEST_ACK, msg.data[1] + 1, timeout]
    send_frame(data, ctlr_arbitration_id)
    # wait for ack of app controller
    ack = listen(const.ACK, server_timeout)
    if ack is None:
        # timeout while waiting for ack, return to listen
        return process_request(listen(const.REQUEST))
    # process the request
    print('Processing the Request with code {}:"{}" by {}'.format(request_code, req_name_by_req_code[request_code],
                                                                  ctlr_name_by_arbitration_id[ctlr_arbitration_id]))
    # time.sleep(uniform(0.5, 2.0))
    time.sleep(3)
    user_input = acquire_user_input(request_code)
    data_frames = create_frames(user_input)
    # send response info
    resp_num_frames = len(data_frames)
    resp_frames_between_ack = 3
    resp_timeout = 100
    pid = msg.data[1] + 1
    resp_info = [const.RESPONSE_INFO, pid, resp_num_frames, resp_frames_between_ack, resp_timeout]
    send_frame(resp_info, ctlr_arbitration_id)
    info_ack = listen(const.ACK, server_timeout)
    if info_ack is None:
        # timeout: continue listen for requests
        return process_request(listen(const.REQUEST))
    # send data
    print("Sending Data...")
    send_mulipart_data(data_frames, ctlr_arbitration_id, 1)
    # Send Fin
    fin = [const.REQUEST_FIN, pid + 1]
    send_frame(fin, ctlr_arbitration_id)
    fin_ack = listen(const.ACK, server_timeout)
    # TODO: Session close is not considered in this prototype yet
    # if fin_ack is None:
    # fin ack not received
    # TODO: try again to close session
    #   listen()
    # session done, continue serving
    # process next request
    process_request(listen(const.REQUEST))


def listen(expected_type=None, timeout=0):
    """
        blocking read on the bus
        no timeout
        :returns message of expected type
    """
    if expected_type == const.REQUEST:
        print("Awaiting app controller request...")

    if timeout < 0:
        # timeout
        print("Timeout for expected frame")
        return None
    if timeout == 0:
        # non blocking timeout
        timeout = None
    start_time = time.time()
    msg = bus.recv()
    elapsed_time = time.time() - start_time
    if msg is None:
        # timeout
        print("Timeout! ")
        return None
    elif expected_type is not None and msg.data[0] != expected_type:
        # frame did not match session
        # drop frame and continue listen
        # print("received {}, expected {}".format(expected_type,msg.data[0]))
        return listen(expected_type, timeout - elapsed_time)
    else:
        # print("Received msg")
        # print(msg)
        return msg


try:
    process_request(listen(const.REQUEST))
except KeyboardInterrupt:
    print("Received keyboard interrupt. Exiting...")
