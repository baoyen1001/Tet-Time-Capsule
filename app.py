import streamlit as st
from datetime import datetime
import base64

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Bảo & Yến - Our Memories",
    page_icon="💑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. QUẢN LÝ DỮ LIỆU TẠM THỜI (SESSION STATE) ---
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {
            "type": "image",
            "url": "https://images.unsplash.com/photo-1548625361-9f939e3c4e33?q=80&w=1000&auto=format&fit=crop",
            "caption": "Chào Tết 2026! Năm đầu tiên của tụi mình ✨",
            "author": "System",
            "date": "Giao thừa 2026",
            "likes": 999
        }
    ]

# --- 3. CSS "ĐẲNG CẤP" (GLASSMORPHISM & MOBILE UI) ---
st.markdown("""
    <style>
    /* Import Font xịn từ Google */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;700&family=Playfair+Display:wght@700&display=swap');

    /* Nền sang trọng (Màu đỏ nhung kết hợp vàng kim) */
    .stApp {
        background: linear-gradient(135deg, #4a0000 0%, #8b0000 50%, #2e0202 100%);
        background-attachment: fixed;
    }

    /* Ẩn các thành phần thừa của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tiêu đề chính */
    .main-title {
        font-family: 'Dancing Script', cursive;
        color: #FFD700;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        margin-bottom: 10px;
    }
    
    .sub-title {
        font-family: 'Playfair Display', serif;
        color: #ffcccc;
        text-align: center;
        font-style: italic;
        margin-bottom: 30px;
        font-size: 1.2rem;
    }

    /* Card bài viết (Giống Facebook nhưng đẹp hơn) */
    .post-card {
        background: rgba(255, 255, 255, 0.1); /* Hiệu ứng kính mờ */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        color: white;
    }

    .author-name {
        font-weight: bold;
        color: #FFD700;
        font-size: 1.1rem;
        font-family: 'Nunito', sans-serif;
    }
    
    .post-date {
        font-size: 0.8rem;
        color: #ccc;
        margin-bottom: 10px;
    }

    .post-caption {
        font-size: 1.1rem;
        margin-bottom: 15px;
        line-height: 1.5;
        font-family: 'Nunito', sans-serif;
    }

    /* Nút bấm Upload */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: #5e0a0a;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #FFD700;
    }
    
    /* Input field */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. GIAO DIỆN CHÍNH ---
def main():
    # Header
    st.markdown("<div class='main-title'>Bảo & Yến</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>✨ Our Digital Home • Tết 2026 ✨</div>", unsafe_allow_html=True)

    # Nút đăng bài (Dạng Expander để gọn giao diện)
    with st.expander("📸 Đăng khoảnh khắc mới"):
        with st.form("upload_form", clear_on_submit=True):
            author = st.selectbox("Bạn là ai?", ["Bảo đẹp trai", "Yến xinh gái"])
            caption = st.text_area("Viết gì đó...", placeholder="Hôm nay tụi mình đi đâu thế?")
            uploaded_file = st.file_uploader("Chọn ảnh/video", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])
            
            submit_btn = st.form_submit_button("Đăng Lên Tường 🚀")
            
            if submit_btn and uploaded_file and caption:
                bytes_data = uploaded_file.getvalue()
                b64_data = base64.b64encode(bytes_data).decode()
                
                file_type = "video" if uploaded_file.type.startswith("video") else "image"
                mime_type = uploaded_file.type
                
                new_post = {
                    "type": file_type,
                    "data": b64_data,
                    "mime": mime_type,
                    "caption": caption,
                    "author": author,
                    "date": datetime.now().strftime("%H:%M • %d/%m/%Y"),
                    "likes": 0
                }
                
                st.session_state.posts.insert(0, new_post)
                st.success("Đã đăng thành công!")
                st.rerun()

    st.markdown("---")

    # --- 5. HIỂN THỊ NEWS FEED ---
    if not st.session_state.posts:
        st.info("Chưa có bài viết nào. Hãy là người đầu tiên đăng bài nhé!")
    
    for i, post in enumerate(st.session_state.posts):
        st.markdown(f"""
        <div class="post-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="author-name">{post['author']}</div>
                    <div class="post-date">{post['date']}</div>
                </div>
                <div style="font-size: 1.5rem;">❤️</div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.2); margin: 10px 0;">
            <div class="post-caption">{post['caption']}</div>
        </div>
        """, unsafe_allow_html=True)

        if post['type'] == 'image':
            if 'url' in post:
                st.image(post['url'], use_column_width=True)
            else:
                st.markdown(f'<img src="data:{post["mime"]};base64,{post["data"]}" style="width:100%; border-radius: 10px;">', unsafe_allow_html=True)
        
        elif post['type'] == 'video':
            st.markdown(f"""
                <video width="100%" controls style="border-radius: 10px;">
                    <source src="data:{post['mime']};base64,{post['data']}" type="{post['mime']}">
                    Trình duyệt không hỗ trợ video.
                </video>
            """, unsafe_allow_html=True)
            
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"Yêu thích", key=f"like_{i}"):
                st.toast("Đã thả tim! ❤️")
        
        st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
