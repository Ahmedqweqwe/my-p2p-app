import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="centered")

st.title("🎨 مولد الصور الذكي بالذكاء الاصطناعي")
st.write("اكتب الوصف باللغة الإنجليزية في الأسفل، وسيقوم الذكاء الاصطناعي برسم الصورة لك مجاناً فوراً.")

# حقل إدخال الوصف النصي للصورة
prompt = st.text_input("اكتب وصف الصورة (يفضل بالإنجليزية):", placeholder="مثال: a futuristic flying car in a cyberpunk city")

# خيارات إضافية لتحسين جودة وتصميم الصورة
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("اختر نمط الصورة والتصميم:", ["Realistic (واقعي)", "Anime (أنمي)", "Cyberpunk (سايبر بانك)", "3D Render (ثلاثي الأبعاد)", "Oil Painting (لوحة زيتية)"])
with col2:
    aspect_ratio = st.selectbox("اختر أبعاد الصورة (المقاس):", ["1:1 (مربع)", "16:9 (عريض للشاشات)", "9:16 (طولي للموبايل)"])

if st.button("توليد ورسم الصورة الآن 🚀"):
    if prompt:
        with st.spinner("⏳ جاري إرسال الوصف لسيرفرات الذكاء الاصطناعي ومعالجة الصورة..."):
            
            # دمج النمط المختار مع الوصف النصي لضمان جودة عالية
            full_prompt = f"{prompt}, {style}, highly detailed, 4k resolution"
            
            # تحويل النص ليكون متوافقاً مع روابط الإنترنت (URL Encoding)
            encoded_prompt = urllib.parse.quote(full_prompt)
            
            # تحديد الأبعاد البرمجية للصورة بناءً على اختيار المستخدم
            width, height = 1024, 1024
            if aspect_ratio == "16:9 (عريض للشاشات)":
                width, height = 1280, 720
            elif aspect_ratio == "9:16 (طولي للموبايل)":
                width, height = 720, 1280
                
            # رابط الـ API المجاني المباشر لتوليد الصور
            image_url = f"https://pollinations.ai{encoded_prompt}?width={width}&height={height}&seed={random_seed := time_time := int(100)}&nologo=true"
            
            try:
                # التحقق من أن السيرفر استجاب وجاهز لعرض الصورة
                response = requests.get(image_url, timeout=15)
                
                if response.status_code == 200:
                    st.success("✨ تم توليد ورسم الصورة بنجاح!")
                    st.divider()
                    
                    # عرض الصورة الناتجة في الموقع للمستخدم
                    st.image(image_url, caption=f"الوصف المعالج: {prompt}", use_container_width=True)
                    
                    # توفير زر لتحميل الصورة مباشرة على جهاز المستخدم
                    st.download_button(
                        label="📥 تحميل الصورة بجودة عالية",
                        data=response.content,
                        file_name="ai_generated_image.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("❌ السيرفر مشغول حالياً، يرجى إعادة المحاولة بعد ثوانٍ قليلة.")
            except Exception as e:
                st.error("⚠️ فشل الاتصال بسيرفر التوليد، تحقق من جودة الإنترنت لديك.")
    else:
        st.error("من فضلك اكتب وصفاً للصورة أولاً لكي يستطيع الذكاء الاصطناعي رسمها!")
