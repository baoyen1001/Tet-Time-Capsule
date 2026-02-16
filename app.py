import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime

# --- 1. CẤU HÌNH CLOUDINARY (Đã điền sẵn key của bạn) ---
cloudinary.config( 
  cloud_name = "diirli2p5", 
  api_key = "734765651265494", 
  api_secret = "MhEUSTq3Vl_KwUT_sWSZt0VPiak",
  secure = True
)
FOLDER_NAME = "BaoYen_Memories_2026"

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Bảo & Yến - Youthful Love",
    page_icon="🍭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session State cho Mục Tiêu (To-Do List)
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Cùng nhau đi Đà Lạt", "done": False, "author": "Bảo"},
        {"task": "Tiết kiệm 50 triệu", "done": False, "author": "Yến"}
    ]

# --- 3. CSS "CANDY 3D" (TƯƠI SÁNG & NĂNG ĐỘNG) ---
st.markdown("""
    <style>
    /* Import Font chữ cute */
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@500;700&display=swap');

    /* Nền Gradient Tươi Sáng */
    .stApp {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        background-attachment: fixed;
    }

    /* Tiêu đề chính */
    .main-title {
        font-family: 'Pacifico', cursive;
        font-size: 3.5rem;
        text-align: center;
        background: -webkit-linear-gradient(#ff6b6b, #556270);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 0px rgba(255,255,255,0.5);
        margin-bottom: 20px;
    }

    /* Card 3D Nổi Khối (Màu trắng sữa) */
    .card-3d {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        border: 2px solid white;
        box-shadow: 
            0 10px 20px rgba(0,0,0,0.1), 
            0 6px 6px rgba(0,0,0,0.1),
            inset 0 -5px 10px rgba(0,0,0,0.05); /* Bóng đổ trong tạo độ dày */
        transition: transform 0.3s ease;
        color: #333;
    }
    .card-3d:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }

    /* Style cho Tab (Nút chuyển đổi) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        padding: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 30px;
        color: #555;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
        color: white !important;
        transform: scale(1.05);
    }

    /* Nút bấm (Gradient) */
    div.stButton > button {
        background: linear-gradient(to right, #f83600 0%, #f9d423 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 5px 15px rgba(248, 54, 0, 0.3);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(248, 54, 0, 0.5);
    }

    /* Input fields */
    input, textarea {
        border-radius: 15px !important;
        border: 2px solid #eee !important;
        padding: 10px !important;
    }

    /* Ẩn footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. HÀM XỬ LÝ (GIỮ NGUYÊN) ---
def upload_to_cloud(file, caption, author):
    try:
        res = cloudinary.uploader.upload(file, folder=FOLDER_NAME, context=f"caption={caption}|author={author}")
        return res
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None

def get_images():
    try:
        return cloudinary.api.resources(type="upload", prefix=FOLDER_NAME, context=True, max_results=50, direction="desc").get('resources', [])
    except:
        return []

# --- 5. GIAO DIỆN CHÍNH ---
def main():
    st.markdown("<div class='main-title'>Bảo & Yến 2026 ❤️</div>", unsafe_allow_html=True)
    
    # Chia 2 Tab chính
    tab_photos, tab_goals = st.tabs(["📸 KHOẢNH KHẮC (Gallery)", "📝 MỤC TIÊU (To-Do)"])

    # --- TAB 1: ẢNH KỶ NIỆM (Lưu Cloudinary) ---
    with tab_photos:
        with st.expander("✨ Đăng ảnh mới (Click để mở)", expanded=False):
            with st.form("upload_form", clear_on_submit=True):
                col1, col2 = st.columns([1, 2])
                author = col1.selectbox("Người đăng", ["Bảo", "Yến"])
                caption = col2.text_input("Caption", placeholder="Viết gì đó cute...")
                img_file = st.file_uploader("Chọn ảnh", type=['jpg', 'png', 'jpeg'])
                
                if st.form_submit_button("Lưu Giữ Kỷ Niệm 🚀"):
                    if img_file:
                        with st.spinner("Đang bay lên mây..."):
                            if upload_to_cloud(img_file, caption, author):
                                st.balloons()
                                st.success("Đã đăng thành công!")
                                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hiển thị ảnh
        images = get_images()
        if not images:
            st.info("Chưa có ảnh nào. Hãy mở hàng đi!")
        
        for img in images:
            ctx = img.get('context', {}).get('custom', {})
            author_name = ctx.get('author', 'Ẩn danh')
            cap_text = ctx.get('caption', '')
            url = img.get('secure_url')
            
            # Card ảnh 3D
            st.markdown(f"""
            <div class="card-3d">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-weight:bold; color:#ff6b6b;">{author_name}</span>
                    <span style="color:#aaa; font-size:0.8em;">📅 {img.get('created_at', '')[:10]}</span>
                </div>
                <img src="{url}" style="width:100%; border-radius:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <div style="margin-top:15px; font-family: 'Quicksand', sans-serif; font-weight: 500;">
                    "{cap_text}"
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 2: MỤC TIÊU (To-Do List) ---
    with tab_goals:
        st.markdown("""
        <div class="card-3d" style="text-align:center; background: #fff0f5;">
            <h3 style="color:#ff6b6b; margin:0;">🎯 Cùng Nhau Phấn Đấu</h3>
            <p style="color:#888;">"Một năm mới rực rỡ đang chờ đón chúng ta"</p>
        </div>
        """, unsafe_allow_html=True)

        # Form thêm mục tiêu
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            new_task = st.text_input("Mục tiêu mới", placeholder="Ví dụ: Mua xe, Đi du lịch...", label_visibility="collapsed")
        with c2:
            who_do = st.selectbox("Ai", ["Cả 2", "Bảo", "Yến"], label_visibility="collapsed")
        with c3:
            add_btn = st.button("Thêm")

        if add_btn and new_task:
            st.session_state.goals.append({"task": new_task, "done": False, "author": who_do})
            st.rerun()

        st.markdown("---")

        # Danh sách Checklist
        if not st.session_state.goals:
            st.info("Chưa có mục tiêu nào. Hãy thêm ngay!")

        for i, goal in enumerate(st.session_state.goals):
            # Layout từng dòng mục tiêu
            col_check, col_text, col_del = st.columns([0.5, 4, 0.5])
            
            # Checkbox
            is_done = col_check.checkbox("", value=goal['done'], key=f"goal_{i}")
            if is_done != goal['done']:
                st.session_state.goals[i]['done'] = is_done
                if is_done: st.toast("Tuyệt vời! Đã hoàn thành 1 mục tiêu 🎉")
                st.rerun()

            # Nội dung text
            style_text = "text-decoration: line-through; color: #ccc;" if is_done else "color: #444; font-weight: bold;"
            col_text.markdown(f"""
                <div style="{style_text} font-family: 'Quicksand', sans-serif; padding-top: 5px;">
                    {goal['task']} <span style="background:#eee; padding:2px 8px; border-radius:10px; font-size:0.7em; margin-left:5px;">{goal['author']}</span>
                </div>
            """, unsafe_allow_html=True)

            # Nút xóa
            if col_del.button("❌", key=f"del_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

        # Thanh tiến độ
        if st.session_state.goals:
            done = sum(1 for g in st.session_state.goals if g['done'])
            total = len(st.session_state.goals)
            prog = done / total
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(prog)
            st.caption(f"Tiến độ: {int(prog*100)}% - Cố lên nhé!")

if __name__ == "__main__":
    main()
