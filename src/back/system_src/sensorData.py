from enum import Enum

class SensorDataType(Enum):
    '''
    定义传感器数据类型
    '''
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    LIGHT = "light"
