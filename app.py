import streamlit as st
import gcoord

# 页面配置
st.set_page_config(page_title="无人机航线规划系统", layout="wide")

# 全局状态初始化
if "drone_data" not in st.session_state:
    st.session_state.drone_data = {
        "point_a": {"lat": 0, "lng": 0, "set": False},
        "point_b": {"lat": 0, "lng": 0, "set": False},
        "height": 50,
        "heartbeat": []
    }

# 页面切换
page = st.sidebar.radio("功能页面", ["航线规划", "飞行监控"])

if page == "航线规划":
    st.title("🗺️ 航线规划")
    # 坐标系选择
    coord_system = st.radio("输入坐标系", ["GCJ-02(高德/百度)", "WGS-84"])
    # A/B点设置
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("起点A")
        a_lat = st.number_input("纬度", value=32.2322, format="%.6f")
        a_lng = st.number_input("经度", value=118.749, format="%.6f")
        if st.button("设置A点"):
            if coord_system == "WGS-84":
                a_lng, a_lat = gcoord.transform([a_lng, a_lat], gcoord.WGS84, gcoord.GCJ02)
            st.session_state.drone_data["point_a"] = {"lat": a_lat, "lng": a_lng, "set": True}
            st.success("A点设置成功！")
    with col2:
        st.subheader("终点B")
        b_lat = st.number_input("纬度", value=32.2343, format="%.6f")
        b_lng = st.number_input("经度", value=118.749, format="%.6f")
        if st.button("设置B点"):
            if coord_system == "WGS-84":
                b_lng, b_lat = gcoord.transform([b_lng, b_lat], gcoord.WGS84, gcoord.GCJ02)
            st.session_state.drone_data["point_b"] = {"lat": b_lat, "lng": b_lng, "set": True}
            st.success("B点设置成功！")
    # 飞行高度设置
    height = st.slider("设定飞行高度(m)", min_value=10, max_value=200, value=50)
    st.session_state.drone_data["height"] = height
    # 系统状态
    st.subheader("系统状态")
    st.write(f"A点已设：{'✅' if st.session_state.drone_data['point_a']['set'] else '❌'}")
    st.write(f"B点已设：{'✅' if st.session_state.drone_data['point_b']['set'] else '❌'}")

if page == "飞行监控":
    st.title("✈️ 飞行监控（心跳包）")
    # 模拟心跳包上传
    if st.button("上传测试心跳包"):
        test_data = {"lat": 32.233, "lng": 118.749, "height": 50, "time": st.datetime.now()}
        st.session_state.drone_data["heartbeat"].append(test_data)
        if len(st.session_state.drone_data["heartbeat"]) > 100:
            st.session_state.drone_data["heartbeat"] = st.session_state.drone_data["heartbeat"][-100:]
    # 显示心跳包数据
    st.subheader("心跳包历史")
    st.dataframe(st.session_state.drone_data["heartbeat"])
    app.run(host='0.0.0.0', port=52722, debug=True)
