import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
import time

# --- 1. CẤU HÌNH KẾT NỐI CLOUDINARY (Đã điền key của Bảo) ---
cloudinary.config( 
  cloud_name = "diirli2p5", 
  api_key = "734765651265494", 
  api_secret = "MhEUSTq3Vl_KwUT_sWSZt0VPiak",
  secure = True
)
FOLDER_NAME = "BaoYen_Memories_2026"

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Bảo & Yến - Our Universe",
    page_icon="🎆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. KHỞI TẠO DỮ LIỆU (SESSION STATE) ---
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Cùng nhau đón giao thừa", "done": True, "author": "Cả 2"},
        {"task": "Đi du lịch Đà Lạt", "done": False, "author": "Bảo"},
        {"task": "Tiết kiệm 100 triệu", "done": False, "author": "Yến"}
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []

# --- 4. CSS SIÊU CẤP (GALAXY + NEON + 3D) ---
st.markdown("""
    <style>
    /* Import Font chữ nghệ thuật */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;900&family=Quicksand:wght@500;700&display=swap');

    /* Nền Galaxy Huyền Ảo */
    .stApp {
        background: radial-gradient(circle at center, #2b1055 0%, #7597de 100%); /* Màu tím mộng mơ sang xanh */
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Hiệu ứng Chữ Neon Happy New Year */
    .neon-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        text-align: center;
        color: #fff;
        text-transform: uppercase;
        text-shadow: 
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #ff00de,
            0 0 30px #ff00de,
            0 0 40px #ff00de;
        animation: flicker 1.5s infinite alternate;
        margin-bottom: 0px;
    }

    /* Dòng chữ chạy "Anh iu ín kim" */
    .love-marquee {
        font-family: 'Dancing Script', cursive;
        font-size: 2.2rem;
        background: linear-gradient(to right, #ff00cc, #333399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        margin-top: -10px;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Card 3D Glassmorphism (Kính mờ) */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 40px rgba(255, 0, 222, 0.4);
    }

    /* Nút bấm Gradient */
    div.stButton > button {
        background: linear-gradient(45deg, #FF0099, #493240);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 0, 153, 0.4);
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 0, 153, 0.6);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: bold;
        font-family: 'Quicksand', sans-serif;
    }

    /* Ẩn các phần thừa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. HÀM XỬ LÝ CLOUDINARY ---
def get_media_resources():
    try:
        return cloudinary.api.resources(
            type="upload", prefix=FOLDER_NAME, context=True, max_results=100, direction="desc"
        ).get('resources', [])
    except:
        return []

def upload_media(file, caption, author):
    try:
        return cloudinary.uploader.upload(file, folder=FOLDER_NAME, context=f"caption={caption}|author={author}")
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None

# --- 6. GIAO DIỆN CHÍNH (MAIN) ---
def main():
    # --- HEADER: PHÁO HOA & LỜI CHÚC ---
    col_h1, col_h2, col_h3 = st.columns([1, 6, 1])
    with col_h1:
        st.image("https://media.giphy.com/media/26tOZ42Mg6pbTUPVS/giphy.gif") # Pháo hoa trái
    with col_h2:
        st.markdown("<div class='neon-title'>HAPPY NEW YEAR<br>2026</div>", unsafe_allow_html=True)
        st.markdown("<div class='love-marquee'>✨ Anh iu Ín Kim nhìu nhìu ✨</div>", unsafe_allow_html=True)
    with col_h3:
        st.image("https://media.giphy.com/media/26tOZ42Mg6pbTUPVS/giphy.gif") # Pháo hoa phải

    # Nút hiệu ứng đặc biệt
    if st.button("🎆 BẤM ĐỂ BẮN PHÁO HOA CHÚC MỪNG 🎆"):
        st.balloons()
        st.snow()

    st.markdown("---")

    # --- TABS CHỨC NĂNG ---
    # Tổng hợp 3 yêu cầu: Gallery, Mục tiêu (To-Do), Điều ước (Wishes)
    tab1, tab2, tab3 = st.tabs(["📸 KHOẢNH KHẮC (Gallery)", "📝 MỤC TIÊU (To-Do)", "💌 HỘP ĐIỀU ƯỚC"])

    # === TAB 1: THƯ VIỆN ẢNH/VIDEO (LƯU TRỮ VĨNH VIỄN) ===
    with tab1:
        # Form Upload (Ẩn trong Expander cho gọn)
        with st.expander("📤 Đăng ảnh/video mới (Click để mở)", expanded=False):
            with st.form("upload_form", clear_on_submit=True):
                c1, c2 = st.columns([1, 2])
                author = c1.selectbox("Người đăng", ["Bảo", "Yến"])
                caption = c2.text_input("Caption", placeholder="Viết gì đó cute...")
                files = st.file_uploader("Chọn file", type=['jpg', 'png', 'mp4'], accept_multiple_files=False)
                
                if st.form_submit_button("Lưu lên mây 🚀"):
                    if files:
                        with st.spinner("Đang gửi tín hiệu..."):
                            upload_media(files, caption, author)
                            st.success("Đã lưu thành công!")
                            st.rerun()

        # Hiển thị Gallery
        media_list = get_media_resources()
        if not media_list:
            st.info("Chưa có ảnh nào. Hãy mở hàng tấm đầu tiên đi!")
        else:
            # Layout Masonry (3 cột)
            cols = st.columns(3)
            for idx, item in enumerate(media_list):
                ctx = item.get('context', {}).get('custom', {})
                url = item.get('secure_url')
                author_name = ctx.get('author', 'Ẩn danh')
                cap_text = ctx.get('caption', '')
                fmt = item.get('format', '')

                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; color:#FFD700; font-weight:bold; margin-bottom:5px;">
                            <span>{author_name}</span>
                            <span style="font-size:0.8em; color:#ddd">📅 {item.get('created_at','')[:10]}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if fmt in ['mp4', 'mov', 'avi']:
                        st.video(url)
                    else:
                        st.image(url, use_column_width=True)
                        
                    st.markdown(f"""
                        <div style="margin-top:10px; font-family:'Quicksand'; font-style:italic;">"{cap_text}"</div>
                    </div>
                    """, unsafe_allow_html=True)

    # === TAB 2: MỤC TIÊU (TO-DO LIST) ===
    with tab2:
        st.markdown("<h3 style='text-align:center; color:#FFD700'>🎯 Cùng Nhau Phấn Đấu</h3>", unsafe_allow_html=True)
        
        # Form thêm mục tiêu
        c_add1, c_add2, c_add3 = st.columns([3, 1, 1])
        with c_add1:
            new_goal = st.text_input("Mục tiêu mới", label_visibility="collapsed", placeholder="Ví dụ: Mua xe...")
        with c_add2:
            goal_author = st.selectbox("Ai", ["Cả 2", "Bảo", "Yến"], label_visibility="collapsed")
        with c_add3:
            if st.button("Thêm") and new_goal:
                st.session_state.goals.append({"task": new_goal, "done": False, "author": goal_author})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Danh sách Checklist
        for i, goal in enumerate(st.session_state.goals):
            col_chk, col_txt, col_del = st.columns([0.5, 4, 0.5])
            
            # Checkbox
            is_done = col_chk.checkbox("", value=goal['done'], key=f"g_{i}")
            if is_done != goal['done']:
                st.session_state.goals[i]['done'] = is_done
                if is_done: st.toast("Giỏi quá! Xong 1 cái rồi nè 🎉")
                st.rerun()

            # Text decoration
            style = "text-decoration: line-through; color: #aaa;" if is_done else "color: white; font-weight: bold;"
            col_txt.markdown(f"""
                <div class="glass-card" style="padding: 10px; margin-bottom: 5px; {style}">
                    {goal['task']} <span style="font-size:0.7em; background:#FF0099; padding:2px 6px; border-radius:5px; margin-left:5px;">{goal['author']}</span>
                </div>
            """, unsafe_allow_html=True)

            if col_del.button("❌", key=f"d_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

    # === TAB 3: HỘP ĐIỀU ƯỚC (TIME CAPSULE) ===
    with tab3:
        st.markdown("<h3 style='text-align:center; color:#00ffdd'>💌 Gửi Tín Hiệu Vào Vũ Trụ</h3>", unsafe_allow_html=True)
        
        with st.form("wish_box"):
            wish_content = st.text_area("Điều ước của bạn cho năm 2026:", height=150)
            if st.form_submit_button("NIÊM PHONG ĐIỀU ƯỚC 🔐"):
                if wish_content:
                    st.session_state.wishes.append({"content": wish_content, "time": datetime.now()})
                    st.balloons()
                    st.success("Điều ước đã được gửi đi! Cuối năm hãy quay lại xem nhé.")
        
        # Hiển thị danh sách điều ước (Tạm thời lưu trong phiên làm việc)
        if st.session_state.wishes:
            st.markdown("### 🔒 Các điều ước đã niêm phong:")
            for w in st.session_state.wishes:
                st.info(f"📅 {w['time'].strftime('%d/%m/%Y')}: {w['content']}")

if __name__ == "__main__":
    main()
