# import streamlit as st
# import requests
# import time

# REFRESH_INTERVAL = 60
# API_URL = "https://jsonplaceholder.typicode.com/posts"

# st.set_page_config(page_title="Dashboard", layout="wide")
# st.title("📊 Real-time Data Dashboard")

# if "last_updated" not in st.session_state:
#     st.session_state.last_updated = time.time()

# # Fetch data
# def fetch_data():
#     try:
#         response = requests.get(API_URL)
#         return response.json()[:10]
#     except:
#         return []

# data = fetch_data()

# # Metrics
# col1, col2 = st.columns(2)
# with col1:
#     st.metric("Items Loaded", len(data))
# with col2:
#     st.metric("Refresh Interval", "60 sec")

# # Display data
# st.subheader("📄 Latest Data")
# for item in data:
#     st.write(f"**{item['title']}**")

# # Countdown
# remaining = REFRESH_INTERVAL - int(time.time() - st.session_state.last_updated)
# st.write(f"⏳ Next update in {remaining} sec")

# # Refresh logic
# if remaining <= 0:
#     st.session_state.last_updated = time.time()
#     st.rerun()

# # Manual refresh
# if st.button("🔄 Refresh Now"):
#     st.session_state.last_updated = 0
#     st.rerun()

# time.sleep(1)
# st.rerun()





import streamlit as st
import requests
import time

REFRESH_INTERVAL = 60
API_URL = "https://jsonplaceholder.typicode.com/posts"

st.set_page_config(page_title="Real-Time Dashboard", layout="wide")
st.title("📊 Real-time Data Dashboard")

if "last_updated" not in st.session_state:
    st.session_state.last_updated = time.time()

# Fetch data
@st.cache_data(ttl=60)
def fetch_data():
    response = requests.get(API_URL)
    return response.json()[:10]

data = fetch_data()

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Items Loaded", len(data))
with col2:
    st.metric("Refresh Interval", "60 sec")

# Display data
st.subheader("📄 Latest Data")
for item in data:
    st.write(f"• {item['title']}")

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