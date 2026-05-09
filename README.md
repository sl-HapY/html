
# 🚀 git-get


---

## 🎯 معرفی

**git-get** یک ابزار رایگان و قدرتمند است که به شما امکان دانلود و جستجوی محتوای دیجیتال را از طریق GitHub Actions فراهم می‌کند. این ابزار خصوصاً برای کاربران ایرانی که با محدودیت‌های اینترنتی مواجه هستند، طراحی شده است.

### ✨ چرا git-get؟

- 🌐 **دسترسی بدون فیلتر**: از سرورهای GitHub استفاده می‌کند
- 🔒 **ایمن و مطمئن**: تمام عملیات روی سرورهای رسمی انجام می‌شود
- 💾 **ذخیره‌سازی ابری**: فایل‌ها در مخزن GitHub شما نگهداری می‌شوند
- 🚀 **رایگان**: بدون هیچ‌گونه هزینه
- 🛡️ **پایدار**: مقاوم در برابر تغییرات شبکه

---

## 🔥 ویژگی‌ها

### 📥 دانلود محتوا
- ✅ **دانلود از یوتوب**: ویدیو و صدا با کیفیت‌های مختلف (144p تا 4K)
- ✅ **دانلود پلی‌لیست**: دانلود کامل پلی‌لیست‌های یوتوب
- ✅ **دانلود مستقیم**: از هر لینک مستقیم (فایل‌های PDF، تصاویر، نرم‌افزار و...)
- ✅ **دانلود یوتوب موزیک**: استخراج MP3 با کیفیت بالا

### 🔍 جستجوی پیشرفته
- ✅ **جستجو در یوتوب**: یافتن ۵۰ نتیجه برتر
- ✅ **جستجوی یوتوب موزیک**: جستجو در محتوای موزیکال یوتوب
- ✅ **نتایج منظم**: ارائه نتایج در قالب جدول منظم

### 🛠️ ابزارهای مدیریتی  
- ✅ **پاکسازی انتخابی**: حذف دسته‌بندی شده فایل‌ها
- ✅ **لینک‌های مستقیم**: دسترسی آسان به فایل‌های دانلود شده

---

## 📋 پیش‌نیازها

