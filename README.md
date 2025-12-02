# QA Automation Project (Python)

مشروع أوتوميشن لاختبارات QA مكتوب بلغة Python. يستخدم `pytest` لتشغيل الاختبارات وPlaywright لتشغيل اختبارات المتصفح الوظيفية.

الملف يحتوي على أمثلة تشغيل سريعة وتشغيل CI.

## المتطلبات
- Python 3.9+
- Git (اختياري)

## إعداد محلي سريع

1. أنشئ بيئة افتراضية:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. ثبّت الاعتمادات:

```bash
pip install -r requirements.txt
```

3. (لاختبارات Playwright) ثبّت المتصفحات المطلوبة:

```bash
python -m playwright install
```

4. شغّل الاختبارات:

```bash
pytest -q
```

5. لتوليد تقرير HTML سريعًا:

```bash
pytest --html=report.html -q
# التقرير: report.html
```

6. لتجميع نتائج Allure (مخرجات Allure تُخزّن في `allure-results`):

```bash
pytest --alluredir=allure-results -q
# لإنشاء تقرير Allure محليًا تحتاج لأداة Allure CLI:
# https://docs.qameta.io/allure/
# مثال لتوليد التقرير إن كان مثبتًا:
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## ملاحظات
- أضفت `tests/test_example_playwright.py` كمثال على اختبار متصفح باستخدام Playwright.
- لتركيب Playwright والمتصفحات في بيئة CI تأكد من تشغيل `playwright install` أو استخدم action رسمي في GitHub Actions.
