import time
import threading
import logging
import queue

from enum import Enum

class DeviceType(Enum):
    '''
    设备类型
    包括：
    空气加湿器
    排风扇
    '''
    HUMIDIFIER_V2 = "humidifier_v2"   # 空气加湿器
    FAN_V2 = "fan_v2"                 # 排风扇

class Device:
    '''
    设备类
    定义设备类型数据
    包括设备id, 名称, 位置, ip, 端口
    新建设备时，会记录设备创建时间
    '''
    def __init__(self, device_id, device_type, name, location, ipv4, port):
        self.device_id = device_id              # 设备id    
        self.device_type = device_type          # 设备类型
        self.name = name                        # 设备名称
        self.location = location                # 设备位置
        self.ipv4 = ipv4                        # 设备ip
        self.port = port                        # 设备端口
        self.creation_timestamp = time.time()   # 设备创建时间
        self.heartbeat_timestamp = self.creation_timestamp  # 设备心跳时间

    def to_dict(self):
        '''
        将设备数据转换为字典
        '''
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "name": self.name,
            "location": self.location,
            "ipv4": self.ipv4,
            "port": self.port
        }
    
    def update_heartbeat_timestamp(self):
        '''
        更新设备心跳时间
        '''
        self.heartbeat_timestamp = time.time()

class DeviceActiveManager(threading.Thread):
    '''
    设备活跃管理类
    是一个线程，每分钟检查一次设备活跃状态
    如果设备心跳时间与当前时间差大于2分钟，则认为设备不活跃
    将不活跃的设备从活跃设备列表中移除
    '''
    def __init__(self, active_devices: list[Device], device_lock: threading.Lock):
        super().__init__()
        self.active_devices = active_devices
        self.device_lock = device_lock

    def run(self):
        '''
        每分钟检查一次设备活跃状态
        '''
        while True:
            # 获取当前时间  
            current_time = time.time()
            # 遍历活跃设备列表
            for device in self.active_devices:
                # 判断device的类型
                if not isinstance(device, Device):
                    self.device_lock.acquire()
                    self.active_devices.remove(device)
                    self.device_lock.release()
                # 检查设备心跳时间与当前时间差
                if current_time - device.heartbeat_timestamp > 120:
                    # 如果设备心跳时间与当前时间差大于2分钟，则认为设备不活跃
                    self.device_lock.acquire()
                    self.active_devices.remove(device)
                    self.device_lock.release()
            # 等待1分钟
            time.sleep(60)
