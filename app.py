import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Plant Monitoring Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_DIR = Path("data")
LATEST_JSON = DATA_DIR / "latest.json"
LATEST_IMG  = DATA_DIR / "latest.jpg"
CSV_PATH    = DATA_DIR / "1st.csv"

st.title("🌱 Plant Monitoring Dashboard")

# ---------- โหลด latest.json ----------
latest = {}
if LATEST_JSON.exists():
    latest = json.loads(LATEST_JSON.read_text(encoding="utf-8"))

pla_latest = latest.get("pla", None)
growth_latest = latest.get("growth_rate", None)
ts_latest = latest.get("timestamp", "N/A")

# ---------- โหลด CSV สำหรับกราฟ ----------
df = None
if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH)
    df["dt"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["dt"]).sort_values("dt")
else:
    st.warning("ยังไม่พบ data/1st.csv (รอให้ Pi push มาก่อน)")

# ---------- ตัวกรองช่วงเวลา ----------
colf1, colf2 = st.columns([1, 3])
with colf1:
    window = st.selectbox("Show", ["7 days", "14 days", "30 days", "All"], index=3)

if df is not None and len(df) > 0 and window != "All":
    days = int(window.split()[0])
    cutoff = df["dt"].max() - pd.Timedelta(days=days)
    df_plot = df[df["dt"] >= cutoff].copy()
else:
    df_plot = df

# ---------- Status logic (ปรับ threshold ได้) ----------
status = "N/A"
if isinstance(growth_latest, (int, float)):
    # ตัวอย่าง: growth < 1.0 = Near Harvest (คุณปรับได้)
    status = "Near Harvest" if growth_latest < 1.0 else "Growing"

# ---------- Metrics แถวบน ----------


st.divider()


# ---------- รูปล่าสุด + ตัวเลขด้านขวา ----------
left, right = st.columns([1.2, 1])

with left:
    if LATEST_IMG.exists():
        st.image(
            str(LATEST_IMG),
            caption="Latest Annotated Image",
            use_container_width=True
        )
    else:
        st.info("No latest image yet")

with right:
    st.subheader("Latest Measurements")

    st.metric(
        label="PLA (mm²)",
        value=f"{pla_latest:.2f}" if isinstance(pla_latest, (int, float)) else str(pla_latest)
    )

    st.metric(
        label="Growth Rate (mm²/day)",
        value=f"{growth_latest:.2f}" if isinstance(growth_latest, (int, float)) else str(growth_latest)
    )

    st.metric(
        label="Timestamp",
        value=ts_latest
    )

    st.metric(
        label="Status",
        value=status
    )

st.divider()

# ---------- กราฟ ----------
if df_plot is not None and len(df_plot) > 1:
    st.subheader("Projected Leaf Area (PLA) vs Time")
    st.line_chart(df_plot.set_index("dt")["PLA_cm2"])

    st.subheader("Growth Rate (dA/dt)")
    st.bar_chart(df_plot.set_index("dt")["growth_rate"])
else:
    st.warning("ข้อมูลใน CSV ยังไม่พอสำหรับทำกราฟ")
