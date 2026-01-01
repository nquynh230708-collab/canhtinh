import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Thiết kế giao diện Dark Mode cảnh báo
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1c1f26; padding: 15px; border-radius: 10px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_content_html=True)

st.title("🚨 HỆ THỐNG MÔ PHỎNG TÀI CHÍNH: LÔ ĐỀ VS ĐẦU TƯ")
st.write("Dành cho Giáo dục Kỹ năng sống - Chuyên đề: Bản chất của xác suất")

# Sidebar
with st.sidebar:
    st.header("⚙️ Cài đặt kịch bản")
    days = st.slider("Thời gian mô phỏng (Ngày)", 365, 3650, 1095)
    reward_rate = st.slider("Tỷ lệ trả thưởng (1 ăn...)", 70, 99, 80)
    interest_rate = st.slider("Lãi suất đầu tư hàng năm (%)", 5, 15, 10)
    bet_amount = 10000 # 10k mỗi ngày
    initial_balance = 100_000_000

# Xử lý Logic
def run_sim():
    g_bal = initial_balance
    i_bal = initial_balance
    g_history = [g_bal]
    i_history = [i_bal]
    daily_int = (1 + interest_rate/100)**(1/365) - 1
    
    for _ in range(days):
        # Lô đề
        g_bal -= bet_amount
        if np.random.rand() < 0.01:
            g_bal += bet_amount * reward_rate
        g_history.append(g_bal)
        
        # Đầu tư (Lãi kép + tích lũy 10k mỗi ngày thay vì đánh đề)
        i_bal = i_bal * (1 + daily_int) + bet_amount
        i_history.append(i_bal)
        
    return g_history, i_history

g_data, i_data = run_sim()

# Vẽ biểu đồ tương tác bằng Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(y=g_data, name="ĐÁNH LÔ ĐỀ (Rủi ro)", line=dict(color='#ff4b4b', width=3)))
fig.add_trace(go.Scatter(y=i_data, name="GỬI TIẾT KIỆM (Lãi kép)", line=dict(color='#00cc96', width=3)))

fig.update_layout(
    title="So sánh Biến động Tài sản",
    xaxis_title="Ngày",
    yaxis_title="Số dư (VNĐ)",
    template="plotly_dark",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# Thống kê cuối cùng
col1, col2 = st.columns(2)
with col1:
    final_g = g_data[-1]
    loss = initial_balance - final_g
    st.metric("Tài sản Lô đề", f"{final_g:,.0f} VNĐ", delta=f"-{loss:,.0f}")
    if final_g < initial_balance:
        st.error(f"Bạn đã mất {(loss/initial_balance)*100:.1f}% tài sản vào tay nhà cái.")

with col2:
    final_i = i_data[-1]
    profit = final_i - initial_balance
    st.metric("Tài sản Đầu tư", f"{final_i:,.0f} VNĐ", delta=f"+{profit:,.0f}")
    st.success(f"Bạn đã tăng trưởng {(profit/initial_balance)*100:.1f}% nhờ kỷ luật.")

st.divider()
st.subheader("💡 Bài học rút ra:")
st.warning("**Toán học chứng minh rằng cờ bạc không phải là may mắn, nó là một cuộc chơi chống lại quy luật xác suất mà bạn chắc chắn sẽ thất bại.**")