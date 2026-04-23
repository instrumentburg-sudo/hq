---
type: long
status: pending
project: apps/dashboard
priority: P2
created: 2026-04-23
---

# Yandex Webmaster — вкладка queries не наполняется

## Контекст
Три запуска pipeline подряд (21, 22, 23 апреля) в логе `/tmp/dashboard-daily.log`:
```
Pulling Webmaster positions...
Webmaster: no queries (API error?)
```
Блок Webmaster в дашборде пустой. SEO-поисковый слой не виден.

## Цель
Вкладка Webmaster показывает поисковые запросы и позиции. Скрипт, тянущий данные, отдаёт непустой результат в логе. Данные доходят до `data.js` → вкладка наполняется.

## План
- [ ] Найти скрипт, ответственный за Webmaster в `apps/dashboard` (вероятно в `update-data.sh` или отдельным `fetch_webmaster.py`)
- [ ] Проверить актуальность API endpoint Яндекс.Вебмастера (версия API, пути)
- [ ] Проверить OAuth токен Webmaster, обновить при необходимости
- [ ] Проверить, не изменилась ли схема ответа (host_id, поле query, поле position)
- [ ] Прогнать скрипт ручной выгрузки — убедиться, что парсер работает
- [ ] Дождаться следующего 18:00, сверить

## Делегирование
Автономно.

## Заметки
P2 — не деньги, но слепая зона по SEO, которая вредит задаче `website-seo-perforators`: без данных Webmaster не видно, что именно проседает.

## Ссылки
- Лог: `/tmp/dashboard-daily.log`
- Pipeline: `/home/iamsohappy/projects/instrumentburg/apps/dashboard/update-data.sh`
- Смежная задача: `website-seo-perforators`
- Родительская задача: `tasks/done/2026-04-22-dashboard-cron-check.md`
