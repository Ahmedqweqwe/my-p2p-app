import time
import random
from playwright.sync_api import sync_playwright

# قائمة بالتعليقات المختلفة لمنع التكرار والحظر
comments_pool = [
    "منور يا غالي ✨",
    "بالتوفيق إن شاء الله 👍",
    "محتوى رائع جداً 💎",
    "تحياتي لك من مصر 🇪🇬",
    "استمر يا بطل 🚀"
]

def run_bot():
    with sync_playwright() as p:
        # فتح متصفح يحاكي جهاز حقيقي
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # الانتقال إلى رابط البث المباشر المستهدف
        page.goto("https://tiktok.com")
        
        # (هنا يتم وضع كود تسجيل الدخول لحسابك يدوياً أو تلقائياً أول مرة)
        print("الرجاء التأكد من تسجيل الدخول داخل البث...")
        time.sleep(10) 
        
        # حلقة تكرارية لإرسال تعليقات مختلفة بمواقيت عشوائية
        for i in range(10):
            # اختيار تعليق عشوائي من القائمة
            current_comment = random.choice(comments_pool)
            
            # تحديد مربع كتابة التعليق في تيك توك وضغط تفاعل
            page.fill('input[placeholder="أضف تعليقاً..."]', current_comment)
            page.press('input[placeholder="أضف تعليقاً..."]', "Enter")
            
            print(f"تم إرسال: {current_comment}")
            
            # فاصل زمني عشوائي (مثلاً بين 5 إلى 15 ثانية) حتى لا يكشفك الروبوت
            time.sleep(random.randint(5, 15))

        browser.close()

# تشغيل السكربت
# run_bot()
