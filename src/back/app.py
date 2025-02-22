# 导入必要的Flask组件和系统模块
from flask import Flask, jsonify, request  # Flask核心组件，用于JSON处理和请求处理
from flask_cors import CORS  # 处理跨域资源共享(CORS)
import sys
import os
sys.path.append(os.getcwd())  # 添加当前工作目录到系统路径，确保可以导入本地模块

# 导入自定义系统管理模块
# import control_src.put_realData as put_realData  # 实时数据处理模块（当前未使用）
import system_src.system_manger as system_manger  # 系统管理器模块

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许跨域请求

# 创建系统管理器实例，用于处理设备管理相关操作
system_manger_instance = system_manger.SystemManager()

# API路由：注册活跃设备
@app.route('/updateData/RegisterActiveDevice', methods=["PUT"])
def register_active_device():
    """
    处理设备注册请求
    接收参数:
    - type: 设备类型
    - device_name: 设备名称
    - device_location: 设备位置
    - device_ipv4: 设备IP地址
    - device_port: 设备端口
    返回:
    - 成功: {"status": "success", "device_id": 设备ID}
    - 失败: {"status": "error", "message": 错误信息}
    """
    try:    
        data = request.get_json()  # 获取JSON格式的请求数据
        print("data:", data)  # 调试输出
        device_id = system_manger_instance.register_active_device(
            data["type"], 
            data["device_name"], 
            data["device_location"], 
            data["device_ipv4"], 
            data["device_port"]
        )
        return jsonify({"status": "success", "device_id": device_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
# API路由：处理设备心跳数据
@app.route('/updateData/HeartbeatData', methods=["PUT"])
def heartbeat_data():
    """
    处理设备心跳请求，用于监控设备在线状态
    接收参数:
    - JSON格式的心跳数据（具体格式需参考system_manger模块定义）
    返回:
    - 成功: {"status": "success", "message": "心跳数据处理成功"}
    - 失败: {"status": "error", "message": 错误信息}
    """
    try:
        data = request.get_json()
        if system_manger_instance.input_device_heartbeat(data):
            return jsonify({"status": "success", "message": "心跳数据处理成功"})
        else:
            return jsonify({"status": "error", "message": "心跳数据处理失败"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 默认路由（当前已注释）
# @app.route('/', methods=["GET"])
# def index():
#     return "Welcome to API v1, try /hello."

# 实时数据更新路由（当前已注释）
# api.add_resource(put_realData.PutRealData, '/updateData/RealData')

# 应用程序入口点
if __name__ == "__main__":
    # app.run(host='127.0.0.1', debug=True, port=8010)  # 本地测试配置
    app.run(host='0.0.0.0', debug=True, port=8010)  # 生产环境配置，允许外部访问

