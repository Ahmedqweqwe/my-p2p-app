import os
import threading
import tkinter as tk
from ftplib import FTP
from tkinter import filedialog, messagebox, simpledialog

# إعدادات الاتصال بهاتفك
PHONE_IP = "192.168.1.9"
PHONE_PORT = 2221
USER = "android"
PASSWORD = "android"
# قم بتغيير هذه السطور في كودك الحالي بالمفكرة:
USER = "android"                
PASSWORD = "android"
# دالة إرسال ملف من الكمبيوتر إلى الهاتف
def send_file_logic():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    def run_send():
        try:
            status_label.config(text="جاري الاتصال بالهاتف...", fg="blue")
            btn_send.config(state=tk.DISABLED)
            
            ftp = FTP()
            ftp.connect(PHONE_IP, PHONE_PORT, timeout=15)
            ftp.login(USER, PASSWORD)
            ftp.encoding = 'utf-8'
            
            file_name = os.path.basename(file_path)
            status_label.config(text="جاري ارسال الملف...", fg="orange")
            
            with open(file_path, 'rb') as file:
                ftp.storbinary(f'STOR {file_name}', file)
                
            ftp.quit()
            status_label.config(text="تم النقل بنجاح", fg="green")
            messagebox.showinfo("نجاح العملية", f"تم إرسال الملف بنجاح:\n{file_name}")
        except Exception as e:
            status_label.config(text="فشل الاتصال!", fg="red")
            messagebox.showerror("خطأ في النقل", f"تأكد من تشغيل الـ FTP بالهاتف\nالخطأ: {e}")
        finally:
            btn_send.config(state=tk.NORMAL)

    threading.Thread(target=run_send, daemon=True).start()

# دالة سحب ملف من الهاتف إلى الكمبيوتر
def receive_file_logic():
    def run_receive():
        try:
            status_label.config(text="جاري الاتصال بالهاتف...", fg="blue")
            btn_recv.config(state=tk.DISABLED)
            
            ftp = FTP()
            ftp.connect(PHONE_IP, PHONE_PORT, timeout=15)
            ftp.login(USER, PASSWORD)
            ftp.encoding = 'utf-8'
            
            file_name = simpledialog.askstring("استقبال ملف", "اكتب اسم الملف الموجود في الهاتف بدقة:")
            
            if file_name:
                status_label.config(text="جاري سحب الملف...", fg="orange")
                save_path = os.path.join(os.path.dirname(__file__), "from_phone_" + file_name)
                
                with open(save_path, 'wb') as file:
                    ftp.retrbinary(f'RETR {file_name}', file.write)
                    
                status_label.config(text="تم الاستلام بنجاح", fg="green")
                messagebox.showinfo("نجاح العملية", f"تم حفظ الملف بجانب الكود باسم:\nfrom_phone_{file_name}")
            else:
                status_label.config(text="تم إلغاء العملية", fg="gray")
                
            ftp.quit()
        except Exception as e:
            status_label.config(text="فشل الاستقبال!", fg="red")
            messagebox.showerror("خطأ", f"لم نجد الملف أو فشل الاتصال:\n{e}")
        finally:
            btn_recv.config(state=tk.NORMAL)

    threading.Thread(target=run_receive, daemon=True).start()

# بناء واجهة البرنامج الرسومية (تم حذف الإيموجي لتجنب خطأ التكل)
root = tk.Tk()
root.title("برنامج نقل الملفات بدون نت")
root.geometry("450x280")

title_label = tk.Label(root, text="تبادل الملفات (كمبيوتر - هاتف)", font=("Arial", 14, "bold"))
title_label.pack(pady=15)

btn_send = tk.Button(root, text="ارسال ملف إلى الهاتف", font=("Arial", 11), bg="#2196F3", fg="white", width=28, command=send_file_logic)
btn_send.pack(pady=10)

btn_recv = tk.Button(root, text="سحب ملف من الهاتف", font=("Arial", 11), bg="#4CAF50", fg="white", width=28, command=receive_file_logic)
btn_recv.pack(pady=10)

status_label = tk.Label(root, text="الحالة: جاهز للعمل", font=("Arial", 10), fg="gray")
status_label.pack(pady=20)

root.mainloop()
