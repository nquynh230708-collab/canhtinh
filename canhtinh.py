import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Cấu hình trang - BẮT BUỘC ĐỂ DÒNG ĐẦU TIÊN
st.set_page_config(page_title="Cảnh tỉnh Lô Đề", layout="wide")

# 2. Tiêu đề ứng dụng (Sử dụng hàm mặc định để không bị lỗi CSS)
st.title("🚨 BẪY XÁC SUẤT: LÔ ĐỀ VS ĐẦU TƯ")
st.subheader("Dành cho học sinh lớp 9 - Bài học về tư duy tài chính")

# 3. Sidebar điều khiển bên trái
with st.sidebar:
    st.header("⚙️ Cài đặt mô phỏng")
    days = st.slider("Số ngày trải nghiệm", 365, 3650, 1095)
    reward_rate = st.slider("Mức thưởng (1 ăn bao nhiêu?)", 70, 99, 80)
    interest_rate = st.slider("Lãi suất đầu tư/năm (%)", 5, 15, 10)
    initial_balance = 100000000  # 100 triệu
    bet_amount = 10000           # 10k mỗi ngày

# 4. Thuật toán xử lý dữ liệu
def run_logic():
    g_bal = initial_balance
    i_bal = initial_balance
    g_hist = [g_bal]
    i_hist = [i_bal]
    
    # Tính lãi suất ngày từ lãi suất năm
    daily_int = (1 + interest_rate/100)**(1/365) - 1
    
    for _ in range(days):
        # Mô phỏng Lô đề (Xác suất trúng 1%)
        g_bal -= bet_amount
        if np.random.rand() < 0.01:
            g_bal += bet_amount * reward_rate
        g_hist.append(g_bal)
        
        # Mô phỏng Đầu tư (Lãi kép + tích lũy 10k mỗi ngày)
        i_bal = i_bal * (1 + daily_int) + bet_amount
        i_hist.append(i_bal)
        
    return g_hist, i_hist

# Chạy mô phỏng
g_data, i_data = run_logic()

# 5. Hiển thị Biểu đồ tương tác
fig = go.Figure()
fig.add_trace(go.Scatter(y=g_data, name="ĐƯỜNG LÔ ĐỀ (Rủi ro)", line=dict(color='red', width=3)))
fig.add_trace(go.Scatter(y=i_data, name="ĐƯỜNG ĐẦU TƯ (Lãi kép)", line=dict(color='green', width=3)))

fig.update_layout(
    xaxis_title="Số ngày trôi qua",
    yaxis_title="Số dư tài khoản (VNĐ)",
    template="plotly_dark",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# 6. Bảng thống kê kết quả
col1, col2 = st.columns(2)
with col1:
    final_g = g_data[-1]
    st.metric("Vốn Lô đề còn lại", f"{final_g:,.0f} VNĐ", delta=f"{final_g - initial_balance:,.0f}")
with col2:
    final_i = i_data[-1]
    st.metric("Vốn Đầu tư tích lũy", f"{final_i:,.0f} VNĐ", delta=f"{final_i - initial_balance:,.0f}")

# 7. Thông điệp đanh thép
st.divider()
st.error("⚠️ THÔNG ĐIỆP: Toán học chứng minh rằng cờ bạc không phải là may mắn, nó là một cuộc chơi chống lại quy luật xác suất mà bạn chắc chắn sẽ thất bại.")
