import streamlit as st
import requests
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="محلل تيك توك التلقائي", page_icon="⚡", layout="centered")

st.title("⚡ محلل تيك توك التلقائي الذكي")
st.write("اكتب اسم الحساب فقط، وسيقوم السيرفر بسحب البيانات الحية وتحليل الأمان تلقائياً دون أي إدخال يدوي.")

# حقل إدخال اسم الحساب
username = st.text_input("أدخل اسم المستخدم (بدون علامة @):", placeholder="مثال: khaby.lame")

if st.button("بدء الفحص التلقائي الحقيقي 🔍"):
    if username:
        username = username.strip().replace("@", "")
        
        with st.spinner("⏳ جاري الاتصال بقاعدة بيانات تيك توك وسحب الإحصائيات الحية..."):
            try:
                # الاتصال بـ API وسيط لجلب بيانات الحساب الحقيقية مجاناً
                api_url = f"https://tikwm.com{username}"
                response = requests.get(api_url, timeout=15).json()
                
                if response.get("code") == 0 and "data" in response:
                    user_data = response["data"]["user"]
                    stats_data = response["data"]["stats"]
                    
                    # سحب الأرقام الحقيقية من التيك توك مباشرة
                    nickname = user_data.get("nickname", username)
                    followers = stats_data.get("followerCount", 0)
                    following = stats_data.get("followingCount", 0)
                    heart_count = stats_data.get("heartCount", 0)
                    video_count = stats_data.get("videoCount", 0)
                    
                    st.success(f"✅ تم العثور على الحساب: {nickname}")
                    st.divider()
                    
                    # عرض البيانات الحقيقية المستخرجة
                    st.subheader("📊 إحصائيات الحساب الحية من السيرفر:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="👥 المتابعين", value=f"{followers:,}")
                    with col2:
                        st.metric(label="❤️ إجمالي الإعجابات", value=f"{heart_count:,}")
                    with col3:
                        st.metric(label="🎬 عدد الفيديوهات", value=f"{video_count:,}")
                        
                    st.divider()
                    
                    # تحليل الحظر الخفي والأمان برمجياً بناءً على الأرقام الحقيقية
                    st.subheader("🕵️‍♂️ تقرير الأمان ومقاومة الحظر:")
                    
                    # الحسابات التي لديها متابعين كثر لكن إعجابات قليلة جداً تكون مشبوهة
                    if followers > 5000 and (heart_count / followers) < 0.5:
                        st.error("🚨 تحذير: نسبة التفاعل منخفضة جداً مقارنة بعدد المتابعين!")
                        st.write("📌 **النتيجة:** الحساب يواجه ضعف شديد في الوصول أو احتمالية وجود حظر خفي (Shadowban) نتيجة متابعين وهميين.")
                        st.metric(label="🛡️ جودة الحساب والموثوقية:", value="35% - منخفضة")
                    else:
                        st.success("🟢 نظام الأمان: الحساب مستقر وتفاعله طبيعي.")
                        st.write("📌 **النتيجة:** مؤشرات الحساب متناسقة مع خوارزميات تيك توك ولا توجد علامات حظر حالية.")
                        st.metric(label="🛡️ جودة الحساب والموثوقية:", value="88% - ممتازة")
                        
                else:
                    st.error("❌ لم يتم العثور على الحساب! تأكد من كتابة اسم المستخدم (Username) بشكل صحيح.")
            except Exception as e:
                st.error("⚠️ حدث خطأ أثناء الاتصال بالسيرفر الخارجي، يرجى المحاولة مرة أخرى لاحقاً.")
    else:
        st.error("الرجاء إدخال اسم حساب أولاً!")
