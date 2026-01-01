import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Cấu hình trang (Phải đặt ở dòng đầu tiên của code)
st.set_page_config(page_title="Cảnh tỉnh Lô Đề", layout="wide")

# 2. Định nghĩa giao diện bằng CSS (Tách riêng để tránh lỗi cú pháp)
css = """
<style>
    .main { background-color: #0e1117; color: white; }
    h1 { color: #ff4b4b; text-align: center; font-family: sans-serif; }
    .stMetric { border: 1px solid #ff4b4b; padding: 10px; border-radius: 5px; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.markdown("<h1>🚨 BẪY XÁC SUẤT: LÔ ĐỀ VS ĐẦU TƯ</h1>", unsafe_allow_html=True)
st.write("Dành cho học sinh lớp 9 - Bài học về tư duy tài chính và xác suất.")

# 3. Sidebar điều khiển
with st.sidebar:
    st.header("⚙️ Cấu hình")
    days = st.slider("Số ngày mô phỏng", 365, 3650, 1095)
    reward_rate = st.slider("Mức thưởng (1 ăn...)", 70, 99, 80)
    interest_rate = st.sidebar.slider("Lãi suất năm (%)", 5, 15, 10)
    initial_bal = 100_000_000
    bet_per_day = 10000

# 4. Logic mô phỏng
def run_simulation():
    g_bal = initial_bal
    i_bal = initial_bal
    g_hist = [g_bal]
    i_hist = [i_bal]
    
    daily_int = (1 + interest_rate/100)**(1/365) - 1
    
    for _ in range(days):
        # Mô phỏng Lô đề
        g_bal -= bet_per_day
        if np.random.rand() < 0.01:
            g_bal += bet_per_day * reward_rate
        g_hist.append(g_bal)
        
        # Mô phỏng Đầu tư
        i_bal = i_bal * (1 + daily_int) + bet_per_day
        i_hist.append(i_bal)
        
    return g_hist, i_hist

g_data, i_data = run_simulation()

# 5. Hiển thị Biểu đồ
fig = go.Figure()
fig.add_trace(go.Scatter(y=g_data, name="LÔ ĐỀ (Rủi ro)", line=dict(color='red', width=2)))
fig.add_trace(go.Scatter(y=i_data, name="ĐẦU TƯ (Lãi kép)", line=dict(color='green', width=2)))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Ngày",
    yaxis_title="Số dư (VNĐ)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# 6. Báo cáo thống kê
c1, c2 = st.columns(2)
with c1:
    st.metric("Tài sản Lô đề", f"{g_data[-1]:,.0f} VNĐ", delta=f"{g_data[-1]-initial_bal:,.0f}")
with c2:
    st.metric("Tài sản Đầu tư", f"{i_data[-1]:,.0f} VNĐ", delta=f"{i_data[-1]-initial_bal:,.0f}")

st.divider()
st.error("THÔNG ĐIỆP KẾT LUẬN: Toán học chứng minh rằng cờ bạc không phải là may mắn, nó là một cuộc chơi chống lại quy luật xác suất mà bạn chắc chắn sẽ thất bại.")
