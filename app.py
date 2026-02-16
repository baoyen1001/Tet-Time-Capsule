import streamlit as st
from datetime import datetime
import base64

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Bảo & Yến - Love & Goals 2026",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. KHỞI TẠO DỮ LIỆU (SESSION STATE) ---
if 'feed' not in st.session_state:
    st.session_state.feed = []
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Cùng nhau đi du lịch Đà Lạt", "done": False, "author": "Bảo"},
        {"task": "Học xong khóa tiếng Anh", "done": False, "author": "Yến"}
    ]

# --- 3. CSS 3D & DECOR SIÊU ĐẸP ---
st.markdown("""
    <style>
    /* Import Font Google */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;700&family=Playfair+Display:wght@700&display=swap');

    /* Nền Galaxy 3D */
    .stApp {
        background: radial-gradient(circle at center, #2b0000 0%, #000000 100%);
        color: white;
    }

    /* Hiệu ứng tiêu đề 3D Neon */
    .neon-text {
        font-family: 'Dancing Script', cursive;
        color: #fff;
        text-shadow: 
            0 0 5px #fff, 
            0 0 10px #ff0055, 
            0 0 20px #ff0055, 
            0 0 40px #ff0055;
        text-align: center;
        font-size: 3.8rem;
        margin-bottom: 10px;
    }

    /* Card 3D Glassmorphism (Kính mờ) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px); /* Nổi lên khi di chuột vào */
        box-shadow: 0 20px 40px rgba(255, 0, 85, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Avatar & Info */
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }
    .avatar-circle {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(45deg, #FFD700, #FF0055);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 20px;
        margin-right: 15px;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
    }
    .author-info h4 {
        margin: 0;
        color: #FFD700;
        font-family: 'Playfair Display', serif;
    }
    .author-info span {
        font-size: 0.8rem;
        color: #aaa;
    }

    /* Style cho Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.1);
        border-radius: 20px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #FF0055, #FF5500);
        color: white !important;
        font-weight: bold;
    }

    /* Nút bấm Custom */
    div.stButton > button {
        background: linear-gradient(90deg, #FF0055, #FF5500);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 5px 15px rgba(255, 85, 0, 0.4);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Ẩn linh tinh */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. HÀM XỬ LÝ ẢNH/VIDEO (QUAN TRỌNG ĐỂ HIỂN THỊ) ---
def get_base64_of_bin_file(bin_file):
    with st.spinner("Đang xử lý media..."):
        data = bin_file.read()
    return base64.b64encode(data).decode()

# --- 5. GIAO DIỆN CHÍNH ---
def main():
    # Tiêu đề Neon
    st.markdown("<div class='neon-text'>Bảo & Yến ❤️</div>", unsafe_allow_html=True)
    st.caption("✨ Nhật ký tình yêu & Mục tiêu 2026 ✨")

    # Chia Tab
    tab1, tab2 = st.tabs(["📸 KHOẢNH KHẮC (Feed)", "📝 MỤC TIÊU (To-Do)"])

    # --- TAB 1: NEWS FEED ---
    with tab1:
        # Form đăng bài
        with st.expander("➕ Đăng ảnh/video mới", expanded=False):
            with st.form("post_form", clear_on_submit=True):
                col_auth, col_cap = st.columns([1, 2])
                with col_auth:
                    author = st.selectbox("Người đăng:", ["Bảo", "Yến"])
                with col_cap:
                    caption = st.text_area("Caption:", placeholder="Viết gì đó lãng mạn đi...", height=80)
                
                uploaded_file = st.file_uploader("Chọn file:", type=['png', 'jpg', 'mp4'])
                submitted = st.form_submit_button("Đăng Ngay 🚀")

                if submitted and caption and uploaded_file:
                    # Xử lý file sang Base64
                    file_ext = uploaded_file.name.split(".")[-1].lower()
                    base64_data = get_base64_of_bin_file(uploaded_file)
                    
                    media_type = "video" if file_ext in ['mp4', 'mov'] else "image"
                    mime_type = f"video/{file_ext}" if media_type == "video" else f"image/{file_ext}"

                    st.session_state.feed.insert(0, {
                        "author": author,
                        "caption": caption,
                        "time": datetime.now().strftime("%H:%M - %d/%m"),
                        "media_data": base64_data,
                        "media_mime": mime_type,
                        "type": media_type
                    })
                    st.success("Đã đăng thành công!")
                    st.rerun()

        st.markdown("---")

        # Hiển thị bài viết
        if not st.session_state.feed:
            st.info("Chưa có bài viết nào. Hai bạn hãy mở hàng đi!")

        for post in st.session_state.feed:
            # Avatar chữ cái đầu
            avatar_char = post['author'][0]
            
            # HTML Card Container
            st.markdown(f"""
            <div class="glass-card">
                <div class="post-header">
                    <div class="avatar-circle">{avatar_char}</div>
                    <div class="author-info">
                        <h4>{post['author']}</h4>
                        <span>{post['time']}</span>
                    </div>
                </div>
                <div style="font-size: 1.1rem; margin-bottom: 15px; font-family: 'Nunito', sans-serif;">
                    {post['caption']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Hiển thị Media bằng St.Image/Video (Đặt ngoài HTML để tránh lỗi render)
            if post['type'] == 'image':
                # Decode base64 để hiển thị bằng st.image (Cách ổn định nhất)
                img_bytes = base64.b64decode(post['media_data'])
                st.image(img_bytes, use_column_width=True)
            elif post['type'] == 'video':
                # Video cần dùng HTML tag vì st.video đôi khi kén base64
                video_html = f'''
                    <video width="100%" controls style="border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                    <source src="data:{post['media_mime']};base64,{post['media_data']}">
                    </video>
                '''
                st.markdown(video_html, unsafe_allow_html=True)
            
            # Khoảng cách giữa các bài
            st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # --- TAB 2: TO-DO LIST (MỤC TIÊU) ---
    with tab2:
        st.markdown("<h3 style='text-align: center; color: #FFD700;'>🎯 Mục Tiêu Năm Nay</h3>", unsafe_allow_html=True)
        
        # Form thêm mục tiêu
        with st.form("goal_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_task = st.text_input("Mục tiêu mới:", placeholder="Ví dụ: Mua xe mới...")
            with col2:
                who = st.selectbox("Ai thực hiện?", ["Cả 2", "Bảo", "Yến"])
            
            if st.form_submit_button("Thêm mục tiêu"):
                if new_task:
                    st.session_state.goals.append({"task": new_task, "done": False, "author": who})
                    st.rerun()

        # Danh sách mục tiêu (Dạng Checklist đẹp)
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        for i, goal in enumerate(st.session_state.goals):
            # Tạo khung cho từng mục tiêu
            col_check, col_text, col_del = st.columns([1, 8, 1])
            
            with col_check:
                is_done = st.checkbox("", value=goal['done'], key=f"check_{i}")
            
            # Cập nhật trạng thái
            if is_done != goal['done']:
                st.session_state.goals[i]['done'] = is_done
                st.rerun()

            with col_text:
                status_style = "text-decoration: line-through; color: gray;" if is_done else "color: white; font-weight: bold;"
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; {status_style}">
                        {goal['task']} <span style="font-size: 0.8em; color: #FFD700; margin-left: 10px;">({goal['author']})</span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_del:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.goals.pop(i)
                    st.rerun()
        
        # Thanh tiến độ
        if st.session_state.goals:
            done_count = sum(1 for g in st.session_state.goals if g['done'])
            total = len(st.session_state.goals)
            progress = done_count / total
            st.markdown("---")
            st.write(f"Tiến độ hoàn thành: {int(progress*100)}%")
            st.progress(progress)
            if progress == 1.0:
                st.balloons()
                st.success("Chúc mừng hai bạn đã hoàn thành mọi mục tiêu! 🎉")

if __name__ == "__main__":
    main()
