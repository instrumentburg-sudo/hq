---
type: long
status: pending
project: apps/dashboard
priority: P1
created: 2026-04-23
---

# LiveSklad COGS — починить refresh токена, остановить пустые запросы

## Контекст
В `run-daily-pipeline.sh` 2026-04-23 (18:03 EKB, лог `/tmp/dashboard-daily.log`):
```
HTTP 401 on A023676 — refreshing token (1/3), waiting 5s
  token refresh failed — falling back to cache
Rate-limited mid-fetch, no cache — writing empty
```
Итог: COGS за 2026-04 (102 заказа) **не обновились**. P&L в `data.js` потерял себестоимость за апрель — это деньги в дашборде.

## Цель
Pipeline 18:00 успешно тянет COGS из LiveSklad detail API для всех заказов текущего месяца, без пустого fallback. Три запуска подряд без `HTTP 401` + `token refresh failed`.

## План
- [ ] Прочитать `fetch_cogs.py`: где refresh-логика, какие токены, откуда читаются
- [ ] Понять, почему `refresh failed`: истёк refresh token / неверный endpoint / rate-limit на сам refresh
- [ ] Проверить кеш токена (файл или переменная окружения), посмотреть срок жизни
- [ ] При необходимости — восстановить credentials вручную через панель LiveSklad
- [ ] Добавить backoff между batch-запросами, если корень — rate-limit на detail
- [ ] Прогнать `fetch_cogs.py` локально, убедиться что 102 заказа за 2026-04 попадают в кеш
- [ ] Дождаться следующего 18:00, сверить, что в логе нет 401 и refresh failed

## Делегирование
Автономно. Исследовательская работа в `apps/dashboard/`, production cron трогать только после ручной проверки.

## Заметки
Попутно: в `fetch_cogs.py:56` `datetime.utcnow()` помечен как deprecated — исправить заодно на `datetime.now(datetime.UTC)`, если буду трогать файл.
Токен LiveSklad хранится по Shop ID `5c615f26149eb4750c36b897` (из BOOT.md).

## Ссылки
- Лог: `/tmp/dashboard-daily.log`
- Скрипт: `/home/iamsohappy/projects/instrumentburg/apps/dashboard/fetch_cogs.py`
- Pipeline: `run-daily-pipeline.sh`
- Родительская задача: `tasks/done/2026-04-22-dashboard-cron-check.md`
