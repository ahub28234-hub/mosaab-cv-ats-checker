# 🔍 Mosaab CV - ATS Compatibility Checker

> **أداة فحص احترافية لتوافق السيرة الذاتية مع أنظمة متابعة المتقدمين (ATS)**

---

## 📋 ما هي هذه الأداة؟

أداة مفتوحة المصدر تفحص سيرتك الذاتية وتعطيك **تقريراً مفصلاً** عن مدى توافقها مع أنظمة ATS التي تستخدمها ٩٩٪ من الشركات الكبرى.

### لماذا تحتاجها؟
- ٧٥٪ من السير الذاتية تُرفض آلياً قبل أن تراها عين بشرية
- معظم "خدمات كتابة ATS" في السوق تعطي نتائج ضعيفة (< ٥٥٪)
- هذه الأداة تكشف الحقيقة بأرقام دقيقة

---

## ⚡ التثبيت

```bash
# 1. استنساخ المستودع
git clone <repo-url>
cd mosaab_cv_ats_checker

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. جربها!
python ats_checker.py your_cv.pdf
```

### المتطلبات
- Python 3.8+
- pdfplumber أو PyPDF2 (للـ PDF)
- python-docx (للـ DOCX)

---

## 🚀 الاستخدام

### الفحص الأساسي
```bash
python ats_checker.py my_cv.pdf
```

### فحص مع وصف وظيفي
```bash
python ats_checker.py my_cv.pdf --job "Software Engineer with Python and AWS experience"
```

### فحص مع ملف وصف وظيفي
```bash
python ats_checker.py my_cv.pdf --job-file job_description.txt
```

### توليد تقرير HTML
```bash
python ats_checker.py my_cv.pdf --output report.html
```

### توليد تقارير متعددة
```bash
python ats_checker.py my_cv.pdf --format all
```

---

## 📊 معايير التقييم

| المعيار | الوزن | الوصف |
|---------|-------|-------|
| 🔑 الكلمات المفتاحية | ٣٥٪ | توافق الكلمات مع الوصف الوظيفي |
| 📐 التنسيق والهيكل | ٢٥٪ | الأقسام، الجداول، الصور |
| 📖 سهولة القراءة | ٢٠٪ | طول الجمل، الأرقام، الأفعال |
| 📞 معلومات التواصل | ١٠٪ | بريد، هاتف، LinkedIn |
| 📏 الطول المناسب | ١٠٪ | عدد الكلمات والصفحات |

### مقياس التقدير

| التقدير | النطاق | المعنى |
|---------|--------|--------|
| **A** | ٨٥-١٠٠ | ممتاز - جاهز للتقديم! 🎯 |
| **B** | ٧٠-٨٤ | جيد - يحتاج لتحسينات بسيطة |
| **C** | ٥٥-٦٩ | مقبول - تحسينات ضرورية |
| **D** | ٤٠-٥٤ | ضعيف - إعادة بناء مطلوبة |
| **F** | ٠-٣٩ | فاشل - إعادة كتابة كاملة |

---

## 📁 هيكل المشروع

```
mosaab_cv_ats_checker/
├── ats_checker.py        # الملف الرئيسي (CLI)
├── ats_engine.py         # محرك التحليل
├── file_reader.py        # قارئ الملفات
├── report_generator.py   # مولد التقارير
├── requirements.txt      # المتطلبات
├── README.md            # هذا الملف
└── samples/             # نماذج تجريبية
    ├── sample_cv.txt
    └── sample_job.txt
```

---

## 🔧 للمطورين

### استخدام المحرك برمجياً

```python
from ats_engine import ATSEngine
from file_reader import CVFileReader

# قراءة السيرة الذاتية
reader = CVFileReader()
cv_text, metadata = reader.read("cv.pdf")

# التحليل
engine = ATSEngine()
result = engine.analyze(cv_text, job_description="Software Engineer...")

print(f"النتيجة: {result['overall_score']}/100")
print(f"التقدير: {result['grade']}")
```

### تخصيص القواعد

يمكنك تعديل قواعد الفحص في ملف `ats_engine.py`:

```python
# تعديل الأوزان
self.ats_rules['weights']['keywords'] = 40  # بدلاً من 35

# إضافة أقسام جديدة
self.section_keywords['publications'] = ['publications', 'papers', 'research']
```

---

## ⚠️ ملاحظات هامة

1. **ملفات PDF الممسوحة ضوئياً**: إذا كانت السيرة الذاتية صورة (scanned PDF)، لن تستطيع الأداة قراءتها. استخدم PDF مع نص قابل للنسخ.

2. **الجداول**: بعض أنظمة ATS لا تقرأ الجداول بشكل صحيح. الأداة تحذرك إذا وجدت جداول.

3. **الدقة**: النتيجة تقديرية بناءً على قواعد معروفة. أنظمة ATS مختلفة قد تعطي نتائج مختلفة قليلاً.

---

## 📞 التواصل

- **Instagram**: [@mosaab_cv](https://instagram.com/mosaab_cv)
- **LinkedIn**: [Mosaab CV](https://linkedin.com/company/mosaab-cv)
- **البريد**: info@mosaab-cv.com

---

## 📜 الترخيص

هذا المشروع مفتوح المصدر تحت ترخيص MIT.

---

<div align="center">

**صنع ب❤️ في الأردن 🇯🇴**

*Mosaab CV - نكتب مستقبلك المهني*

</div>
