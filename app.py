import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# ---------- ตั้งค่า ----------
DATA_DIR = Path("data")
JSON_PATH = DATA_DIR / "latest.json"
IMG_PATH  = DATA_DIR / "latest.jpg"

st.set_page_config(page_title="Plant Monitoring Dashboard", layout="wide")

st.title("🌱 Plant Monitoring Dashboard")

# ---------- ตรวจว่ามีข้อมูลไหม ----------
if not JSON_PATH.exists():
    st.error("❌ ไม่พบไฟล์ latest.json")
    st.stop()

# ---------- โหลดข้อมูล ----------
with open(JSON_PATH, "r") as f:
    data = json.load(f)

timestamp = data.get("timestamp", "N/A")
pla = data.get("pla", "N/A")
growth = data.get("growth_rate", "N/A")

# ---------- แสดงค่า ----------
col1, col2, col3 = st.columns(3)

col1.metric("📐 PLA", f"{pla}")
col2.metric("📈 Growth Rate", f"{growth}")
col3.metric("⏱️ Timestamp", timestamp)

st.divider()

# ---------- แสดงรูป ----------
if IMG_PATH.exists():
    st.image(str(IMG_PATH), caption="Latest Annotated Image", use_container_width=True)
else:
    st.warning("⚠️ ไม่พบไฟล์ latest.jpg")
