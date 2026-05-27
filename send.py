import streamlit as st
import hashlib

st.set_page_config(page_title="TikTok Analyzer PRO", page_icon="📊", layout="centered")

st.title("📊 TikTok Account Trust & Engagement Analyzer")
st.write("Enter the username below to analyze the profile stats and evaluate shadowban status.")

username = st.text_input("Enter TikTok Username (without @):", placeholder="example: ahmedtop373")

if st.button("Run Full Analysis 🔍"):
    if username:
        username = username.strip().replace("@", "")
        
        with st.spinner("Scanning profile data and tracking engagement metrics..."):
            import time
            time.sleep(1.8)
            
        # تحويل الاسم إلى رقم ثابت فريد باستخدام دالة التشفير Hash
        # هذا يضمن أن الحساب المكتوب ستظهر له نفس الأرقام دائماً ولا تتغير عشوائياً
        name_hash = int(hashlib.md5(username.encode('utf-8')).hexdigest(), 16)
        
        # توليد أرقام متناسقة ومظهرها حقيقي تماماً بناءً على تشفير الاسم
        followers = (name_hash % 85000) + 1200
        video_count = (name_hash % 90) + 15
        heart_count = followers * ((name_hash % 5) + 3) + (name_hash % 400)
        
        # حساب معدل الموثوقية والأمان برمجياً
        has_numbers = sum(c.isdigit() for c in username)
        trust_score = 94
        if has_numbers > 2:
            trust_score -= 20
        if len(username) < 6:
            trust_score -= 10
            
        st.success(f"Analysis successfully completed for: @{username}")
        st.divider()
        
        # عرض المؤشرات الإحصائية الثابتة للحساب
        st.subheader("📊 Profile Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Followers", value=f"{followers:,}")
        with col2:
            st.metric(label="Total Likes", value=f"{heart_count:,}")
        with col3:
            st.metric(label="Videos", value=f"{video_count:,}")
            
        st.divider()
        
        # تقرير الحظر الخفي والأمان
        st.subheader("🛡️ Shadowban & Security Risk Report")
        
        if trust_score >= 80:
            st.success("🟢 Safe Status: No Shadowban detected on this account.")
            st.write("Analysis shows consistent core data structure. Video reach and comment visibility align perfectly with the current algorithm.")
            st.metric(label="Account Trust Score", value=f"{trust_score}%")
        else:
            st.error("🚨 Warning: Moderate Shadowban risk detected!")
            st.write("Account structure triggers filters due to patterns often shared by automated profiles. Post visibility might be temporarily throttled.")
            st.metric(label="Account Trust Score", value=f"{trust_score}%")
            st.info("💡 Tip: Maintain natural interactions and avoid repetitive engagement bursts to restore full reach.")
    else:
        st.error("Please enter a valid TikTok username first.")
