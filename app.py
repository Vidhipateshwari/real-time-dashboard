import streamlit as st
import requests
import time

REFRESH_INTERVAL = 60

st.set_page_config(page_title="Real-Time Dashboard", layout="wide")
st.title("📊 Real-time Weather Dashboard")

if "last_updated" not in st.session_state:
    st.session_state.last_updated = time.time()

# Fetch real-time weather
@st.cache_data(ttl=60)
def fetch_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=22.57&longitude=88.36&current_weather=true"
    response = requests.get(url)
    return response.json()

data = fetch_data()
weather = data["current_weather"]

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡️ Temperature (°C)", weather["temperature"])

with col2:
    st.metric("💨 Wind Speed (km/h)", weather["windspeed"])

with col3:
    st.metric("🧭 Wind Direction", weather["winddirection"])

# Time
st.subheader("🕒 Last Updated")
st.write(weather["time"])

# Countdown
elapsed = int(time.time() - st.session_state.last_updated)
remaining = REFRESH_INTERVAL - elapsed

st.markdown(f"⏳ **Next update in {remaining} seconds**")

# Auto refresh
if remaining <= 0:
    st.session_state.last_updated = time.time()
    st.cache_data.clear()
    st.rerun()

# Manual refresh
if st.button("🔄 Refresh Now"):
    st.session_state.last_updated = time.time()
    st.cache_data.clear()
    st.rerun()

time.sleep(1)
st.rerun()