1. **حساب GitHub**: [github.com](https://github.com) (رایگان)
2. **مرورگر وب**: کروم، فایرفاکس یا هر مرورگر مدرن
3. **اتصال اینترنت**: برای دسترسی به GitHub

> ⚠️ **توجه**: نیازی به نصب نرم‌افزار اضافی ندارید!

---

## 🚀 نصب و راه‌اندازی

### مرحله ۱:
1.فورک کردن این پروژه


---

## 📖 نحوه استفاده

### ▶️ راه‌اندازی
1. به تب **Actions** در مخزن خود بروید
2. **git-get** را از فهرست انتخاب کنید
3. **Run workflow** را کلیک کنید

### ⚙️ تنظیمات

#### 📁 روش دانلود (Download Method)
- **youtube_download**: دانلود ویدیو یوتوب
- **youtube_playlist**: دانلود پلی‌لیست کامل
- **direct_download**: دانلود مستقیم فایل
- **youtube_search**: جستجو در یوتوب
- **youtube_music_search**: جستجوی موزیک

#### 🎬 کیفیت ویدیو (فقط یوتوب)
- **best**: بهترین کیفیت موجود
- **2160**: 4K (۲۱۶۰p)
- **1440**: 2K (۱۴۴۰p)  
- **1080**: Full HD (۱۰۸۰p)
- **720**: HD (۷۲۰p)
- **480**: SD (۴۸۰p)
- **audio**: فقط صدا (MP3)

#### 🔗 ورودی (Input Text)
- **برای دانلود**: لینک یوتوب یا لینک مستقیم
- **برای جستجو**: کلمات کلیدی

---

## ⚠️ محدودیت‌ها

### 🕒 زمانی
- **حداکثر زمان اجرا**: ۳ ساعت
- **تعداد اجرای همزمان**: ۲۰ عملیات
- **تعداد دفعات ماهانه**: ۲۰۰۰ دقیقه (رایگان)

### 📊 حجمی  
- **حداکثر حجم فایل**: ۲ گیگابایت
- **حداکثر حجم مخزن**: ۱۰۰ گیگابایت
- **حداکثر فایل در commit**: ۱۰۰ عدد

### 🚫 محدودیت‌های محتوا
- فایل‌های دارای حق‌نشر محدود
- محتوای نامناسب یا غیرقانونی
- فایل‌های آلوده به ویروس

### 💾 ذخیره‌سازی
- فایل‌ها در مخزن عمومی قابل دسترس هستند

---

## 💡 مثال‌های کاربردی

### مثال ۱: دانلود ویدیو یوتوب
```
روش: youtube_download
کیفیت: 1080
ورودی: https://www.youtube.com/watch?v=VIDEO_ID
```

### مثال ۲: دانلود موزیک
```
روش: youtube_download  
کیفیت: audio
ورودی: https://www.youtube.com/watch?v=MUSIC_ID
```

### مثال ۳: دانلود پلی‌لیست
```
روش: youtube_playlist
کیفیت: 720
ورودی: https://www.youtube.com/playlist?list=PLAYLIST_ID
```

### مثال ۴: دانلود مستقیم
```
روش: direct_download
ورودی: https://example.com/file.pdf https://example.com/image.jpg
```

### مثال ۵: جستجو
```
روش: youtube_search
ورودی: آموزش برنامه‌نویسی
```

### مثال ۶: جستجوی موزیک
```
روش: youtube_music_search  
ورودی: احسان خواجه‌امیری
```

---

## 🔧 عیب‌یابی

### ❌ خطاهای رایج

#### خطا: "Workflow failed"
**علت**: مشکل در اتصال یا تنظیمات
**راه‌حل**: 
- چند دقیقه صبر کنید و دوباره امتحان کنید
- لینک را بررسی کنید

#### خطا: "Download failed"  
**علت**: فایل در دسترس نیست یا محدود است
**راه‌حل**:
- لینک را بررسی کنید  
- از VPN استفاده کنید

#### خطا: "File too large"
**علت**: فایل بزرگتر از ۲ گیگابایت است  
**راه‌حل**:
- کیفیت پایین‌تری انتخاب کنید
- فایل را تقسیم کنید

### 🐛 گزارش مشکل
اگر با مشکلی مواجه شدید:
1. فایل لاگ را بررسی کنید
2. از تب **Issues** در GitHub استفاده کنید  
3. اطلاعات کامل مشکل را ارسال کنید

---

## ❓ سؤالات متداول

### ❓ آیا استفاده از git-get قانونی است؟
✅ بله، git-get فقط یک ابزار است. مسئولیت استفاده قانونی با شماست.

### ❓ آیا فایل‌هایم امن هستند؟
✅ فایل‌ها روی سرورهای GitHub نگهداری می‌شوند که امنیت بالایی دارند.

### ❓ آیا می‌توانم فایل‌های خصوصی دانلود کنم؟
✅ از مخزن Private استفاده کنید تا فایل‌ها خصوصی باشند.

### ❓ چطور فایل‌هایم را پاک کنم؟
✅ از ابزار **git-get Cleanup** استفاده کنید.

### ❓ آیا محدودیت سرعت دارد؟
✅ سرعت به اتصال اینترنت شما و سرورهای GitHub بستگی دارد.

### ❓ آیا از VPN پشتیبانی می‌کند؟
✅ git-get از پروکسی داخلی استفاده می‌کند و نیازی به VPN ندارید.

### ❓ چطور چندین فایل همزمان دانلود کنم؟
✅ لینک‌ها را با اسپیس از هم جدا کنید.

### ❓ آیا از تمام سایت‌ها پشتیبانی می‌کند؟
✅ بیشتر سایت‌ها پشتیبانی می‌شوند، اما برخی ممکن است محدودیت داشته باشند.


---

MIT License

Copyright (c) 2024 hapy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

```
