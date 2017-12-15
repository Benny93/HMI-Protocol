#!/bin/bash
sudo modprobe vcan
# Create a vcan network interface with a specific name
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up

#show details of vcan
ip -details -statistics link show vcan0
