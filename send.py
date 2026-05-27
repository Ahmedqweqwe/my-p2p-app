import streamlit as st
import time

# إعدادات الصفحة والعنوان
st.set_page_config(page_title="منصة تداول P2P الذكية", page_icon="💰", layout="wide")

st.title("💰 نموذج محاكاة منصة تداول P2P الذكية")
st.write("هذه المنصة تحاكي نظام الضمان التلقائي (Escrow System) لمعاملات شخص لشخص بدون تدخل بشري إلا في النزاعات.")

# استخدام st.session_state لحفظ حالة المعاملة أثناء ضغط الأزرار
if 'step' not in st.session_state:
    st.session_state.step = 'setup'
if 'amount' not in st.session_state:
    st.session_state.amount = 0.0
if 'wallet' not in st.session_state:
    st.session_state.wallet = ""

# تقسيم الشاشة إلى جزأين: لوحة العميل ولوحة المراقبة الخلفية
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🛒 نافذة تنفيذ المعاملة")
    
    # الخطوة الأولى: إعداد طلب الشراء
    if st.session_state.step == 'setup':
        st.subheader("إنشاء طلب شراء عملة رقمية (USDT)")
        wallet_input = st.text_input("أدخل عنوان محفظة المشتري الرقمية:")
        amount_input = st.number_input("أدخل كمية USDT المطلوبة للطلب:", min_value=10.0, step=5.0)
        
        if st.button("بدء عملية الشراء وحجز العملات"):
            if wallet_input:
                st.session_state.wallet = wallet_input
                st.session_state.amount = amount_input
                st.session_state.step = 'escrow_locked'
                st.rerun()
            else:
                st.error("الرجاء إدخال عنوان محفظتك الرقمية أولاً!")

    # الخطوة الثانية: حجز العملات في نظام الضمان (Escrow) وبدء مهلة الدفع
    elif st.session_state.step == 'escrow_locked':
        st.info("🔒 نظام الضمان (Escrow): تم سحب العملات من حساب البائع وحجزها مؤقتاً في السيرفر بنجاح.")
        st.success(f"الكمية المحجوزة: **{st.session_state.amount} USDT** لصالح المحفظة (`{st.session_state.wallet}`)")
        
        st.warning("⚠️ يرجى تحويل المبلغ المالي للبائع عبر (فودافون كاش أو الحساب البنكي) خارج المنصة ثم الضغط على تأكيد الدفع.")
        
        # أزرار التحكم للمشتري
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ لقد قمت بتحويل الأموال (تأكيد الدفع)"):
                st.session_state.step = 'waiting_seller'
                st.rerun()
        with col_btn2:
            if st.button("❌ إلغاء المعاملة وفك حجز العملات"):
                st.session_state.step = 'setup'
                st.rerun()

    # الخطوة الثالثة: انتظار تأكيد البائع
    elif st.session_state.step == 'waiting_seller':
        st.warning("⏳ في انتظار قيام البائع بفتح حسابه البنكي والتأكد من استلام الأموال النقدية...")
        
        col_seller1, col_seller2 = st.columns(2)
        with col_seller1:
            if st.button("🟢 (صوت البائع): نعم استلمت الكاش، حرر العملات للمشتري"):
                st.session_state.step = 'completed'
                st.rerun()
        with col_seller2:
            if st.button("🚨 فتح نزاع (لم أستلم الأموال أو هناك مشكلة)"):
                st.session_state.step = 'dispute'
                st.rerun()

    # الخطوة الرابعة: اكتمال المعاملة تلقائياً
    elif st.session_state.step == 'completed':
        st.balloons()
        st.success(f"🎉 تمت المعاملة بنجاح وتلقائياً بالكامل! تم تحرير **{st.session_state.amount} USDT** إلى المحفظة `{st.session_state.wallet}`.")
        if st.button("🔄 بدء معاملة جديدة"):
            st.session_state.step = 'setup'
            st.rerun()

    # الخطوة الخامسة: حالة النزاع والتدخل البشري من الإدارة
    elif st.session_state.step == 'dispute':
        st.error("🚨 تم تجميد المعاملة وتحويلها إلى لوحة تحكم الإدارة (النزاعات).")
        st.write("النظام التلقائي توقف هنا. يقوم المشرفون الآن بفحص إيصالات التحويل وكشف الحساب يدوياً.")
        
        st.subheader("🛠️ قرارات الإدارة (صلاحياتك كمشرف على الموقع):")
        col_admin1, col_admin2 = st.columns(2)
        with col_admin1:
            if st.button("⚖️ تحرير العملات للمشتري (التحويل صحيح)"):
                st.session_state.step = 'completed'
                st.rerun()
        with col_admin2:
            if st.button("⚖️ إعادة العملات للبائع (المشتري لم يحول أموال)"):
                st.error("تم إلغاء الطلب وإرجاع الرصيد للبائع.")
                if st.button("العودة للرئيسية"):
                    st.session_state.step = 'setup'
                    st.rerun()

with col2:
    st.header("📊 حالة السيرفر الخلفي")
    st.write("هنا ترى ما يحدث داخل قاعدة بيانات السيرفر في نفس اللحظة:")
    
    # عرض حالة المعاملة الحالية داخل السيرفر للتحقق
    status_mapping = {
        'setup': '💤 في انتظار بدء معاملة',
        'escrow_locked': '🔒 العملات محجوزة في الضمان مؤقتاً',
        'waiting_seller': '⏳ العميل دفع، بانتظار تأكيد البائع',
        'completed': '✅ معاملة منتهية وناجحة',
        'dispute': '🚨 نزاع قائم يتطلب تدخل الإدارة'
    }
    
    st.metric(label="حالة المعاملة الحالية:", value=status_mapping[st.session_state.step])
    st.metric(label="القيمة الرقمية الحالية بالضمان:", value=f"{st.session_state.amount} USDT")
