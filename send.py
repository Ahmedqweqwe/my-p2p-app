from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import re

# إعداد متصفح كروم بشكل مخفي (Headless) لسرعة الأداء
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# رابط فيديو التيك توك المراد فحصه
video_url = "https://www.tiktok.com/@username/video/1234567890123456789"

try:
    driver.get(video_url)
    
    # 1. محاولة استخراج النص البديل (Alt Text) مباشرة من عنصر الفيديو أو الصورة المصغرة
    try:
        video_element = driver.find_element(By.TAG_NAME, "img") # تيك توك يضع بوستر الفيديو كصورة تحتوي على alt
        alt_text = video_element.get_attribute("alt")
        print(f"[+] النص البديل المخفي (Alt Text): {alt_text}\n")
    except Exception:
        print("[-] لم يتم العثور على نص بديل مباشر.")

    # 2. استخراج البيانات البرمجية المخفية (Metadata) من كود الصفحة
    page_source = driver.page_source
    
    # البحث عن كتل البيانات المخفية (JSON) داخل الكود
    # تيك توك يغير المسميات باستمرار، ولكن الفكرة واحدة وهي البحث عن الـ Scripts التي تحتوي على بيانات الفيديو
    json_data = re.search(r'<script id="__UNIVERSAL_DATA_FOR_NEXT_DEV__" type="application/json">(.*?)</script>', page_source)
    
    if json_data:
        data = json.loads(json_data.group(1))
        
        # هنا نقوم بالدخول تفصيلياً داخل الـ JSON لاستخراج الكلمات المفتاحية (تختلف التقسيمة حسب تحديثات تيك توك)
        print("[+] تم العثور على ملف البيانات المخفي! يمكنك فحص الكلمات المفتاحية منه:")
        # مثال لطباعة الكلمات الدلالية أو الوسوم المرتبطة بالفيديو في الخلفية
        # print(json.dumps(data, indent=4, ensure_ascii=False)) 
    else:
        print("[-] لم يتم العثور على كتلة البيانات البرمجية المباشرة (قد تحتاج لتحديث الـ Regex).")

finally:
    driver.quit()