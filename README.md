
<div dir="rtl" align="right">

**دانلودر همه‌کاره‌ای که می‌تواند در محیط گیتهاب اکشنز اجرا شود و فایل‌های نهایی را به صورت یک فایل ZIP تحویل دهد.**

این ابزار برای شرایطی طراحی شده که دسترسی مستقیم به بسیاری از سایت‌ها وجود ندارد و تنها راه ارتباطی از طریق گیتهاب است.  
با تعریف یک یا چند وظیفه (Task) در قالب یک JSON، می‌توانید:

- فایل‌ها را مستقیماً از لینک HTTP/HTTPS دانلود کنید
- مخازن گیت (از جمله Hugging Face) را کلون کنید (حتی با LFS)
- یک وبسایت را به صورت کامل آینه‌سازی (Mirror) کنید

---
## 📦 پیش‌نیازها

فایل گردش کار گیتهاب از پیش‌نیازهای لازم در رانر اوبونتو مراقبت می‌کند.

| ابزار/کتابخانه       | نصب روی رانر           |
|---------------------|----------------------|
| Python 3.11+        | `actions/setup-python` |
| `requests`          | `pip install requests` |
| `beautifulsoup4`    | `pip install beautifulsoup4` |
| `lxml`              | `pip install lxml` |
| `git`               | از پیش نصب شده        |
| `git-lfs`           | از پیش نصب شده        |

در صورت اجرای محلی باید همین کتابخانه‌ها را روی سیستم خود داشته باشید.

---

## ✨ ویژگی‌ها

- **چند وظیفه همزمان** – چندین دانلود از انواع مختلف را در یک اجرا مدیریت می‌کند.
- **دانلود مستقیم** – فایل‌های ساده، دیتاست‌ها، تصاویر و هر چیزی که لینک مستقیم دارد.
- **کلون کامل Git** – مخصوصاً برای مخازن Hugging Face با پشتیبانی از فایل‌های بزرگ (LFS).
- **آینه‌ساز وبسایت** – سایت‌های استاتیک را به صورت کامل و با اصلاح لینک‌های داخلی دانلود می‌کند.
- **خروجی ZIP** – تمام فایل‌های دانلودشده را در یک فایل ZIP جمع‌بندی می‌کند و به عنوان Artifact گیتهاب تحویل می‌دهد.
- **لاگ دقیق** – هر مرحله با زمان ثبت می‌شود تا پیشرفت کار مشخص باشد.

---

## 🛠 شیوه استفاده

### ۱. راه‌اندازی گردش کار (Workflow)

فایل `.github/workflows/download.yml` را با محتوای زیر در مخزن خود بسازید:

```yaml
name: Multi Downloader
on: workflow_dispatch   # دستی اجرا می‌شود
jobs:
  download:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests beautifulsoup4 lxml
      - name: Run downloader
        env:
          TASKS_JSON: |
            [
              // اینجا وظایف خود را تعریف کنید
            ]
        run: python downloader.py
      - uses: actions/upload-artifact@v4
        with:
          name: downloaded-files
          path: final_download.zip
