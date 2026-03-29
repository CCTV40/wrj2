from flask import Flask, render_template, request, jsonify
import gcoord  # 坐标转换

app = Flask(__name__)
app.secret_key = "drone_project_2026"  # 加个密钥避免报错

# 全局存储无人机数据
drone_data = {
    "point_a": {"lat": 0, "lng": 0, "set": False},
    "point_b": {"lat": 0, "lng": 0, "set": False},
    "height": 50,
    "heartbeat": []
}

# ------------------- 页面路由 -------------------
@app.route('/')
def index():
    return "无人机航线规划系统 - 后端服务已启动"

@app.route('/api/info')
def info():
    return jsonify({"status": "running", "msg": "服务正常"})

# ------------------- 航线规划接口 -------------------
@app.route('/api/set-point', methods=['POST'])
def set_point():
    try:
        data = request.json
        point_type = data.get('type')
        lat = float(data.get('lat', 0))
        lng = float(data.get('lng', 0))
        coord_from = data.get('coordSystem', 'GCJ02')

        # 坐标转换
        if coord_from == "WGS84":
            lng, lat = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)

        if point_type == "A":
            drone_data["point_a"] = {"lat": lat, "lng": lng, "set": True}
        elif point_type == "B":
            drone_data["point_b"] = {"lat": lat, "lng": lng, "set": True}

        return jsonify({"code": 200, "msg": "设置成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"错误：{str(e)}"}), 500

@app.route('/api/set-height', methods=['POST'])
def set_height():
    try:
        height = int(request.json.get('height', 50))
        drone_data["height"] = height
        return jsonify({"code": 200, "msg": "高度设置成功"})
    except:
        return jsonify({"code": 500, "msg": "设置失败"}), 500

@app.route('/api/get-route-info', methods=['GET'])
def get_route_info():
    return jsonify({
        "pointA": drone_data["point_a"],
        "pointB": drone_data["point_b"],
        "height": drone_data["height"]
    })

# ------------------- 飞行监控（心跳包） -------------------
@app.route('/api/upload-heartbeat', methods=['POST'])
def upload_heartbeat():
    try:
        data = request.json
        drone_data["heartbeat"].append(data)
        if len(drone_data["heartbeat"]) > 100:
            drone_data["heartbeat"] = drone_data["heartbeat"][-100:]
        return jsonify({"code": 200, "msg": "上传成功"})
    except:
        return jsonify({"code": 500, "msg": "上传失败"}), 500

@app.route('/api/get-heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify(drone_data["heartbeat"])

# ------------------- 启动 -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52722, debug=True)
