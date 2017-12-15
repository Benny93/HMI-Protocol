"""
Protocol Constants

"""

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
