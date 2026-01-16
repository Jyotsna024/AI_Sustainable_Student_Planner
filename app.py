import streamlit as st
from ai_engine import analyze_schedule

st.set_page_config(page_title="AI Sustainable Student Planner",layout="wide")

st.markdown("""
<style>
.main {
background-color: #0f172a;
color: white;
}
h1, h2, h3 {
color: #38bdf8;
}
.card {
background-color: #020617;
padding: 20px;
border-radius: 16px;
margin-bottom: 20px;
}
</style>
""",unsafe_allow_html=True)

st.title("🌱 AI Sustainable Student Planner")
st.subheader("Plan smart. Study better. Live sustainably.")

with st.container():
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        classes=st.number_input("Daily class hours",0,12,5)
        study=st.number_input("Self-study hours",0,12,4)
        screen=st.number_input("Screen time (hours)",0,15,8)
    with col2:
        sleep=st.number_input("Sleep hours",0,12,6)
        travel=st.selectbox("Primary travel method",["Walking","Bicycle","Public Transport","Two-wheeler","Car"])
    st.markdown("</div>",unsafe_allow_html=True)

if st.button("Generate Sustainable Plan"):
    result=analyze_schedule(classes,study,screen,sleep,travel)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader("📊 Sustainability Analysis")
    st.write(result)
    st.markdown("</div>",unsafe_allow_html=True)
