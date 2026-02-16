import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 1. Cấu hình trang (Phải đặt đầu tiên)
st.set_page_config(
    page_title="Hộp Thời Gian Tết 2026",
    page_icon="🧧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS tùy chỉnh để đẹp trên Mobile
st.markdown("""
    <style>
    /* Nền đỏ đậm sang trọng */
    .stApp {
        background-color: #8B0000;
        color: #FFD700;
    }
    /* Chỉnh màu chữ Input thành đen cho dễ đọc */
    .stTextInput > div > div > input {
        color: #000000;
        background-color: #FFFDD0;
    }
    .stTextArea > div > div > textarea {
        color: #000000;
        background-color: #FFFDD0;
    }
    /* Nút bấm vàng rực rỡ */
    .stButton>button {
        background-color: #FFD700;
        color: #8B0000;
        border-radius: 20px;
        font-weight: bold;
        border: 2px solid #FFFFFF;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    /* Tiêu đề */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Giao diện chính
def main():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzJjMzQ1NjY3ODkwMTIza2xmZHNramZkc2tsamZkc2w&rid=giphy.gif", use_column_width=True) # Ảnh pháo hoa minh họa (nếu link die thì nó ẩn)

    st.title("🧧 GỬI ƯỚC NGUYỆN 2026")
    st.write("✨ *Hãy viết điều ước và gửi vào vũ trụ. Link này có thể mở trên điện thoại!*")

    # Form nhập liệu
    with st.form("wish_form", clear_on_submit=True):
        name = st.text_input("Tên của bạn:", placeholder="Ví dụ: Bảo đẹp trai")
        content = st.text_area("Điều ước năm nay:", height=100, placeholder="Năm nay mình sẽ...")
        
        # Nút gửi
        submitted = st.form_submit_button("🚀 GỬI ĐIỀU ƯỚC")

        if submitted:
            if not name or not content:
                st.error("⚠️ Bạn quên nhập tên hoặc điều ước rồi!")
            else:
                # Giả lập loading
                with st.spinner('Đang gửi tín hiệu lên sao Hỏa...'):
                    time.sleep(1.5)
                
                st.balloons()
                st.success(f"Tuyệt vời, {name} ơi! Điều ước đã được ghi nhận.")
                
                # Hiển thị lại kết quả đẹp mắt để chụp màn hình
                st.markdown("---")
                st.markdown(f"### 💌 Xác nhận từ Vũ Trụ")
                st.info(f"**Người gửi:** {name}\n\n**Nội dung:** {content}\n\n**Thời gian:** {datetime.now().strftime('%H:%M - %d/%m/%Y')}")
                st.warning("📸 Mẹo: Hãy chụp màn hình lại tấm vé này để làm kỷ niệm nhé!")

    st.markdown("---")
    with st.expander("ℹ️ Về trang web này"):
        st.write("""
        Đây là Hộp thời gian phiên bản Online.
        Dữ liệu phiên bản này sẽ được làm mới mỗi khi server khởi động lại để bảo mật quyền riêng tư trên Cloud công cộng.
        """)

if __name__ == "__main__":
    main()
