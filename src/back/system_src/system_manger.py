import json
import os
import time
import requests
import socket
import threading
import logging
import uuid
import sys

sys.path.append(os.getcwd())

import system_src.device as device


class SystemManager:
    def __init__(self):
        self.active_devices = []
        self.device_id_counter = 0
        self.device_id_lock = threading.Lock()
        self.device_id_lock = threading.Lock()

    def register_active_device(self, device_name: str, device_location: str, device_ipv4: str, device_port: int):
        """
        注册活跃设备
        1- 检查device_ipv4是否已存在
        2- 如果存在, 则返回对应的设备id号
        3- 如果不存在, 则生成一个设备id号, 并返回
        4- 将设备信息存储到active_devices字典中
        """
        # 检查device_ipv4是否已存在 
        # 如果存在, 则返回对应的设备id号
        for active_device in self.active_devices:
            if active_device.ipv4 == device_ipv4:
                print(f"设备{device_ipv4}已存在")
                return active_device.device_id
        # 如果不存在，则生成一个设备id号，并返回
        device_id = str(uuid.uuid4().int)[:32]
        new_active_device = device.Device(device_id, device_name, device_location, device_ipv4, device_port)
        self.active_devices.append(new_active_device)
        return device_id
    
    def test_register_active_device(self, device_name, device_location, device_ipv4, device_port):
        """
        注册活跃设备
        """
        # with self.device_id_lock:
        #     device_id = str(self.device_id_counter)
        device_id = str(uuid.uuid4().int)[:32]
        self.device_id_counter += 1
        self.active_devices[device_id] = {
            "name": device_name,
            "location": device_location,
            "ipv4": device_ipv4,
            "port": device_port
        }
        print(f"注册活跃设备: {device_id}, {device_name}, {device_location}, {device_ipv4}, {device_port}")
        print(f'当前活跃设备数量： {self.device_id_counter}' )
        return device_id
