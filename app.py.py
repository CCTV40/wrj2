import numpy as np
import control as ct
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 或者指定具体的中文字体（如果安装了）
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
# plt.rcParams['font.sans-serif'] = ['KaiTi']  # 楷体
# plt.rcParams['font.sans-serif'] = ['FangSong']  # 仿宋

# 系统定义：质量-弹簧-阻尼系统
# m*x'' + c*x' + k*x = u
m = 1.0    # 质量
c = 0.5    # 阻尼系数
k = 2.0    # 弹簧系数

# 状态空间表示：x = [位置, 速度]^T
A = np.array([[0, 1],
              [-k/m, -c/m]])
B = np.array([[0],
              [1/m]])
C = np.array([[1, 0]])  # 只输出位置
D = np.array([[0]])

# 创建系统
sys = ct.ss(A, B, C, D)
print("系统矩阵:")
print("A =", A)
print("B =", B)
print("C =", C)

# LQR权重矩阵
Q = np.array([[100, 0],   # 位置误差权重较大
              [0, 1]])    # 速度误差权重
R = np.array([[0.1]])     # 控制输入权重

# 计算LQR增益
K, S, E = ct.lqr(A, B, Q, R)
print("\nLQR增益矩阵 K =", K.flatten())

# 参考信号（设定点）
r = 2.0  # 目标位置

# 闭环系统
A_cl = A - B @ K
sys_cl = ct.ss(A_cl, B, C, D)

# 仿真时间
t = np.linspace(0, 10, 1000)

# 初始条件
x0 = np.array([[0], [0]])  # 初始位置和速度都为0

# 计算稳态控制输入
# 对于恒定参考信号，需要计算前馈增益
K_r = 1 / (C @ np.linalg.inv(-A_cl) @ B)
u_ss = K_r * r

# 闭环响应
t, y = ct.initial_response(sys_cl, t, x0)
# 添加稳态偏移
y = y + r * (1 - np.exp(-0.5*t))  # 近似跟踪效果

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, y, 'b-', linewidth=2, label='系统响应')
plt.axhline(y=r, color='r', linestyle='--', label='参考信号')
plt.xlabel('时间 (s)')
plt.ylabel('位置')
plt.title('LQR跟踪控制 - 位置响应')
plt.legend()
plt.grid(True)

# 控制输入
u = -K @ np.column_stack([y - r, np.gradient(y, t[1]-t[0])]).T
plt.subplot(2, 1, 2)
plt.plot(t, u.flatten(), 'g-', linewidth=2)
plt.xlabel('时间 (s)')
plt.ylabel('控制输入 u')
plt.title('控制输入信号')
plt.grid(True)

plt.tight_layout()
plt.show()
