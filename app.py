import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from datetime import datetime

from backend.ai_engine import generate_plan
from backend.models import StudentInput

st.set_page_config(
    page_title="AI Sustainable Student Planner",
    page_icon="🌱",
    layout="centered"
)

st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.stButton>button {border-radius: 12px; padding: 0.6rem 1.2rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🌱 AI Sustainable Student Planner")
st.caption("Personalized planning with sustainability & burnout intelligence")
st.divider()

sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
screen = st.slider("📱 Screen Time (hours)", 0, 12, 6)
study = st.slider("📚 Study Hours", 0, 12, 4)
travel = st.selectbox(
    "🚶 Mode of Travel",
    ["Walking", "Bicycle", "Public Transport", "Two-wheeler", "Car"]
)

HIST_PATH = Path("history.csv")

def save_history(payload):
    row = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "sleep": sleep,
        "screen": screen,
        "study": study,
        "travel": travel,
        "score": payload["score"],
        "level": payload["level"],
        "burnout": payload["burnout"],
        "confidence": payload["burnout_confidence"]
    }
    df = pd.DataFrame([row])
    if HIST_PATH.exists():
        df.to_csv(HIST_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(HIST_PATH, index=False)

if st.button("✨ Generate Plan"):
    data = StudentInput(
        sleep=sleep,
        screen=screen,
        study=study,
        travel=travel
    )

    result = generate_plan(data)
    save_history(result)

    st.subheader("📊 Sustainability Score")
    st.progress(result["score"] / 100)
    st.metric("Score", result["score"], result["level"])

    burnout_map = {0: "Low", 1: "Moderate", 2: "High"}
    st.subheader("🧠 Burnout Risk")
    st.metric(
        "Risk Level",
        burnout_map[result["burnout"]],
        f"{result['burnout_confidence']}% confidence"
    )
    st.caption("Key contributing factors: " + ", ".join(result["burnout_drivers"]))

    st.subheader("📈 Analytics")

    chart_df = pd.DataFrame({
        "Metric": ["Sleep", "Screen", "Study"],
        "Hours": [sleep, screen, study]
    })

    bar = alt.Chart(chart_df).mark_bar().encode(
        x="Metric",
        y="Hours",
        color="Metric"
    ).properties(height=220)

    st.altair_chart(bar, use_container_width=True)

    donut_df = pd.DataFrame({
        "Type": ["Score", "Remaining"],
        "Value": [result["score"], 100 - result["score"]]
    })

    donut = alt.Chart(donut_df).mark_arc(innerRadius=70).encode(
        theta="Value",
        color="Type"
    )

    st.altair_chart(donut, use_container_width=True)

    st.subheader("🗓️ Daily Planner")
    df = pd.DataFrame(
        result["plan"],
        columns=["Time", "Activity", "Note"]
    )
    st.table(df)

    if result["tips"]:
        st.subheader("💡 Suggestions")
        for tip in result["tips"]:
            st.success(tip)

if HIST_PATH.exists():
    st.divider()
    st.subheader("🕘 Recent History")
    hist = pd.read_csv(HIST_PATH)
    st.dataframe(hist.tail(10), use_container_width=True)
