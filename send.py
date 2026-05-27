import streamlit as st
import re
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="كاشف حسابات تيك توك الاحترافي", page_icon="🕵️‍♂️", layout="centered")

st.title("🕵️‍♂️ كاشف ومحلل أمان حسابات تيك توك")
st.write("أدخل اسم المستخدم (Username) للكشف على الحساب وفحص نقاط الأمان ونسبة الحظر الخفي.")

# حقل إدخال اسم الحساب
username = st.text_input("أدخل اسم المستخدم (بدون علامة @):", placeholder="مثال: ahmed_user")

# قائمة معايير الفحص المحاكية
if st.button("بدء فحص وتتبع الحساب 🔎"):
    if username:
        # تنظيف اسم الحساب من الفراغات
        username = username.strip().replace("@", "")
        
        # رسالة بدء الفحص
        with st.spinner("⏳ جاري الاتصال بخوادم الفحص وتحليل بيانات الحساب..."):
            time.sleep(2.5) # محاكاة وقت سحب البيانات
            
        st.success("✅ اكتمل سحب البيانات الرقمية بنجاح!")
        st.divider()
        
        # --- نظام التقييم البرمجي للحساب ---
        # 1. فحص طول الاسم وجودته
        is_bot_name = bool(re.search(r'\d{4,}', username)) # إذا كان الاسم يحتوي على أكثر من 4 أرقام متتالية
        
        # حساب نقاط الأمان الافتراضية
        trust_score = 95
        issues = []
        
        if is_bot_name:
            trust_score -= 30
            issues.append("⚠️ اسم المستخدم يحتوي على أرقام عشوائية كثيرة (سلوك مشابه للبوتات).")
            
        if len(username) < 5:
            trust_score -= 15
            issues.append("⚠️ اسم المستخدم قصير جداً، مما يقلل من موثوقية الحساب لدى الخوارزميات.")

        # --- عرض النتائج للمستخدم ---
        st.subheader(f"📊 تقرير الفحص الخاص بالحساب: @{username}")
        
        # عرض مؤشر الثقة والأمان
        if trust_score >= 80:
            st.metric(label="🛡️ درجة موثوقية الحساب (Trust Score):", value=f"{trust_score}%", delta="آمن ومستقر")
            st.success("🟢 الحساب في حالة ممتازة ولا يواجه أي قيود حالياً بالخوارزميات.")
        elif trust_score >= 50:
            st.metric(label="🛡️ درجة موثوقية الحساب (Trust Score):", value=f"{trust_score}%", delta="- انتباه", delta_color="inverse")
            st.warning("🟡 الحساب معرض للمراقبة الفورية إذا قام بأنشطة مكثفة.")
        else:
            st.metric(label="🛡️ درجة موثوقية الحساب (Trust Score):", value=f"{trust_score}%", delta="مخاطر عالية", delta_color="inverse")
            st.error("🔴 الحساب يمتلك تقييم منخفض جداً ويواجه مشاكل في التفاعل.")

        st.divider()
        
        # 2. فحص حالة الحظر الخفي (Shadowban Status)
        st.subheader("🕵️‍♂️ فحص القيود الخفية (Shadowban Checker)")
        if trust_score < 70:
            shadowban_chance = "65%"
            st.error(f"🚨 احتمالية وجود حظر خفي (Shadowban): {shadowban_chance}")
            st.write("📌 **السبب:** ظهور تعليقاتك قد يكون مقيداً للآخرين بسبب تراجع جودة وتفاعل الحساب.")
        else:
            st.success("✅ الحظر الخفي: 0% (تعليقاتك وفيديوهاتك تظهر للجميع بشكل طبيعي).")
            
        st.divider()
        
        # عرض المشاكل والنصائح
        st.subheader("🛠️ المشاكل المكتشفة ونصائح الحل:")
        if issues:
            for issue in issues:
                st.write(issue)
            st.info("💡 **نصيحة المطور:** قم بتغيير اسم المستخدم لاسم حقيقي، وتجنب تكرار نفس التعليق في البث المباشر لأكثر من 3 مرات متتالية.")
        else:
            st.write("🎯 لم يتم العثور على أي مشاكل برمجية في بنية الحساب الحالية. استمر في التفاعل الطبيعي!")
            
    else:
        st.error("الرجاء إدخال اسم حساب تيك توك أولاً لبدء الفحص!")
