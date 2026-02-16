import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
import time

# --- 1. CẤU HÌNH KẾT NỐI (Key của Bảo) ---
cloudinary.config( 
  cloud_name = "diirli2p5", 
  api_key = "734765651265494", 
  api_secret = "MhEUSTq3Vl_KwUT_sWSZt0VPiak",
  secure = True
)
FOLDER_NAME = "BaoYen_Memories_2026"

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Bảo & Yến - Tet 2026",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. KHỞI TẠO DỮ LIỆU ---
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Chụp bộ ảnh Tết áo dài", "done": True, "author": "Cả 2"},
        {"task": "Đi du lịch Đà Lạt", "done": False, "author": "Bảo"},
        {"task": "Tiết kiệm 100 triệu", "done": False, "author": "Yến"}
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []

# --- 4. CSS & HIỆU ỨNG (KHÔNG DÙNG LINK NGOÀI ĐỂ TRÁNH LỖI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;700&family=Pacifico&display=swap');

    /* Nền Gradient Pastel */
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #a1c4fd 100%);
        background-attachment: fixed;
    }

    /* --- HIỆU ỨNG HOA RƠI & PHÁO HOA BẰNG EMOJI (SIÊU BỀN) --- */
    
    /* 1. Lớp chứa hiệu ứng nền */
    .effect-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 1;
        overflow: hidden;
    }

    /* 2. Định nghĩa hạt rơi (Hoa đào) */
    .particle {
        position: absolute;
        top: -10%;
        font-size: 25px;
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        0% { transform: translateY(0vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }

    /* Tạo vị trí ngẫu nhiên cho hoa */
    .p1 { left: 10%; animation-duration: 10s; animation-delay: 0s; }
    .p2 { left: 25%; animation-duration: 15s; animation-delay: 2s; font-size: 20px;}
    .p3 { left: 50%; animation-duration: 12s; animation-delay: 4s; }
    .p4 { left: 75%; animation-duration: 8s; animation-delay: 1s; font-size: 30px;}
    .p5 { left: 90%; animation-duration: 18s; animation-delay: 3s; }

    /* 3. Hiệu ứng Pháo hoa (CSS thuần - Tạo vòng tròn nổ) */
    @keyframes firework {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(1.5); opacity: 0; }
    }
    
    .firework-css {
        position: absolute;
        width: 10px; height: 10px;
        border-radius: 50%;
        box-shadow: 
            0 0 0 5px #ff00de,
            0 0 0 10px #00d4ff,
            0 0 0 20px #ff9a9e;
        animation: firework 2s infinite;
    }
    .fw1 { top: 10%; left: 10%; animation-delay: 0.5s; }
    .fw2 { top: 15%; right: 10%; animation-delay: 1.2s; box-shadow: 0 0 0 5px yellow, 0 0 0 15px red; }

    /* --- GIAO DIỆN CHÍNH --- */
    .hero-title {
        font-family: 'Pacifico', cursive;
        font-size: 4.5rem;
        text-align: center;
        color: #fff;
        text-shadow: 3px 3px 0px rgba(255, 105, 180, 0.6);
        margin-top: -20px;
        position: relative; z-index: 10;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* Card nội dung */
    .content-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        position: relative; z-index: 10;
        transition: transform 0.2s;
    }
    .content-card:hover { transform: translateY(-3px); }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center; gap: 20px;
        background: rgba(255,255,255,0.4);
        padding: 10px; border-radius: 50px;
        margin-bottom: 20px; position: relative; z-index: 10;
    }
    .stTabs [aria-selected="true"] {
        background: white !important; color: #ff758c !important;
        border-radius: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    div[data-testid="stMarkdownContainer"] p { font-family: 'Nunito', sans-serif; }

    /* Button */
    div.stButton > button {
        background: linear-gradient(to right, #ff758c 0%, #ff7eb3 100%);
        color: white; border: none; border-radius: 20px;
        font-weight: bold; padding: 0.5rem 1rem;
        box-shadow: 0 4px 10px rgba(255, 117, 140, 0.4);
    }
    div.stButton > button:hover { transform: scale(1.05); }

    /* Ẩn Header */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    
    <div class="effect-container">
        <div class="particle p1">🌸</div>
        <div class="particle p2">✨</div>
        <div class="particle p3">🌸</div>
        <div class="particle p4">🍀</div>
        <div class="particle p5">🌸</div>
        
        <div class="firework-css fw1"></div>
        <div class="firework-css fw2"></div>
    </div>
""", unsafe_allow_html=True)

# --- 5. HÀM CLOUDINARY ---
def get_media():
    try:
        return cloudinary.api.resources(type="upload", prefix=FOLDER_NAME, context=True, max_results=50, direction="desc").get('resources', [])
    except:
        return []

def upload_media(file, caption, author):
    try:
        return cloudinary.uploader.upload(file, folder=FOLDER_NAME, context=f"caption={caption}|author={author}")
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None

# --- 6. GIAO DIỆN CHÍNH ---
def main():
    # Header
    st.markdown("<div class='hero-title'>Tết 2026: Bảo & Yến ❤️</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; font-weight:bold; position:relative; z-index:10; font-size:1.2rem;'>🌸 Xuân Bính Ngọ - Bên Nhau Trọn Đời 🌸</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📸 KHOẢNH KHẮC", "📝 MỤC TIÊU", "💌 ĐIỀU ƯỚC"])

    # === TAB 1: THƯ VIỆN ẢNH ===
    with tab1:
        with st.expander("📤 Đăng ảnh/video mới (Click để mở)", expanded=False):
            with st.form("up_form", clear_on_submit=True):
                c1, c2 = st.columns([1, 2])
                author = c1.selectbox("Người đăng", ["Bảo", "Yến"])
                caption = c2.text_input("Caption", placeholder="Nhập chú thích...")
                file = st.file_uploader("Chọn ảnh/video", type=['jpg','png','mp4'])
                if st.form_submit_button("Lưu Kỷ Niệm"):
                    if file:
                        with st.spinner("Đang lưu..."):
                            upload_media(file, caption, author)
                            st.success("Đã lưu!")
                            time.sleep(1)
                            st.rerun()

        media = get_media()
        if not media:
            st.info("Chưa có ảnh nào.")
        
        cols = st.columns(3)
        for i, item in enumerate(media):
            ctx = item.get('context', {}).get('custom', {})
            url = item.get('secure_url')
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="content-card">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="font-weight:bold; color:#ff758c;">{ctx.get('author','Author')}</span>
                        <span style="font-size:0.8em; color:#888;">{item.get('created_at','')[:10]}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if item.get('format') == 'mp4':
                    st.video(url)
                else:
                    st.image(url, use_column_width=True)
                
                st.markdown(f"""
                    <div style="margin-top:10px; font-family:'Nunito'; color:#555;">"{ctx.get('caption','')}"</div>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 2: MỤC TIÊU ===
    with tab2:
        c_add1, c_add2, c_add3 = st.columns([3, 1, 1])
        with c_add1:
            new_task = st.text_input("Mục tiêu mới", label_visibility="collapsed", placeholder="Nhập mục tiêu...")
        with c_add2:
            who = st.selectbox("Ai", ["Cả 2", "Bảo", "Yến"], label_visibility="collapsed", key="who_goal")
        with c_add3:
            if st.button("Thêm") and new_task:
                st.session_state.goals.append({"task": new_task, "done": False, "author": who})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        for i, g in enumerate(st.session_state.goals):
            c_chk, c_txt, c_del = st.columns([0.5, 5, 0.5])
            
            done = c_chk.checkbox("", value=g['done'], key=f"g{i}")
            if done != g['done']:
                st.session_state.goals[i]['done'] = done
                st.rerun()
            
            style = "text-decoration: line-through; color: #aaa;" if done else "color: #444; font-weight:bold;"
            
            c_txt.markdown(f"""
                <div class="content-card" style="padding:10px; margin-bottom:5px; {style}">
                    {g['task']} <span style="font-size:0.7em; background:#ff9a9e; color:white; padding:2px 8px; border-radius:10px; margin-left:5px;">{g['author']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if c_del.button("🗑️", key=f"d{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

    # === TAB 3: ĐIỀU ƯỚC ===
    with tab3:
        st.markdown("<h3 style='text-align:center; color:#fff; font-family:Nunito'>💌 Gửi Tín Hiệu Vào Vũ Trụ</h3>", unsafe_allow_html=True)
        
        with st.form("wish"):
            txt = st.text_area("Điều ước 2026:", height=100)
            if st.form_submit_button("Gửi đi ❤️"):
                if txt:
                    st.session_state.wishes.append({"txt": txt, "date": datetime.now()})
                    st.success("Đã gửi!")
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.wishes:
            for i, w in enumerate(st.session_state.wishes):
                col_content, col_delete = st.columns([8, 1])
                with col_content:
                    st.markdown(f"""
                    <div class="content-card">
                        <span style="font-weight:bold; color:#ff758c;">📅 {w['date'].strftime('%d/%m/%Y')}</span><br>
                        {w['txt']}
                    </div>
                    """, unsafe_allow_html=True)
                with col_delete:
                    st.markdown("<br>", unsafe_allow_html=True) 
                    if st.button("❌", key=f"del_wish_{i}"):
                        st.session_state.wishes.pop(i)
                        st.rerun()
        else:
            st.info("Chưa có điều ước nào.")

if __name__ == "__main__":
    main()
