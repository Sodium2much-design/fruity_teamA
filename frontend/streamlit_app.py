import streamlit as st
from PIL import Image
import os
import time
import requests

# ตั้งค่า UI
st.set_page_config(page_title="Fruit Juice Dispenser", page_icon="🍹", layout="wide")
st.title("🍹 Fruit Juice Dispenser")

# สร้างคอลัมน์สำหรับ Layout
col1, col2 = st.columns([2, 1])

# เส้นทางไปยังโฟลเดอร์ที่เก็บภาพ
image_folder = "frontend/image"  # ไฟล์ทั้งหมดอยู่ในโฟลเดอร์นี้

juice_options = ['starfruit', 'dragonfruit', 'mangosteen', 'melon', 'lemon', 'watermelon']

# Mapping ชื่อที่แสดงกับชื่อที่เก็บข้อมูล
juice_display_name = {
    'starfruit': 'ดาวน้อยน่าอร่อยจังเลย',
    'dragonfruit': 'แก้วมังกรแต่ไม่มังใจ',
    'mangosteen': 'มังคุเทศ',
    'melon': 'เมล่อนซ่อนใจ',
    'lemon': 'เลม่อนแสนซน',
    'watermelon': 'แตงโม แตงโม แตงโม'
}

juice_images = {
    'starfruit': 'starfruit.png',
    'dragonfruit': 'dragonfruit.png',
    'mangosteen': 'mangosteen.png',
    'melon': 'melon.png',
    'lemon': 'lemon.png',
    'watermelon': 'watermelon.png'
}

juice_gifs = {
    'starfruit': 'starfruit_glass.gif',
    'dragonfruit': 'dragonfruit_glass.gif',
    'mangosteen': 'mangosteen_glass.gif',
    'melon': 'melon_glass.gif',
    'lemon': 'lemon_glass.gif',
    'watermelon': 'watermelon_glass.gif'
}

juice_full = {
    'starfruit': 'starfruit_full.png',
    'dragonfruit': 'dragonfruit_full.png',
    'mangosteen': 'mangosteen_full.png',
    'melon': 'melon_full.png',
    'lemon': 'lemon_full.png',
    'watermelon': 'watermelon_full.png'
}

# ใช้ placeholder เพื่อแสดงข้อความใน col2 (แก้วเปล่า)
empty_glass_placeholder = col2.empty()

# ฟังก์ชันสำหรับโหลดภาพจากไฟล์
def load_image(image_path):
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        st.warning(f"Image not found: {image_path}")
        return None

# ฟังก์ชันเชื่อมต่อกับ FastAPI เพื่อเพิ่มสถิติ
def update_juice_click(juice_type):
    url = f"http://127.0.0.1:8000/juices/{juice_type}/click"
    response = requests.post(url)
    return response.json()

# ฟังก์ชันเพื่อดึงข้อมูลสถิติจาก FastAPI
def get_juice_stats():
    url = "http://127.0.0.1:8000/juices/"
    response = requests.get(url)
    return response.json()

# การแสดงสถิติการกดปุ่ม
st.sidebar.header("Juice Stats")

# ฟังก์ชันที่แสดงข้อมูลสถิติ
def get_sidebar_stats_markdown():
    juice_stats = get_juice_stats()
    sorted_stats = sorted(juice_stats, key=lambda x: x['click_count'], reverse=True)

    md = ""
    for stat in sorted_stats:
        name = stat['name'].capitalize()
        count = stat['click_count']
        md += f"🥤 **{name} Juice**: {count} clicks\n\n"  # เอา backticks ออก
    return md

sidebar_stats_container = st.sidebar.empty()
sidebar_stats_container.markdown(get_sidebar_stats_markdown())

# การเลือกน้ำผลไม้
with col1:
    st.header("Choose Your Juice")

    # แสดงแก้วเปล่าใน col2
    empty_glass_path = os.path.join(image_folder, 'glass.png')
    glass_img = load_image(empty_glass_path)
    if glass_img:
        empty_glass_placeholder.image(glass_img, caption="Empty Glass")

    # การเลือกน้ำผลไม้
    for i in range(0, len(juice_options), 3):
        juice_col1, juice_col2, juice_col3 = st.columns([1, 1, 1])
        for j, juice in enumerate(juice_options[i:i+3]):
            with [juice_col1, juice_col2, juice_col3][j]:
                image_path = os.path.join(image_folder, juice_images[juice])

                # โหลดและแสดงภาพน้ำผลไม้
                img = load_image(image_path)
                if img:
                    st.image(img, caption=f"{juice_display_name[juice]}", width=140)

                if st.button(f"🥤 Dispense {juice_display_name[juice]}"):

                    # แสดงภาพแก้วเปล่าใน col2
                    glass_img = load_image(empty_glass_path)
                    if glass_img:
                        empty_glass_placeholder.image(glass_img, caption="Empty Glass")

                    # รอ 
                    time.sleep(1)

                    # แสดง GIF การเติมน้ำลงในแก้วที่แตกต่างกันไปตามผลไม้
                    gif_path = os.path.join(image_folder, juice_gifs[juice])
                    if os.path.exists(gif_path):
                        empty_glass_placeholder.image(gif_path, caption=f"Dispensing {juice_display_name[juice]} Juice")

                    # รอจนกว่าจะเห็นอนิเมชั่น
                    time.sleep(4)

                    # แสดงข้อความ "Done" 
                    empty_glass_placeholder.empty()
                    full_image_path = os.path.join(image_folder, juice_full[juice])
                    if os.path.exists(full_image_path):
                        empty_glass_placeholder.image(full_image_path, caption=f"Done dispensing {juice_display_name[juice]} juice!")

                    # ส่งคำขอไปยัง FastAPI เพื่อเพิ่มสถิติ
                    update_juice_click(juice)

                    # รีเฟรชข้อมูลสถิติใน sidebar
                    sidebar_stats_container.markdown(get_sidebar_stats_markdown())

                    # ลบข้อความออกหลังจาก 1 วินาที
                    time.sleep(2)

                    # แสดงแก้วเปล่าอีกครั้งหลังจากทำการเสร็จสิ้น
                    glass_img = load_image(empty_glass_path)
                    if glass_img:
                        empty_glass_placeholder.image(glass_img, caption="Empty Glass")
