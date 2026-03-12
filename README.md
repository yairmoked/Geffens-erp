# Geffens ERP - Supermarket Edition

מערכת ERP מלאה המותאמת לענף סופרמרקטים, חנויות נוחות וממתקים 24/7.

## מה כלול

- מודלי ERP מלאים: ליבה ארגונית, משתמשים והרשאות, מכירות, רכש, מלאי, כספים, משאבי אנוש וייצור.
- הרחבת רכש לסופרמרקט:
  - קטלוג ספק-מוצר (lead time, מינימום הזמנה, מארזים)
  - חוקי חידוש מלאי לפי Min/Max לכל מחסן ומוצר
  - הצעות חידוש מלאי אוטומטיות
- אינטגרציה לאתרי סחר חיצוניים ב-API
- מערכת ליקוט להזמנות מאתרי סחר
- תצוגות דפים עם התאמה לנייד + דף תצוגת פרויקט מלאה

## הפעלה מהירה (Codex Cloud / Local)

### אפשרות 1 - פקודה אחת

```bash
./scripts/setup_and_run.sh
```

הסקריפט מבצע:
1. התקנת תלויות
2. יצירת סכימת DB
3. הרצת בדיקות
4. העלאת שרת על `0.0.0.0:8000`

### אפשרות 2 - Makefile

```bash
make install
make init-db
make test
make run-cloud
```

## כתובות צפייה

- דף הבית: `http://127.0.0.1:8000/`
- תצוגת הפרויקט במלואו: `http://127.0.0.1:8000/project`
- מניפסט JSON של כל מרכיבי הפרויקט: `http://127.0.0.1:8000/api/project/manifest`
- health: `http://127.0.0.1:8000/health`

### צפייה מהמובייל

- התחברי לאותה רשת Wi‑Fi של המחשב
- פתחי `http://<IP-של-המחשב>:8000/`
- אפשר לקבל הנחיות גם מ-`GET /api/system/mobile-access`

## API שימושי

- `GET /health`
- `GET /api/system/mobile-access`
- `GET /api/project/manifest`
- `POST /api/replenishment/min-max`
- `GET /api/integrations/channels`
- `GET /api/picking/board`
