# Geffens ERP - Supermarket Edition

מערכת ERP מלאה המותאמת לענף סופרמרקטים, חנויות נוחות וממתקים 24/7.

## מה כלול

- מודלי ERP מלאים: ליבה ארגונית, משתמשים והרשאות, מכירות, רכש, מלאי, כספים, משאבי אנוש וייצור.
- הרחבת רכש לסופרמרקט:
  - קטלוג ספק-מוצר (lead time, מינימום הזמנה, מארזים)
  - חוקי חידוש מלאי לפי Min/Max לכל מחסן ומוצר
  - הצעות חידוש מלאי אוטומטיות
- אינטגרציה לאתרי סחר חיצוניים ב-API:
  - הגדרת ערוצי סחר
  - קליטת הזמנות חיצוניות ושורות הזמנה
- מערכת ליקוט להזמנות מאתרי סחר:
  - אצוות ליקוט
  - משימות ליקוט ושורות ליקוט
- תצוגות דפים (UI בסיסי ב-FastAPI + Jinja) עם התאמה לנייד

## הרצה מהירה

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## צפייה בדפדפן / מובייל

- מחשב מקומי: `http://127.0.0.1:8000/`
- מובייל (אותה רשת Wi‑Fi): `http://<IP-של-המחשב>:8000/`
- בדיקת תקינות: `http://127.0.0.1:8000/health`

## API שימושי

- `GET /api/system/mobile-access`
- `POST /api/replenishment/min-max`
- `GET /api/integrations/channels`
- `GET /api/picking/board`
