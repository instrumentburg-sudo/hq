---
type: short
status: pending
project: apps/dashboard
priority: P1
created: 2026-04-22
---

# Сверить автоматическое обновление 18:00 на apps/dashboard

## Что сделать
Проверить, что cron в 18:00 Asia/Yekaterinburg отрабатывает без сбоев: `fetch_modulbank`, `gen_pnl`, рендер 7 вкладок (Метрика, Avito, Direct, LiveSklad, Модульбанк, Convex, сводная).

## Результат
Логи cron за последние 3 дня без ошибок. Дашборд `apps/dashboard` показывает актуальные цифры по всем 7 вкладкам. Дата последнего успешного запуска — сегодняшняя.

## Заметки
_(заполняется по ходу)_
