import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Plant #1 Details", layout="wide")
st.title("Plant #1 Details")

CSV_PATH = Path("data/1st.csv")
LATEST_IMG = Path("data/latest.jpg")

if not CSV_PATH.exists():
    st.error("ไม่พบไฟล์ data/1st.csv (รอให้ Pi push มาก่อน)")
    st.stop()

df = pd.read_csv(CSV_PATH)

# รวม date+time เป็น datetime (ไฟล์คุณเป็น day/month/year)
df["dt"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["dt"]).sort_values("dt")

# ค่า current จากแถวล่าสุด
last = df.iloc[-1]
pla = float(last["PLA_cm2"])
growth = float(last["growth_rate"])

# status logic (ปรับ threshold ได้)
status = "Near Harvest" if growth < 1.0 else "Growing"

col1, col2 = st.columns([1, 2])
with col1:
    if LATEST_IMG.exists():
        st.image(str(LATEST_IMG), use_container_width=True, caption="Latest Annotated Image")
    else:
        st.warning("ไม่พบ data/latest.jpg")

with col2:
    st.subheader(f"Status: {status}")
    st.metric("Current PLA (cm²)", f"{pla:.2f}")
    st.metric("Current Growth Rate (cm²/day)", f"{growth:.2f}")

st.divider()

st.subheader("Projected Leaf Area (PLA) vs Time")
st.line_chart(df.set_index("dt")["PLA_cm2"])

st.subheader("Growth Rate (dA/dt)")
st.bar_chart(df.set_index("dt")["growth_rate"])
