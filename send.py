import streamlit as st

# عنوان المنصة
st.title("📱 تطبيق التجربة الخاص بي")
st.write("مرحباً بك! هذا السكربت يعمل الآن بنجاح على سيرفر Streamlit.")

# حقل إدخال بيانات تجريبي
user_data = st.text_input("جرّب كتابة أي شيء هنا:")

# زر تفاعلي
if st.button("اضغط للتأكيد"):
    if user_data:
        st.success(f"✅ تم استقبال النص بنجاح: {user_data}")
    else:
        st.warning("⚠️ من فضلك اكتب نصاً في الحقل أولاً.")
