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
    page_title="Bảo & Yến - Official Site",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. KHỞI TẠO DỮ LIỆU ---
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Chụp bộ ảnh Tết", "done": True, "author": "Cả 2"},
        {"task": "Đi du lịch Đà Lạt", "done": False, "author": "Bảo"},
        {"task": "Tiết kiệm 100 triệu", "done": False, "author": "Yến"}
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []

# --- 4. CSS CHUYÊN NGHIỆP (PASTEL BLUE & PINK THEME) ---
st.markdown("""
    <style>
    /* Import Font Google Xịn Xò */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;700&display=swap');

    /* Nền Gradient Pastel Siêu Mượt */
    .stApp {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); /* Tím nhạt pha Hồng */
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%); /* Xanh Pastel */
        /* Phối màu chuẩn Pastel Blue - Pink */
        background-image: linear-gradient(to top, #a18cd1 0%, #fbc2eb 100%);
        background-attachment: fixed;
    }

    /* Tiêu đề chính */
    .hero-title {
        font-family: 'Dancing Script', cursive;
        font-size: 5rem;
        text-align: center;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 0px;
        padding-top: 20px;
    }

    .sub-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.5rem;
        text-align: center;
        color: #fff;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Card 3D Chuyên nghiệp (Glassmorphism Light) */
    .pro-card {
        background: rgba(255, 255, 255, 0.75); /* Màu trắng sữa bán trong suốt */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* Bóng đổ mềm */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #4a4a4a; /* Chữ màu xám đậm dễ đọc trên nền sáng */
    }
    
    .pro-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.9);
    }

    /* Tùy chỉnh Tabs */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 20px;
        background-color: rgba(255,255,255,0.2);
        padding: 15px;
        border-radius: 50px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: white;
        font-family: 'Nunito', sans-serif;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #a18cd1 !important;
        border-radius: 30px;
        padding: 5px 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* Nút bấm Gradient */
    div.stButton > button {
        background: linear-gradient(to right, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        color: #555;
        border: none;
        border-radius: 30px;
        padding: 12px 25px;
        font-weight: bold;
        font-family: 'Nunito', sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(to right, #fecfef 0%, #ff9a9e 100%);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }

    /* Input & Textarea */
    input, textarea {
        border-radius: 15px !important;
        border: 2px solid #fff !important;
        background-color: rgba(255,255,255,0.8) !important;
        color: #333 !important;
    }

    /* Ẩn footer mặc định */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
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
    st.markdown("<div class='hero-title'>Bảo & Yến</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>💕 Our Love Journey 2026 💕</div>", unsafe_allow_html=True)

    # Nút Pháo Hoa (Hoạt động 100%)
    col_c1, col_c2, col_c3 = st.columns([1,2,1])
    with col_c2:
        if st.button("🎆 BẤM VÀO ĐÂY ĐỂ BẮN PHÁO HOA 🎆"):
            st.balloons()
            time.sleep(1)
            st.snow()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📸 KHOẢNH KHẮC", "📝 MỤC TIÊU", "💌 ĐIỀU ƯỚC"])

    # === TAB 1: GALLERY ===
    with tab1:
        # Form upload ẩn
        with st.expander("📤 Đăng ảnh mới", expanded=False):
            with st.form("up_form", clear_on_submit=True):
                c1, c2 = st.columns([1, 2])
                author = c1.selectbox("Người đăng", ["Bảo", "Yến"])
                caption = c2.text_input("Caption", placeholder="Viết dòng tâm trạng...")
                file = st.file_uploader("Chọn ảnh/video", type=['jpg','png','mp4'])
                if st.form_submit_button("Lưu Kỷ Niệm"):
                    if file:
                        with st.spinner("Đang xử lý..."):
                            upload_media(file, caption, author)
                            st.success("Đã lưu!")
                            st.rerun()
        
        # Hiển thị ảnh
        media = get_media()
        if not media:
            st.info("Chưa có ảnh nào. Hãy upload ngay!")
        
        # Grid 3 cột
        cols = st.columns(3)
        for i, item in enumerate(media):
            ctx = item.get('context', {}).get('custom', {})
            url = item.get('secure_url')
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="pro-card">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <span style="font-weight:bold; color:#ff9a9e;">{ctx.get('author','Author')}</span>
                        <span style="font-size:0.8em; color:#888;">{item.get('created_at','')[:10]}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if item.get('format') == 'mp4':
                    st.video(url)
                else:
                    st.image(url, use_column_width=True)
                
                st.markdown(f"""
                    <div style="margin-top:10px; font-family:'Nunito'; font-weight:600; color:#555;">
                        "{ctx.get('caption','')}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 2: MỤC TIÊU ===
    with tab2:
        # Form thêm
        c_add1, c_add2, c_add3 = st.columns([3, 1, 1])
        with c_add1:
            new_task = st.text_input("Mục tiêu mới", label_visibility="collapsed", placeholder="Nhập mục tiêu...")
        with c_add2:
            who = st.selectbox("Ai", ["Cả 2", "Bảo", "Yến"], label_visibility="collapsed")
        with c_add3:
            if st.button("Thêm") and new_task:
                st.session_state.goals.append({"task": new_task, "done": False, "author": who})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # List
        for i, g in enumerate(st.session_state.goals):
            c_chk, c_txt, c_del = st.columns([0.5, 5, 0.5])
            
            done = c_chk.checkbox("", value=g['done'], key=f"g{i}")
            if done != g['done']:
                st.session_state.goals[i]['done'] = done
                st.rerun()
            
            # Style text
            style = "text-decoration: line-through; color: #aaa;" if done else "color: #444; font-weight:bold;"
            bg = "#e8f5e9" if done else "rgba(255,255,255,0.6)"
            
            c_txt.markdown(f"""
                <div style="background:{bg}; padding:10px; border-radius:10px; border:1px solid #ddd; {style}">
                    {g['task']} <span style="font-size:0.7em; background:#ff9a9e; color:white; padding:2px 8px; border-radius:10px; margin-left:5px;">{g['author']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if c_del.button("✖️", key=f"d{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

    # === TAB 3: ĐIỀU ƯỚC ===
    with tab3:
        st.markdown("<h3 style='text-align:center; color:#fff; font-family:Nunito'>💌 Gửi Tín Hiệu Vào Vũ Trụ</h3>", unsafe_allow_html=True)
        with st.form("wish"):
            txt = st.text_area("Điều ước 2026:", height=150)
            if st.form_submit_button("NIÊM PHONG"):
                if txt:
                    st.session_state.wishes.append({"txt": txt, "date": datetime.now()})
                    st.success("Đã gửi!")
                    st.balloons()
        
        if st.session_state.wishes:
            for w in st.session_state.wishes:
                st.info(f"📅 {w['date'].strftime('%d/%m/%Y')}: {w['txt']}")

if __name__ == "__main__":
    main()
