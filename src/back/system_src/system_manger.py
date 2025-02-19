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
import system_src.mysql_src.mysql_humidifier_v2 as mysql_humidifier_v2


mysql_host = "127.0.0.1"
mysql_port = 3306
mysql_user = "root"
mysql_password = "123456"


class SystemManager:
    def __init__(self):
        self.active_devices = list[device.Device]()     # 活跃设备列表  
        self.device_id_counter = 0   # 设备id计数器
        self.device_id_lock = threading.Lock()  # 设备id锁

        # 创建活跃设备检索线程
        self.active_device_thread = device.DeviceActiveManager(self.active_devices, self.device_id_lock)
        self.active_device_thread.start()

        # 创建humidifier_v2设备数据管理对象
        self.mysql_humidifier_v2 = mysql_humidifier_v2.MySql_HumidifierV2(mysql_host, mysql_port, mysql_user, mysql_password)

    def register_active_device(self, type: str, device_name: str, device_location: str, device_ipv4: str, device_port: int) -> str:
        """
        注册活跃设备
        1- 检查device_ipv4是否已存在
        2- 如果存在, 则返回对应的设备id号
        3- 如果不存在, 则生成一个设备id号, 并返回
        4- 将设备信息存储到active_devices字典中
        """
        # 检查设备是否已添加到数据库 并得到device_id
        device_id = self._check_and_get_device_id(type, device_name, device_location, device_ipv4, device_port)

        # 检查device_ipv4是否已存在活跃设备列表中 
        # 如果存在, 则返回对应的设备id号
        for active_device in self.active_devices:
            if active_device.ipv4 == device_ipv4:
                print(f"设备{device_ipv4}已存在")
                return active_device.device_id
        # 如果不存在, 则创建一个活跃设备
        new_active_device = device.Device(device_id, type, device_name, device_location, device_ipv4, device_port)
        # 添加到活跃设备列表
        self.device_id_lock.acquire()   
        self.active_devices.append(new_active_device)
        self.device_id_lock.release()
        # 返回设备id号
        return device_id

    def input_device_heartbeat(self, putData: str):
        """
        输入设备心跳数据
        1- 检查设备是否存在
        2- 如果存在, 更新设备的心跳数据
        3- 如果不存在, 返回错误信息
        """
        # 解析json数据
        data_parse = json.loads(putData)
        device_id = data_parse["device_id"]
        device_type = data_parse["device_type"]
        # sensor_data数据结构：
        # sensor_data = [
        #     {
        #         "type": "temperature",
        #         "value": 23.5
        #     },
        #     {
        #         "type": "humidity",
        #         "value": 68
        #     },
        # ]
        sensor_data = data_parse["sensor_data"]
        # device_data数据结构：
        # device_data = {
        #     "humidity": 60,
        #     "remaining_battery": 80
        # }
        device_data = data_parse["device_data"]

        # 检查设备是否存在
        for active_device in self.active_devices:
            if active_device.device_id == device_id:
                # 更新设备的心跳数据
                active_device.update_heartbeat_timestamp()
                print(f"设备{device_id}的心跳数据已更新")
                return True
        # 如果不存在, 返回错误信息
        print(f"设备{device_id}不存在")
        return False
    
    def _check_and_get_device_id(self, type: str, device_name: str, device_location: str, device_ipv4: str, device_port: int) -> str:
        '''
        检查设备是否已添加到数据库 并得到device_id
        '''
        if type == "humidifier_v2":
            device_saveInfo_dict = self.mysql_humidifier_v2.get_humidifier_v2_data_by_device_name_and_location(device_name, device_location)
            if device_saveInfo_dict is not None:
                print(f"设备{device_name}已存在")
                device_id = device_saveInfo_dict["device_id"]
                # 若其ip和端口号已修改 则更新数据库
                if device_saveInfo_dict["device_ipv4"] != device_ipv4 or device_saveInfo_dict["device_port"] != device_port:
                    self.mysql_humidifier_v2.update_humidifier_v2_data_by_device_id(device_id, device_name, device_location, device_ipv4, device_port)
            else:
                print(f"设备{device_name}不存在")
                device_id = str(uuid.uuid4().int)[:32]
                # 添加到数据库
                self.mysql_humidifier_v2.add_humidifier_v2_data(device_id, device_name, device_location, device_ipv4, device_port)
            return device_id
        else:
            device_id = str(uuid.uuid4().int)[:32]
            print(f"设备类型{type}不存在")
            return device_id
