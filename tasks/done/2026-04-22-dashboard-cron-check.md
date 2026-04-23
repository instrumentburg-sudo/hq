---
type: short
status: completed
project: apps/dashboard
priority: P1
created: 2026-04-22
completed: 2026-04-23
---

# Сверить автоматическое обновление 18:00 на apps/dashboard

## Что сделать
Проверить, что cron в 18:00 Asia/Yekaterinburg отрабатывает без сбоев: `fetch_modulbank`, `gen_pnl`, рендер 7 вкладок.

## Результат
**Cron по расписанию работает:**
- crontab: `0 13 * * * /home/iamsohappy/projects/instrumentburg/apps/dashboard/run-daily-pipeline.sh` (13:00 UTC = 18:00 EKB)
- Лог: `/tmp/dashboard-daily.log`, 3 запуска (21, 22, 23 апреля)
- Сегодняшний запуск: 13:03:06 → 13:03:55 (≈50 сек), до `✓ done`
- Артефакты: Vercel-деплой (`dashboard-three-blond-70.vercel.app`), `ib-digest/dashboard-news/2026-04-23.html`, Telegram msg id 18494

**НО 2 стабильных бага — вынесены в отдельные задачи:**
- `livesklad-cogs-token-refresh` (П1) — сегодня `HTTP 401 → token refresh failed → empty`, COGS за 2026-04 (102 заказа) не обновились. Это деньги в P&L.
- `webmaster-api-queries-fix` (П2) — `Webmaster: no queries (API error?)` три запуска подряд. Вкладка Webmaster пуста.

Пайплайн не падает (`set -euo pipefail`, ошибки в stdout, не в exit code), поэтому cron считается «успешным», но часть данных теряется.

## Заметки
Сверка 2026-04-23. Дальше — чинить два бага по отдельности, по приоритету.
