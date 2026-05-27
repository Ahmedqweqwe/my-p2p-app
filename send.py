import streamlit as st
import requests

st.set_page_config(page_title="Real TikTok Analyzer", page_icon="📈", layout="centered")

st.title("📈 Real TikTok Account Analyzer")
st.write("This version pulls live data from official servers.")

username = st.text_input("Enter TikTok Username (without @):")

if st.button("Fetch Live Data"):
    if username:
        username = username.strip().replace("@", "")
        
        with st.spinner("Connecting to live servers..."):
            url = "https://rapidapi.com"
            querystring = {"username": username}
            
            headers = {
                # 🛑 ضع الكود السري الذي نسخته من موقع RapidAPI بين القوسين بالأسفل بدلاً من هذه الكلمة
                "X-RapidAPI-Key": "PASTE_YOUR_RAPIDAPI_KEY_HERE",
                "X-RapidAPI-Host": "://rapidapi.com"
            }
            
            try:
                response = requests.get(url, headers=headers, params=querystring, timeout=10).json()
                
                if response.get("code") == 0 and "data" in response:
                    stats = response["data"]["stats"]
                    followers = stats.get("followerCount", 0)
                    heart_count = stats.get("heartCount", 0)
                    video_count = stats.get("videoCount", 0)
                    
                    st.success(f"Real data loaded for: @{username}")
                    st.divider()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Real Followers", value=f"{followers:,}")
                    with col2:
                        st.metric(label="Real Total Likes", value=f"{heart_count:,}")
                    with col3:
                        st.metric(label="Videos Count", value=f"{video_count:,}")
                else:
                    st.error("Account not found or API limits reached.")
            except Exception as e:
                st.error("Connection failed. Check your API key.")
    else:
        st.error("Please enter a username.")
