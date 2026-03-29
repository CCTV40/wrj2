import streamlit as st
import gcoord
from datetime import datetime

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
page = st.sidebar.radio("功能页面", ["航线规划", "飞行监控"], key="page_radio")

if page == "航线规划":
    st.title("🗺️ 航线规划")
    coord_system = st.radio("输入坐标系", ["GCJ-02(高德/百度)", "WGS-84"], key="coord_system")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("起点A")
        a_lat = st.number_input("纬度", value=32.2322, format="%.6f", key="a_lat")
        a_lng = st.number_input("经度", value=118.7490, format="%.6f", key="a_lng")
        if st.button("设置A点", key="set_a"):
            try:
                if coord_system == "WGS-84":
                    a_lng, a_lat = gcoord.transform([a_lng, a_lat], gcoord.WGS84, gcoord.GCJ02)
                st.session_state.drone_data["point_a"] = {"lat": a_lat, "lng": a_lng, "set": True}
                st.success("A点设置成功！")
            except Exception as e:
                st.error(f"转换失败：{str(e)}")

    with col2:
        st.subheader("终点B")
        b_lat = st.number_input("纬度", value=32.2343, format="%.6f", key="b_lat")
        b_lng = st.number_input("经度", value=118.7490, format="%.6f", key="b_lng")
        if st.button("设置B点", key="set_b"):
            try:
                if coord_system == "WGS-84":
                    b_lng, b_lat = gcoord.transform([b_lng, b_lat], gcoord.WGS84, gcoord.GCJ02)
                st.session_state.drone_data["point_b"] = {"lat": b_lat, "lng": b_lng, "set": True}
                st.success("B点设置成功！")
            except Exception as e:
                st.error(f"转换失败：{str(e)}")

    height = st.slider("设定飞行高度(m)", 10, 200, 50, key="height")
    st.session_state.drone_data["height"] = height

    st.subheader("系统状态")
    st.write(f"A点：{'✅ 已设置' if st.session_state.drone_data['point_a']['set'] else '❌ 未设置'}")
    st.write(f"B点：{'✅ 已设置' if st.session_state.drone_data['point_b']['set'] else '❌ 未设置'}")

if page == "飞行监控":
    st.title("✈️ 飞行监控")
    if st.button("上传测试心跳包", key="send_heartbeat"):
        test_data = {
            "lat": 32.2330,
            "lng": 118.7490,
            "height": st.session_state.drone_data["height"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.drone_data["heartbeat"].append(test_data)
        if len(st.session_state.drone_data["heartbeat"]) > 100:
            st.session_state.drone_data["heartbeat"] = st.session_state.drone_data["heartbeat"][-100:]
    
    st.subheader("心跳包历史")
    st.dataframe(st.session_state.drone_data["heartbeat"], key="heartbeat_list")
