"""
Protocol Constants

"""

"""
Message Codes
First Byte of Frame payload contains the messages code
"""
# TODO: Does not need a full byte to be transfered
REQUEST = 0
REQUEST_ACK = 1
ACK = 2
RESPONSE_INFO = 3
DATA = 4
REQUEST_FIN = 5

"""
IDs
For a better performance:
Lower IDs are better than higher IDs

Identifier should dynamically match priority.
This is ignored here for simplicity
"""

LOW_PRIO = 0xffffffff

# Navigation
NAV_HMI_RESP = 0x000001
NAV_HMI_REQ = 0x000011

# air conditioning
AC_HMI_RESP = 0x000002
AC_HMI_REQ = 0x000021

"""
Request Codes
"""
# Navigation
NAV_REQ_DESTINATION = 10

# Air conditioning
AC_REQ_TEMPERATURE = 20
