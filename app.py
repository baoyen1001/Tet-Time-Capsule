import streamlit as st
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# --- 1. CẤU HÌNH TRANG (PHẢI ĐỂ ĐẦU TIÊN) ---
st.set_page_config(
    page_title="Hộp Thời Gian Tết Bính Ngọ 2026",
    page_icon="🏮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. HÀM TẠO ẢNH THIỆP (TÍNH NĂNG PRO) ---
def create_wish_card(name, content):
    # Tạo nền đỏ
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#8B0000')
    d = ImageDraw.Draw(img)
    
    # Vẽ khung vàng
    d.rectangle([20, 20, width-20, height-20], outline="#FFD700", width=5)
    d.rectangle([30, 30, width-30, height-30], outline="#FFD700", width=2)
    
    # Do Streamlit Cloud không có sẵn font tiếng Việt đẹp, ta dùng font mặc định nhưng canh chỉnh khéo
    # Tiêu đề
    d.text((width/2, 100), "CHÚC MỪNG NĂM MỚI", fill="#FFD700", anchor="mm", font_size=60)
    d.text((width/2, 180), "2026", fill="#FFD700", anchor="mm", font_size=80)
    
    # Nội dung điều ước (Cắt dòng nếu quá dài)
    import textwrap
    lines = textwrap.wrap(content, width=40) # Tự xuống dòng
    y_text = 280
    for line in lines:
        d.text((width/2, y_text), line, fill="white", anchor="mm", font_size=40)
        y_text += 50
        
    # Tên người gửi
    d.text((width/2, height-100), f"Người gửi: {name}", fill="#FFD700", anchor="mm", font_size=30)
    
    # Chuyển ảnh thành bytes để hiển thị lên web
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# --- 3. CSS TÙY CHỈNH (GIAO DIỆN ĐẸP) ---
st.markdown("""
    <style>
    /* Import font Google */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@300;400&display=swap');

    /* Nền chung */
    .stApp {
        background-color: #5e0a0a; /* Đỏ rượu vang */
        background-image: radial-gradient(#7a0e0e 20%, transparent 20%),
        radial-gradient(#7a0e0e 20%, transparent 20%);
        background-size: 50px 50px;
        background-position: 0 0, 25px 25px;
    }

    /* Tiêu đề chính */
    h1 {
        font-family: 'Playfair Display', serif;
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
        font-size: 3rem !important;
        padding-bottom: 20px;
    }

    /* Card chứa form */
    .wish-card {
        background-color: rgba(255, 253, 208, 0.95); /* Màu kem */
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #FFD700;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    /* Chỉnh màu chữ trong card */
    .stMarkdown, .stText, label {
        color: #333333 !important;
        font-family: 'Roboto', sans-serif;
    }

    /* Input field */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #000;
        border: 1px solid #d1d1d1;
        border-radius: 8px;
    }

    /* Nút bấm vàng kim loại */
    .stButton > button {
        background: linear-gradient(to bottom, #FFD700 5%, #FFAA00 100%);
        background-color: #FFD700;
        border-radius: 28px;
        border: 1px solid #ffaa22;
        display: inline-block;
        cursor: pointer;
        color: #8B0000;
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        font-weight: bold;
        padding: 16px 31px;
        text-decoration: none;
        text-shadow: 0px 1px 0px #ffee66;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(to bottom, #FFAA00 5%, #FFD700 100%);
        transform: scale(1.02);
    }
    
    /* Ẩn footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. GIAO DIỆN CHÍNH ---
def main():
    # Header với hiệu ứng
    st.markdown("<h1>🏮 HỘP THỜI GIAN 2026 🏮</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ffcccb; font-style: italic; margin-bottom: 30px;'>Gửi một tín hiệu vào vũ trụ, gặt hái thành công vào cuối năm.</p>", unsafe_allow_html=True)

    # Container dạng Card
    with st.container():
        st.markdown('<div class="wish-card">', unsafe_allow_html=True)
        
        # Form nhập liệu
        col1, col2 = st.columns([1, 1])
        with col1:
            name = st.text_input("Họ và tên quý danh:", placeholder="Nhập tên của bạn...")
        with col2:
            feeling = st.selectbox("Cảm xúc hiện tại:", ["Hào hứng 🤩", "Hy vọng 🍀", "Quyết tâm 🔥", "Bình yên 🍵"])
            
        content = st.text_area("Điều ước tâm huyết nhất năm nay:", height=120, placeholder="Ví dụ: Năm nay mình sẽ đi du lịch Nhật Bản và để dành được 100 triệu...")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Nút bấm nằm ngoài card để nổi bật
        submitted = st.button("🚀 NIÊM PHONG & GỬI ĐI")

        # --- 5. XỬ LÝ KHI BẤM NÚT ---
        if submitted:
            if not name or not content:
                st.error("⚠️ Bạn ơi, vũ trụ cần biết tên và điều ước của bạn mới thực hiện được!")
            else:
                # Hiệu ứng Loading chuyên nghiệp
                with st.status("Đang kết nối với vệ tinh...", expanded=True) as status:
                    st.write("Đang mã hóa điều ước...")
                    time.sleep(1)
                    st.write("Đang gửi lên đám mây...")
                    time.sleep(1)
                    status.update(label="✅ Đã gửi thành công!", state="complete", expanded=False)
                
                # Hiệu ứng pháo hoa
                st.balloons()
                
                # Tạo thiệp ảnh
                card_image = create_wish_card(f"{name} - {feeling}", content)
                
                # Hiển thị kết quả
                st.markdown("---")
                st.markdown("<h3 style='color: #FFD700; text-align: center;'>🧧 LỜI NHẮN ĐÃ ĐƯỢC LƯU GIỮ</h3>", unsafe_allow_html=True)
                
                col_img, col_dl = st.columns([2, 1])
                
                with col_img:
                    st.image(card_image, caption="Thiệp xác nhận từ vũ trụ", use_column_width=True)
                
                with col_dl:
                    st.success("Điều ước của bạn đã được niêm phong an toàn!")
                    st.info("Hãy tải tấm thiệp này về máy làm kỷ niệm nhé.")
                    
                    # Nút tải về
                    st.download_button(
                        label="📥 Tải Thiệp Về Máy",
                        data=card_image,
                        file_name=f"DieuUoc_Tet2026_{name}.png",
                        mime="image/png"
                    )

if __name__ == "__main__":
    main()
