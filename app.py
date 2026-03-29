from flask import Flask, render_template, request, jsonify
import gcoord  # 坐标转换

app = Flask(__name__)

# 全局存储无人机数据（实际项目用数据库）
drone_data = {
    "point_a": {"lat": 0, "lng": 0, "set": False},
    "point_b": {"lat": 0, "lng": 0, "set": False},
    "height": 50,
    "heartbeat": []
}

# ------------------- 页面路由 -------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route-plan')
def route_plan():
    return render_template('route_plan.html')

@app.route('/flight-monitor')
def flight_monitor():
    return render_template('flight_monitor.html')

# ------------------- 航线规划接口 -------------------
@app.route('/api/set-point', methods=['POST'])
def set_point():
    data = request.json
    point_type = data.get('type')  # 'A' 或 'B'
    lat = float(data.get('lat'))
    lng = float(data.get('lng'))
    coord_from = data.get('coordSystem', 'GCJ02')

    # 坐标转换：统一转成 GCJ02（国内地图标准）
    if coord_from == "WGS84":
        lng, lat = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)

    if point_type == "A":
        drone_data["point_a"] = {"lat": lat, "lng": lng, "set": True}
    elif point_type == "B":
        drone_data["point_b"] = {"lat": lat, "lng": lng, "set": True}

    return jsonify({"code": 200, "msg": "设置成功"})

@app.route('/api/set-height', methods=['POST'])
def set_height():
    height = request.json.get('height', 50)
    drone_data["height"] = height
    return jsonify({"code": 200, "msg": "高度设置成功"})

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
    data = request.json
    drone_data["heartbeat"].append(data)
    # 最多存100条
    if len(drone_data["heartbeat"]) > 100:
        drone_data["heartbeat"] = drone_data["heartbeat"][-100:]
    return jsonify({"code": 200, "msg": "上传成功"})

@app.route('/api/get-heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify(drone_data["heartbeat"])

# ------------------- 启动 -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
