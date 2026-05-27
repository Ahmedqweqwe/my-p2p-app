import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="AI Image Generator PRO", page_icon="🎨", layout="centered")

st.title("🎨 مولد الصور الذكي بالذكاء الاصطناعي")
st.write("اكتب وصف الصورة باللغة العربية أو الإنجليزية، وسيقوم الذكاء الاصطناعي برسمها فوراً!")

# حقل إدخال الوصف النصي
prompt = st.text_input("اكتب وصف الصورة هنا:", placeholder="مثال: كلب رائد فضاء على القمر")

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("اختر نمط الصورة والتصميم:", ["Realistic (واقعي)", "Anime (أنمي)", "Cyberpunk (سايبر بانك)", "3D Render (ثلاثي الأبعاد)"])
with col2:
    aspect_ratio = st.selectbox("اختر أبعاد الصورة (المقاس):", ["1:1 (مربع)", "16:9 (عرض الشاشات)", "9:16 (طولي للموبايل)"])

if st.button("توليد ورسم الصورة الآن 🚀"):
    if prompt:
        with st.spinner("⏳ جاري ترجمة الوصف ومعالجة الصورة بالسيرفر الذكي..."):
            
            # --- نظام ترجمة فوري ذكي وسريع مدمج داخل الكود ---
            translated_prompt = prompt
            try:
                # استخدام مترجم مجاني مدمج لتحويل النص للإنجليزية تلقائياً لتفادي مشاكل السيرفر
                trans_url = f"https://googleapis.com{urllib.parse.quote(prompt)}"
                trans_resp = requests.get(trans_url, timeout=5).json()
                if trans_resp and trans_resp[0]:
                    translated_prompt = trans_resp[0][0][0]
            except Exception:
                pass # إذا فشلت الترجمة يستمر بالوصف الأصلي
                
            # دمج النمط والأبعاد مع الوصف المترجم لجودة فائقة
            full_prompt = f"{translated_prompt}, {style}, highly detailed, 4k resolution"
            encoded_prompt = urllib.parse.quote(full_prompt)
            
            width, height = 1024, 1024
            if aspect_ratio == "16:9 (عرض الشاشات)":
                width, height = 1280, 720
            elif aspect_ratio == "9:16 (طولي للموبايل)":
                width, height = 720, 1280
                
            image_url = f"https://pollinations.ai{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            # حزمة الحماية لإقناع السيرفر بالاتصال الآمن دائماً بدون حظر
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            try:
                # سحب داتا الصورة مع زيادة مهلة الاستجابة لـ 30 ثانية كاملة
                response = requests.get(image_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    st.success("✨ تم رسم وتوليد صورتك بنجاح!")
                    st.divider()
                    
                    st.image(response.content, caption=f"الترجمة التلقائية للوصف: {translated_prompt}", use_container_width=True)
                    
                    st.download_button(
                        label="📥 تحميل الصورة بجودة عالية",
                        data=response.content,
                        file_name="ai_image.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("❌ السيرفر مشغول حالياً بمعالجة صور أخرى، يرجى المحاولة مرة أخرى الآن.")
            except Exception:
                st.error("⚠️ خطأ في معالجة الشبكة. يرجى الضغط على الزر مرة ثانية لإعادة إرسال طلب الرسم.")
    else:
        st.error("من فضلك اكتب وصفاً أولاً!")
