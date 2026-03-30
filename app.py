import streamlit as st
import requests
import time

REFRESH_INTERVAL = 60

st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("📊 Real-time Weather Dashboard (India)")

# Predefined cities (India)
cities = {
    "Kolkata": (22.57, 88.36),
    "Delhi": (28.61, 77.20),
    "Mumbai": (19.07, 72.87),
    "Bangalore": (12.97, 77.59),
    "Chennai": (13.08, 80.27)
}

# Select city
selected_city = st.selectbox("📍 Select City", list(cities.keys()))
lat, lon = cities[selected_city]

if "last_updated" not in st.session_state:
    st.session_state.last_updated = time.time()

# Fetch weather
@st.cache_data(ttl=60)
def fetch_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    return response.json()

data = fetch_data(lat, lon)
weather = data["current_weather"]

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡️ Temperature (°C)", weather["temperature"])

with col2:
    st.metric("💨 Wind Speed (km/h)", weather["windspeed"])

with col3:
    st.metric("🧭 Wind Direction", weather["winddirection"])

st.subheader(f"🕒 Last Updated ({selected_city})")
st.write(weather["time"])

# Countdown
elapsed = int(time.time() - st.session_state.last_updated)
remaining = REFRESH_INTERVAL - elapsed
st.markdown(f"⏳ **Next update in {remaining} seconds**")

# Refresh logic
if remaining <= 0 or st.button("🔄 Refresh Now"):
    st.session_state.last_updated = time.time()
    st.cache_data.clear()
    st.rerun()

time.sleep(1)
st.rerun()