import streamlit as st

st.set_page_config(page_title="测试页", layout="wide")
st.title("Streamlit 环境测试页 ✅")

st.write("如果能看到这个页面，说明 Streamlit 环境正常，报错来自你的业务代码")

# 测试基础组件
st.subheader("基础组件测试")
st.button("点击我")
st.slider("滑动条", 0, 100, 50)
st.text_input("输入框")

# 测试动态组件
st.subheader("动态组件测试")
if st.button("切换显示"):
    if "show" not in st.session_state:
        st.session_state.show = True
    st.session_state.show = not st.session_state.show

if st.session_state.get("show", True):
    st.write("显示内容")
else:
    st.write("隐藏内容")
    # 清空数据（原生按钮，无 JS）
    if st.button("清空历史数据", type="secondary", key="clear"):
        st.session_state.drone_data["heartbeat"] = []
        st.rerun()
