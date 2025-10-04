import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ตั้งค่า UI
st.set_page_config(page_title="Database - Juice Dispenser", page_icon="🍹", layout="wide")
st.title("🍹 Fruit Juice Database")

# ฟังก์ชันเพื่อดึงข้อมูลจาก FastAPI
def get_juice_stats():
    url = "http://127.0.0.1:8000/juices/"  # URL ของ FastAPI ที่ให้ข้อมูลน้ำผลไม้
    response = requests.get(url)
    return response.json()

# ฟังก์ชันแสดงข้อมูลในตาราง, กราฟแท่ง และกราฟวงกลม
def display_juice_data():
    juice_stats = get_juice_stats()  # ดึงข้อมูลจาก FastAPI
    juice_data = pd.DataFrame(juice_stats)  # แปลงข้อมูลเป็น DataFrame

    juice_data.rename(columns={'name': 'Juice'}, inplace=True)

    # คำนวณเปอร์เซ็นต์การคลิก
    total_clicks = juice_data['click_count'].sum()
    juice_data['percentage'] = (juice_data['click_count'] / total_clicks) * 100 if total_clicks > 0 else [0] * len(juice_data)

    # ปรับให้เปอร์เซ็นต์ในตารางแสดงเป็นทศนิยม 2 ตำแหน่ง
    juice_data['percentage'] = juice_data['percentage'].round(2)

    # เรียงข้อมูลจากการกดมากไปหาน้อย
    juice_data = juice_data.sort_values(by='click_count', ascending=False)

    # แบ่งคอลัมน์ของ Streamlit
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # แสดงข้อมูลเป็นตาราง
        st.subheader("Juice Click Statistics")

        juice_data = juice_data.reset_index(drop=True)
        juice_data.index = juice_data.index + 1

        st.dataframe(juice_data)


    with col2:
        # สร้างกราฟแท่งที่แสดงการคลิก
        st.subheader("Juice Click Count")

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=juice_data, x='Juice', y='click_count', palette='Blues_d', ax=ax)
        ax.set_xlabel('Juice Type', fontsize=12)
        ax.set_ylabel('Click Count', fontsize=12)
        ax.set_title('Juice Click Statistics', fontsize=14)
        plt.xticks(rotation=45, ha="right")

        # ตั้งค่าให้แกน Y นับทีละ 1
        ax.set_yticks(range(0, int(juice_data['click_count'].max()) + 1, 1))

        st.pyplot(fig)

    with col3:
        # สร้างกราฟวงกลมแสดงเปอร์เซ็นต์การคลิก
        st.subheader("Juice Click Percentage")

        # กรองเฉพาะน้ำผลไม้ที่มีการคลิก > 0
        pie_data = juice_data[juice_data['click_count'] > 0]

        if not pie_data.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                pie_data['percentage'],
                labels=pie_data['Juice'],
                autopct='%1.2f%%',
                startangle=90,
                colors=sns.color_palette("Paired", len(pie_data))
            )
            ax.set_title('Juice Click Percentage', fontsize=14)
            st.pyplot(fig)
        else:
            st.info("ยังไม่มีน้ำผลไม้ที่ถูกคลิกเลย 😅")

# ใช้ sleep ก่อนรีเฟรช
st.write("Refreshing data... (will refresh every 10 seconds)")

# แสดงข้อมูลครั้งแรก
display_juice_data()

# หน่วงเวลา 10 วินาทีแล้วรีเฟรชใหม่
time.sleep(10)
st.rerun()
