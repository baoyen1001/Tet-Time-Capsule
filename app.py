import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime, date
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
    page_title="The Story of Us",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. KHỞI TẠO DỮ LIỆU ---
if 'timeline' not in st.session_state:
    st.session_state.timeline = [
        {"date": date(2026, 1, 10), "title": "Ngày bắt đầu", "desc": "Khoảnh khắc chúng ta chính thức bên nhau ❤️", "icon": "💘"},
        {"date": date(2026, 2, 14), "title": "Valentine Đầu Tiên", "desc": "Cùng nhau đi ăn tối lãng mạn", "icon": "🌹"},
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []
if 'love_start_date' not in st.session_state:
    st.session_state.love_start_date = date(2026, 1, 10)

# --- 4. CSS CAO CẤP (POLAROID & TIMELINE STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Nunito:wght@400;700&family=Playfair+Display:wght@700&display=swap');

    /* Nền giấy cũ Vintage sang trọng */
    .stApp {
        background-color: #fdfbf7;
        background-image: url("https://www.transparenttextures.com/patterns/cream-paper.png");
        color: #4a4a4a;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #fff;
        border-right: 1px solid #eee;
    }

    /* Typography */
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #2c3e50; }
    p, div { font-family: 'Nunito', sans-serif; }
    
    .handwriting {
        font-family: 'Dancing Script', cursive;
        font-size: 1.5rem;
        color: #555;
    }

    /* --- 1. POLAROID CARD (GALLERY) --- */
    .polaroid {
        background: white;
        padding: 15px 15px 40px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transform: rotate(-2deg);
        transition: all 0.3s ease;
        border: 1px solid #ddd;
        margin-bottom: 30px;
        text-align: center;
    }
    .polaroid:hover {
        transform: rotate(0deg) scale(1.02);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        z-index: 10;
    }
    .polaroid img { width: 100%; filter: sepia(10%); }
    .polaroid-caption {
        margin-top: 15px;
        font-family: 'Dancing Script', cursive;
        font-size: 1.3rem;
        color: #444;
    }

    /* --- 2. VERTICAL TIMELINE --- */
    .timeline-item {
        background: white;
        border-left: 4px solid #ff9a9e;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-radius: 0 10px 10px 0;
        position: relative;
    }
    .timeline-date {
        font-weight: bold; color: #ff9a9e; text-transform: uppercase; font-size: 0.8rem;
    }
    .timeline-icon {
        position: absolute; left: -22px; top: 15px; 
        background: #fff; border: 2px solid #ff9a9e; 
        border-radius: 50%; width: 35px; height: 35px; 
        text-align: center; line-height: 30px;
    }

    /* --- 3. ENVELOPE (TIME CAPSULE) --- */
    .envelope {
        background: #fff;
        border: 2px dashed #ccc;
        padding: 30px;
        text-align: center;
        border-radius: 10px;
        cursor: pointer;
    }
    .envelope.locked { background: #f9f9f9; color: #aaa; }
    .envelope.unlocked { border: 2px solid #ff9a9e; background: #fff5f7; }

    /* Button */
    div.stButton > button {
        background-color: #2c3e50; color: white; border-radius: 5px;
        font-family: 'Nunito', sans-serif; text-transform: uppercase; letter-spacing: 1px;
    }
    div.stButton > button:hover { background-color: #ff9a9e; border-color: #ff9a9e; }
    
    /* Ẩn Header */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. HÀM HỖ TRỢ ---
def get_media():
    try:
        return cloudinary.api.resources(type="upload", prefix=FOLDER_NAME, context=True, max_results=100, direction="desc").get('resources', [])
    except:
        return []

def upload_media(file, caption, author):
    try:
        return cloudinary.uploader.upload(file, folder=FOLDER_NAME, context=f"caption={caption}|author={author}")
    except:
        return None

def get_love_duration():
    delta = date.today() - st.session_state.love_start_date
    return delta.days, delta.total_seconds()

# --- 6. GIAO DIỆN CHÍNH ---
def main():
    
    # --- SIDEBAR (THANH BÊN) ---
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>Bảo & Yến</h2>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; font-size:3rem;'>∞</div>", unsafe_allow_html=True)
        
        days, seconds = get_love_duration()
        st.metric(label="Bên nhau được", value=f"{days} Ngày")
        
        st.markdown("---")
        st.markdown("### 🎵 Mood Player")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3")
        st.caption("Now playing: Our Song")
        
        st.markdown("---")
        st.info("💡 Mẹo: Vào Tab 'Hành Trình' để ghi lại những cột mốc đáng nhớ nhé!")

    # --- MAIN CONTENT ---
    st.markdown("<h1 style='text-align:center; font-size: 3.5rem;'>The Journal of Us</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888; margin-bottom:40px;'>Lưu giữ từng khoảnh khắc, trân trọng từng phút giây.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📸 POLAROID GALLERY", "📍 HÀNH TRÌNH YÊU", "💌 HỘP THƯ TƯƠNG LAI"])

    # === TAB 1: POLAROID GALLERY ===
    with tab1:
        # Nút Upload nhỏ gọn
        with st.expander("📷 Thêm ảnh vào Album"):
            with st.form("up"):
                c1, c2 = st.columns([1, 2])
                au = c1.selectbox("Photographer", ["Bảo", "Yến"])
                cap = c2.text_input("Ghi chú (Viết ngắn sẽ đẹp hơn)")
                fl = st.file_uploader("Chọn ảnh", type=['jpg','png'])
                if st.form_submit_button("Rửa ảnh"):
                    if fl:
                        upload_media(fl, cap, au)
                        st.rerun()

        media = get_media()
        if not media:
            st.caption("Chưa có tấm ảnh nào...")
        
        # Hiển thị dạng Polaroid
        cols = st.columns(3)
        for i, item in enumerate(media):
            ctx = item.get('context', {}).get('custom', {})
            url = item.get('secure_url')
            
            # Góc xoay ngẫu nhiên cho tự nhiên (-2 đến 2 độ)
            rot = (i % 5) - 2 
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="polaroid" style="transform: rotate({rot}deg);">
                    <img src="{url}" style="border: 1px solid #eee;">
                    <div class="polaroid-caption">
                        "{ctx.get('caption','')}"
                    </div>
                    <div style="font-size:0.7rem; color:#ccc; margin-top:5px; font-family:'Nunito'">
                        {item.get('created_at')[:10]} • {ctx.get('author')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 2: VERTICAL TIMELINE (Hành Trình) ===
    with tab2:
        c_add, c_view = st.columns([1, 2])
        
        with c_add:
            st.markdown("### ✨ Cột mốc mới")
            with st.form("add_event"):
                title = st.text_input("Sự kiện")
                desc = st.text_area("Mô tả ngắn")
                d = st.date_input("Ngày diễn ra")
                icon = st.selectbox("Biểu tượng", ["❤️", "✈️", "🏠", "💍", "🎉", "🚗", "🍜"])
                if st.form_submit_button("Ghim lên tường"):
                    st.session_state.timeline.append({"date": d, "title": title, "desc": desc, "icon": icon})
                    # Sắp xếp lại theo thời gian
                    st.session_state.timeline.sort(key=lambda x: x['date'], reverse=True)
                    st.rerun()
        
        with c_view:
            st.markdown("### 🗓️ Dòng thời gian")
            # Sắp xếp timeline mới nhất lên đầu
            sorted_timeline = sorted(st.session_state.timeline, key=lambda x: x['date'], reverse=True)
            
            for event in sorted_timeline:
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-icon">{event['icon']}</div>
                    <div class="timeline-date">{event['date'].strftime('Ngày %d tháng %m năm %Y')}</div>
                    <h3 style="margin: 5px 0; font-size:1.2rem;">{event['title']}</h3>
                    <p style="color:#666; font-style:italic;">{event['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 3: ENVELOPE (Time Capsule) ===
    with tab3:
        st.markdown("<h3 style='text-align:center'>Gửi tin nhắn cho chính mình</h3>", unsafe_allow_html=True)
        
        with st.expander("✍️ Viết thư tay"):
            with st.form("wish_form"):
                txt = st.text_area("Nội dung:")
                unlock = st.date_input("Ngày mở:", date.today())
                if st.form_submit_button("Dán tem & Gửi"):
                    st.session_state.wishes.append({"txt": txt, "date": date.today(), "unlock": unlock})
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        cols_w = st.columns(2)
        for i, w in enumerate(st.session_state.wishes):
            today = date.today()
            is_locked = today < w['unlock']
            
            with cols_w[i % 2]:
                if is_locked:
                    days_left = (w['unlock'] - today).days
                    st.markdown(f"""
                    <div class="envelope locked">
                        <div style="font-size:3rem;">🔒</div>
                        <h4>Thư chưa đến ngày mở</h4>
                        <p>Còn {days_left} ngày nữa</p>
                        <small>Gửi ngày: {w['date'].strftime('%d/%m/%Y')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="envelope unlocked">
                        <div style="font-size:3rem;">💌</div>
                        <h4>Thư của quá khứ</h4>
                        <p style="font-family:'Dancing Script'; font-size:1.2rem;">"{w['txt']}"</p>
                        <small>Đã mở khóa: {w['unlock'].strftime('%d/%m/%Y')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Đốt thư", key=f"del_w_{i}"):
                        st.session_state.wishes.pop(i)
                        st.rerun()

if __name__ == "__main__":
    main()
