
from flask import Flask, request, jsonify
from flask_restful import Resource

class PutRealData(Resource):
    def put(self):
        if request.is_json:
            data = request.get_json()
            required_keys = ["type", "room_id", "timestamp", "data", "device"]
            if not all(key in data for key in required_keys):
                return {"message": "Missing required parameters"}, 400

            if data["type"] != "sensor_data":
                return {"message": "Invalid type"}, 400

            sensor_data = data["data"]
            device_info = data["device"]

            # 处理传感器数据和设备信息
            # 这里可以添加数据存储或处理逻辑

            return {"message": "Data updated successfully"}, 200
        else:
            return {"message": "Request must be JSON"}, 400