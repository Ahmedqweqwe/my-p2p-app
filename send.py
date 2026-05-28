import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 1. إعداد رابط الفيديو المستهدف
target_url = "ضع_رابط_فيديو_تيك_توك_هنا"

def extract_tiktok_keywords(url):
    print("[+] جاري تهيئة المتصفح وتخطي الحظر...")
    
    # إعدادات المتصفح لعدم الكشف أوتوماتيكياً وتخطي الحظر الأساسي
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # التشغيل في الخلفية بدون فتح نافذة
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1200x800")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # تشغيل متصفح كرووم
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5)  # وقت مستقطع لضمان تحميل أكواد الجافاسكربت والـ JSON الكاملة
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        keywords_data = {
            "Alt_Text": "غير متوفر",
            "Meta_Keywords": "غير متوفر",
            "SEO_Description": "غير متوفر",
            "Hidden_JSON_Tags": []
        }
        
        # أ. استخراج النص البديل (Alt Text) لغلاف الفيديو
        video_cover = soup.find('img', class_=lambda x: x and 'styles-ImgPoster' in x) or soup.find('img', alt=True)
        if video_cover and video_cover.get('alt'):
            keywords_data["Alt_Text"] = video_cover.get('alt')
            
        # ب. جلب الميتا الموجهة لمحركات البحث (SEO Metadata)
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords_data["Meta_Keywords"] = meta_keywords.get('content')
            
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            keywords_data["SEO_Description"] = meta_desc.get('content')

        # ج. تحليل ملف الـ JSON المخفي بالخلفية (SIGI_STATE أو Universal Share State)
        json_script = soup.find('script', id='SIGI_STATE') or soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
        if json_script:
            try:
                raw_json = json.loads(json_script.string)
                # محاولة البحث عن وسوم العناوين والهاشتاغات بشكل ديناميكي داخل الـ JSON
                if "ItemModule" in raw_json:
                    for item_id in raw_json["ItemModule"]:
                        video_info = raw_json["ItemModule"][item_id]
                        if "challenges" in video_info:
                            keywords_data["Hidden_JSON_Tags"] = [ch['title'] for ch in video_info['challenges']]
            except Exception:
                pass

        return keywords_data

    except Exception as e:
        print(f"[-] حدث خطأ أثناء الاستخراج: {e}")
        return None
    finally:
        driver.quit()

# تشغيل السكربت وحفظ النتائج
if __name__ == "__main__":
    if target_url == "ضع_رابط_فيديو_تيك_توك_هنا":
        print("[-] فضلاً قم بتعديل المتغير target_url ووضع رابط فيديو تيك توك حقيقي.")
    else:
        results = extract_tiktok_keywords(target_url)
        
        if results:
            print("[+] تم الاستخراج بنجاح! جاري حفظ البيانات...")
            with open("extracted_keywords.txt", "w", encoding="utf-8") as f:
                f.write(f"--- نتائج استخراج الكلمات المفتاحية المخفية ---\n\n")
                f.write(f"[1] النص البديل (Alt Text):\n {results['Alt_Text']}\n\n")
                f.write(f"[2] كلمات الميتا (Meta Keywords):\n {results['Meta_Keywords']}\n\n")
                f.write(f"[3] وصف السيو (SEO Description):\n {results['SEO_Description']}\n\n")
                f.write(f"[4] وسوم الـ JSON المخفية (Hashtags):\n {', '.join(results['Hidden_JSON_Tags']) if results['Hidden_JSON_Tags'] else 'لم يتم العثور على وسوم داخلية'}\n")
            print("[+] اكتمل الأمر. تم إنشاء ملف تلقائي باسم: extracted_keywords.txt")
