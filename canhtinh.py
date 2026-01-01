import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Cấu hình tiêu đề trang
st.set_page_config(page_title="Cảnh tỉnh Lô Đề", layout="wide")

# 2. Sửa lỗi CSS và tham số (Đảm bảo viết sát lề trái)
st.markdown("### 🚨 BẪY XÁC SUẤT: LÔ ĐỀ VS ĐẦU TƯ", unsafe_allow_html=True)
st.write("Ứng dụng mô phỏng dành cho giáo dục kỹ năng sống.")

# 3. Sidebar điều khiển
with st.sidebar:
    st.header("⚙️ Cài đặt")
    days = st.slider("Số ngày mô phỏng", 365, 3650, 1095)
    reward_rate = st.slider("Mức thưởng (1 ăn...)", 70, 99, 80)
    interest_rate = st.slider("Lãi suất năm (%)", 5, 15, 10)
    initial_bal = 100_000_000
    bet = 10000

# 4. Thuật toán tính toán
def run_sim():
    g_bal, i_bal = initial_bal, initial_bal
    g_hist, i_hist = [initial_bal], [initial_bal]
    daily_int = (1 + interest_rate/100)**(1/365) - 1
    
    for _ in range(days):
        # Lô đề
        g_bal -= bet
        if np.random.rand() < 0.01:
            g_bal += bet * reward_rate
        g_hist.append(g_bal)
        # Đầu tư
        i_bal = i_bal * (1 + daily_int) + bet
        i_history_val = i_bal
        i_hist.append(i_history_val)
    return g_hist, i_hist

g_data, i_data = run_sim()

# 5. Hiển thị biểu đồ
fig = go.Figure()
fig.add_trace(go.Scatter(y=g_data, name="LÔ ĐỀ", line=dict(color='red')))
fig.add_trace(go.Scatter(y=i_data, name="ĐẦU TƯ", line=dict(color='green')))
fig.update_layout(template="plotly_dark", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# 6. Thống kê
c1, c2 = st.columns(2)
c1.metric("Vốn Lô đề", f"{g_data[-1]:,.0f} VNĐ")
c2.metric("Vốn Đầu tư", f"{i_data[-1]:,.0f} VNĐ")

st.error("KẾT LUẬN: Toán học chứng minh rằng cờ bạc không phải là may mắn, nó là một cuộc chơi chống lại quy luật xác suất mà bạn chắc chắn sẽ thất bại.")
