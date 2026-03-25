import numpy as np
import control as ct
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st

# --------------------------
# 配置中文字体显示
# --------------------------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# --------------------------
# 系统定义：质量-弹簧-阻尼系统
# --------------------------
# m*x'' + c*x' + k*x = u
m = 1.0   # 质量
c = 0.5   # 阻尼系数
k = 2.0   # 弹簧系数

# 状态空间表示：x = [位置, 速度]^T
A = np.array([[0, 1],
              [-k/m, -c/m]])
B = np.array([[0],
              [1/m]])
C = np.array([[1, 0]])  # 只输出位置
D = np.array([[0]])

# 创建系统
sys = ct.ss(A, B, C, D)

# --------------------------
# Streamlit 界面与可视化
# --------------------------
st.title("无人机新那条检测可视化")
st.subheader("质量-弹簧-阻尼系统响应")

# 生成阶跃响应
t = np.linspace(0, 10, 1000)
t_step, y_step = ct.step_response(sys, T=t)

# 绘图
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t_step, y_step, label='阶跃响应')
ax.set_xlabel('时间 (s)')
ax.set_ylabel('位置')
ax.set_title('系统阶跃响应曲线')
ax.grid(True)
ax.legend()

# 在 Streamlit 中显示
st.pyplot(fig)

# 显示系统矩阵
st.subheader("系统状态空间矩阵")
st.write("A 矩阵：")
st.write(A)
st.write("B 矩阵：")
st.write(B)
st.write("C 矩阵：")
st.write(C)
st.write("D 矩阵：")
st.write(D)
