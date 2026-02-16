import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime

# --- 1. CẤU HÌNH KẾT NỐI (ĐÃ TÍCH HỢP KEY CỦA BẠN) ---
cloudinary.config( 
  cloud_name = "diirli2p5", 
  api_key = "734765651265494", 
  api_secret = "MhEUSTq3Vl_KwUT_sWSZt0VPiak",
  secure = True
)

# Tên thư mục trên Cloudinary (Nơi chứa ảnh của 2 bạn)
FOLDER_NAME = "BaoYen_Memories_2026"

# --- 2. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Bảo & Yến - Our Forever Gallery",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 3. CSS GIAO DIỆN "GLASSMORPHISM" (KÍNH MỜ SANG TRỌNG) ---
st.markdown("""
    <style>
    /* Import Font đẹp */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;700&display=swap');

    /* Nền Galaxy Tối */
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%);
        color: white;
    }

    /* Tiêu đề Neon */
    .neon-title {
        font-family: 'Dancing Script', cursive;
        text-align: center;
        font-size: 3.5rem;
        color: #fff;
        text-shadow: 0 0 10px #ff00de, 0 0 20px #ff00de, 0 0 40px #ff00de;
        margin-bottom: 10px;
    }

    /* Card chứa ảnh (Hiệu ứng kính) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 0, 222, 0.5);
    }

    /* Thông tin người đăng */
    .author-tag {
        font-size: 0.9rem;
        font-weight: bold;
        color: #FFD700;
        margin-bottom: 5px;
        font-family: 'Nunito', sans-serif;
    }
    
    .caption-text {
        font-size: 1rem;
        color: #e0e0e0;
        font-style: italic;
        margin-bottom: 10px;
        font-family: 'Nunito', sans-serif;
    }

    /* Nút bấm đẹp */
    .stButton > button {
        background: linear-gradient(45deg, #ff00de, #00d4ff);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        width: 100%;
        padding: 10px;
    }
    
    /* Ẩn các phần thừa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. HÀM XỬ LÝ CLOUDINARY ---
def upload_to_cloud(file, caption, author):
    try:
        # Upload file lên Cloudinary kèm thông tin (context)
        res = cloudinary.uploader.upload(
            file, 
            folder=FOLDER_NAME,
            context=f"caption={caption}|author={author}"
        )
        return res
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return None

def get_images_from_cloud():
    try:
        # Lấy danh sách ảnh từ folder về
        res = cloudinary.api.resources(
            type="upload",
            prefix=FOLDER_NAME,
            context=True, # Lấy kèm caption
            max_results=50,
            direction="desc" # Ảnh mới nhất lên đầu
        )
        return res.get('resources', [])
    except:
        return []

# --- 5. GIAO DIỆN CHÍNH ---
def main():
    st.markdown("<div class='neon-title'>Bảo & Yến ❤️</div>", unsafe_allow_html=True)
    st.caption("✨ Nơi lưu giữ những khoảnh khắc vĩnh cửu ✨")

    # --- FORM ĐĂNG ẢNH ---
    with st.expander("📸 ĐĂNG KHOẢNH KHẮC MỚI", expanded=False):
        with st.form("upload_form", clear_on_submit=True):
            col1, col2 = st.columns([1, 2])
            author = col1.selectbox("Người đăng:", ["Bảo", "Yến"])
            caption = col2.text_input("Caption:", placeholder="Viết điều gì đó lãng mạn...")
            
            uploaded_file = st.file_uploader("Chọn ảnh/video:", type=['jpg', 'png', 'jpeg', 'mp4'])
            
            submit_btn = st.form_submit_button("LƯU LÊN MÂY ☁️")
            
            if submit_btn and uploaded_file:
                with st.spinner("Đang gửi tín hiệu lên vệ tinh..."):
                    result = upload_to_cloud(uploaded_file, caption, author)
                    if result:
                        st.success("Đã lưu thành công! Ảnh sẽ không bao giờ mất.")
                        st.rerun() # Tải lại trang để hiện ảnh ngay

    st.markdown("---")

    # --- HIỂN THỊ KHO ẢNH (GALLERY) ---
    st.subheader("🎞️ Ký Ức Của Chúng Ta")
    
    # Lấy ảnh từ Cloud về
    images = get_images_from_cloud()
    
    if not images:
        st.info("Chưa có ảnh nào. Hai bạn hãy mở hàng đi nào!")
    else:
        # Hiển thị dạng lưới (Grid)
        for img in images:
            # Lấy thông tin metadata
            context = img.get('context', {}).get('custom', {})
            author_name = context.get('author', 'Người giấu mặt')
            caption_content = context.get('caption', '...')
            created_at = img.get('created_at', '')[:10] # Lấy ngày đăng
            img_url = img.get('secure_url')
            
            # Giao diện từng Card
            st.markdown(f"""
            <div class="glass-card">
                <div class="author-tag">Avatar: {author_name} • <span style="font-weight:normal; color:#ccc">{created_at}</span></div>
                <div class="caption-text">"{caption_content}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hiển thị ảnh/video
            if "video" in img.get('resource_type', ''):
                st.video(img_url)
            else:
                st.image(img_url, use_column_width=True)
            
            # Khoảng cách
            st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
