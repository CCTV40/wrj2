import streamlit as st
import gcoord

# 页面配置
st.set_page_config(page_title="无人机航线规划系统", layout="wide")

# 全局状态初始化（Streamlit 用 session_state 存储数据）
if "drone_data" not in st.session_state:
    st.session_state.drone_data = {
        "point_a": {"lat": 0.0, "lng": 0.0, "set": False},
        "point_b": {"lat": 0.0, "lng": 0.0, "set": False},
        "height": 50,
        "heartbeat": []
    }

# 侧边栏导航
with st.sidebar:
    st.title("导航")
    page = st.radio("功能页面", ["航线规划", "飞行监控"])
    st.divider()
    # 坐标系设置
    st.subheader("坐标系设置")
    coord_system = st.radio("输入坐标系", ["GCJ-02(高德/百度)", "WGS-84"], index=0)
    st.divider()
    # 系统状态
    st.subheader("系统状态")
    st.write(f"A点已设：{'✅' if st.session_state.drone_data['point_a']['set'] else '❌'}")
    st.write(f"B点已设：{'✅' if st.session_state.drone_data['point_b']['set'] else '❌'}")

# ------------------- 航线规划页面 -------------------
if page == "航线规划":
    st.title("🗺️ 航线规划")
    st.divider()

    # A/B 点设置
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("起点A")
        a_lat = st.number_input("纬度", value=32.2322, format="%.6f", key="a_lat")
        a_lng = st.number_input("经度", value=118.749, format="%.6f", key="a_lng")
        if st.button("设置A点", type="primary"):
            # 坐标转换
            lat, lng = a_lat, a_lng
            if coord_system == "WGS-84":
                lng, lat = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)
            st.session_state.drone_data["point_a"] = {"lat": lat, "lng": lng, "set": True}
            st.success("✅ A点设置成功！")

    with col2:
        st.subheader("终点B")
        b_lat = st.number_input("纬度", value=32.2343, format="%.6f", key="b_lat")
        b_lng = st.number_input("经度", value=118.749, format="%.6f", key="b_lng")
        if st.button("设置B点", type="primary"):
            # 坐标转换
            lat, lng = b_lat, b_lng
            if coord_system == "WGS-84":
                lng, lat = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)
            st.session_state.drone_data["point_b"] = {"lat": lat, "lng": lng, "set": True}
            st.success("✅ B点设置成功！")

    st.divider()
    # 飞行高度设置
    st.subheader("飞行参数")
    height = st.slider("设定飞行高度(m)", min_value=10, max_value=200, value=50, key="height")
    st.session_state.drone_data["height"] = height
    st.info(f"当前设定高度：{height}m")

# ------------------- 飞行监控页面 -------------------
if page == "飞行监控":
    st.title("✈️ 飞行监控（心跳包）")
    st.divider()

    # 模拟心跳包上传（实际项目对接无人机硬件）
    if st.button("上传测试心跳包", type="primary"):
        import time
        test_data = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "lat": st.session_state.drone_data["point_a"]["lat"] + 0.0001,
            "lng": st.session_state.drone_data["point_a"]["lng"] + 0.0001,
            "height": st.session_state.drone_data["height"],
            "status": "正常"
        }
        st.session_state.drone_data["heartbeat"].append(test_data)
        # 最多保留100条
        if len(st.session_state.drone_data["heartbeat"]) > 100:
            st.session_state.drone_data["heartbeat"] = st.session_state.drone_data["heartbeat"][-100:]
        st.success("✅ 测试心跳包上传成功！")

    st.divider()
    # 显示心跳包历史
    st.subheader("心跳包历史数据")
    if st.session_state.drone_data["heartbeat"]:
        st.dataframe(st.session_state.drone_data["heartbeat"], use_container_width=True)
    else:
        st.info("暂无心跳包数据")

    # 清空数据按钮
    if st.button("清空历史数据", type="secondary"):
        st.session_state.drone_data["heartbeat"] = []
        st.experimental_rerun()
