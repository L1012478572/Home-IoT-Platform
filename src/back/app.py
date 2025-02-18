from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
sys.path.append(os.getcwd())

# import control_src.put_realData as put_realData
import system_src.system_manger as system_manger

app = Flask(__name__)
CORS(app)

# 系统管理器实例
system_manger_instance = system_manger.SystemManager()

# 注册活跃设备
@app.route('/updateData/RegisterActiveDevice', methods=["PUT"])
def register_active_device():
    try:    
        data = request.get_json()
        print("data:", data)
        device_id = system_manger_instance.register_active_device(
            data["device_name"], 
            data["device_location"], 
            data["device_ipv4"], 
            data["device_port"]
        )
        return jsonify({"status": "success", "device_id": device_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# @app.route('/', methods=["GET"])
# def index():
#     return "Welcome to API v1, try /hello."

# api.add_resource(put_realData.PutRealData, '/updateData/RealData')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', debug=True, port=8010)
    app.run(host='0.0.0.0', debug=True, port=8010)

