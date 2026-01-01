import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Thiết kế giao diện Dark Mode (Đã sửa lỗi unsafe_allow_html)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { 
        background-color: #1c1f26; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #ff4b4b; 
    }
    h1 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 BẪY XÁC SUẤT: LÔ ĐỀ VS ĐẦU TƯ")
st.write("Dành cho học sinh lớp 9 - Bài học về Kỳ vọng âm và Lãi suất kép")

# Sidebar cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình mô phỏng")
    days = st.slider("Số ngày trải nghiệm", 365, 3650, 1095)
    reward_rate = st.slider("Mức thưởng (1 ăn bao nhiêu?)", 70, 99, 80)
    interest_rate = st.slider("Lãi suất đầu tư hàng năm (%)", 5, 15, 10)
    initial_balance = 100_000_000
    bet_per_day = 10000

# Hàm tính toán mô phỏng
def run_simulation():
    g_balance = initial_balance
    i_balance = initial_balance
    g_history = [initial_balance]
    i_history = [initial_balance]
    
    # Tính lãi suất ngày từ lãi suất năm
    daily_interest = (1 + interest_rate/100)**(1/365) - 1
    
    for _ in range(days):
        # 1. Logic Lô đề
        g_balance -= bet_per_day
        if np.random.rand() < 0.01: # Xác suất trúng 1/100
            g_balance += bet_per_day * reward_rate
        g_history.append(g_balance)
        
        # 2. Logic Đầu tư
        i_balance = i_balance * (1 + daily_interest) + bet_per_day
        i_history.append(i_balance)
        
    return g_history, i_history

# Chạy và hiển thị
g_data, i_data = run_simulation()

# Vẽ biểu đồ Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(y=g_data, name="ĐÁNH LÔ ĐỀ", line=dict(color='#ff4b4b', width=3)))
fig.add_trace(go.Scatter(y=i_data, name="GỬI TIẾT KIỆM", line=dict(color='#00cc96', width=3)))

fig.update_layout(
    xaxis_title="Ngày trôi qua",
    yaxis_title="Số tiền (VNĐ)",
    template="plotly_dark",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)
st.plotly_chart(fig, use_container_width=True)

# Báo cáo thống kê
col1, col2 = st.columns(2)
with col1:
    final_g = g_data[-1]
    st.metric("Vốn Lô đề còn lại", f"{final_g:,.0f} VNĐ", delta=f"{final_g - initial_balance:,.0f}")
    
with col2:
    final_i = i_data[-1]
    st.metric("Vốn Đầu tư có được", f"{final_i:,.0f} VNĐ", delta=f"{final_i - initial_balance:,.0f}")

st.divider()
st.error("THÔNG ĐIỆP KẾT LUẬN: Toán học chứng minh rằng cờ bạc không phải là may mắn, nó là một cuộc chơi chống lại quy luật xác suất mà bạn chắc chắn sẽ thất bại.")
