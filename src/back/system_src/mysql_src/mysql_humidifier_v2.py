'''
    空气加湿器v2版本

    1 设备信息库 DeviceInfo 
        1.1 humidifier_v2 表：
            id: key
            device_id: 设备id
            device_name: 设备名称
            device_location: 设备位置
            device_ipv4: 设备ip地址
            device_port: 设备端口
            register_time: 注册时间

    2 创建对应的设备数据库，并管理数据 数据库名根据humidifier_v2+device_id生成
        2.1 每月创建一个表 表名：humidifier_v2_YYYYMM
        2.2 表结构：
            id: key
            datetime: 数据时间
            temperature: 温度
            humidity: 湿度
            humidity_set: 湿度设置
            remaining_battery: 剩余电量
'''

import mysql.connector
import datetime

class MySql_HumidifierV2:
    def __init__(self, mysql_host: str, mysql_port: int, mysql_user: str, mysql_password: str):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_device_info = "DeviceInfo"

        # 连接到设备信息数据库
        self.mysql_deviceInfo_conn = mysql.connector.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_device_info
        )
        # 创建设备信息数据库游标
        self.mysql_deviceInfo_cursor = self.mysql_deviceInfo_conn.cursor()

        # 判断是否有humidifier_v2表
        self.mysql_deviceInfo_cursor.execute("SHOW TABLES LIKE 'humidifier_v2'")
        result = self.mysql_deviceInfo_cursor.fetchone()
        if result:
            print("humidifier_v2表存在")
        else:
            print("humidifier_v2表不存在")  
            # 创建humidifier_v2表
            self.create_humidifier_v2_table()
            
    
    def create_humidifier_v2_table(self):
        '''
        创建humidifier_v2表
        表结构：
            id: key
            device_id: 设备id
            device_name: 设备名称
            device_location: 设备位置
            device_ipv4: 设备ip地址
            device_port: 设备端口
            register_time: 注册时间
        '''
        try:
            self.mysql_deviceInfo_cursor.execute("CREATE TABLE humidifier_v2 (id INT AUTO_INCREMENT PRIMARY KEY, device_id VARCHAR(255), device_name VARCHAR(255), device_location VARCHAR(255), device_ipv4 VARCHAR(255), device_port INT, register_time DATETIME)")
            self.mysql_deviceInfo_conn.commit()
            print("humidifier_v2表创建成功")
        except mysql.connector.Error as err:
            print(f"创建humidifier_v2表失败: {err}")

    def add_humidifier_v2_data(self, device_id: str, device_name: str, device_location: str, device_ipv4: str, device_port: int):
        '''
        向humidifier_v2表中添加一条数据
        数据内容由入口参数获得
        '''
        try:
            register_time = datetime.datetime.now()
            sql = "INSERT INTO humidifier_v2 (device_id, device_name, device_location, device_ipv4, device_port, register_time) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (device_id, device_name, device_location, device_ipv4, device_port, register_time)
            self.mysql_deviceInfo_cursor.execute(sql, val)
            self.mysql_deviceInfo_conn.commit()
            print(f"设备{device_id}的数据已添加到humidifier_v2表中")
        except mysql.connector.Error as err:
            print(f"添加设备{device_id}的数据到humidifier_v2表失败: {err}")

    def get_humidifier_v2_data_by_device_name_and_location(self, device_name: str, device_location: str) -> dict:
        '''
        根据device_name和device_location查询表中是否有对应的数据
        若有则返回对应数据的字典
        '''
        try:
            sql = "SELECT * FROM humidifier_v2 WHERE device_name = %s AND device_location = %s"
            val = (device_name, device_location)
            self.mysql_deviceInfo_cursor.execute(sql, val)
            result = self.mysql_deviceInfo_cursor.fetchone()
            if result:
                data = {
                    "id": result[0],
                    "device_id": result[1],
                    "device_name": result[2],
                    "device_location": result[3],
                    "device_ipv4": result[4],
                    "device_port": result[5],
                    "register_time": result[6]
                }
                return data
            else:
                print(f"没有找到设备名称为{device_name}且设备位置为{device_location}的数据")
                return None
        except mysql.connector.Error as err:
            print(f"查询设备数据失败: {err}")
            return None
        
    def update_humidifier_v2_data_by_device_id(self, device_id: str, device_name: str, device_location: str, device_ipv4: str, device_port: int):
        '''
        根据device_id更新humidifier_v2表中的数据
        '''
        try:
            sql = "UPDATE humidifier_v2 SET device_name = %s, device_location = %s, device_ipv4 = %s, device_port = %s WHERE device_id = %s"
            val = (device_name, device_location, device_ipv4, device_port, device_id)
            self.mysql_deviceInfo_cursor.execute(sql, val)
            self.mysql_deviceInfo_conn.commit()
            print(f"设备{device_id}的数据已更新")
        except mysql.connector.Error as err:
            print(f"更新设备{device_id}的数据失败: {err}")
    
