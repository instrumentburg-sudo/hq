---
type: long
status: completed
project: apps/avito-responder
priority: P1
created: 2026-04-22
completed: 2026-05-11
---

# Миграция apps/avito-responder в единый responder

## Контекст
apps/avito-responder — Python-бот на Anthropic API, systemd-сервис на OpenClaw VPS. Работал отдельно. Теперь становится адаптером «авито» внутри `instrumentburg-responder`.

## Цель
Логика и knowledge_base `apps/avito-responder` перенесены в адаптер «авито» единого responder'а. systemd-сервис отключён. Функциональность сохранена, качество ответов не просело.

## План
- [x] Вынести systemd-юнит в архив
- [x] Портировать knowledge_base в общую (см. responder-unification)
- [x] Адаптер «авито» в instrumentburg-responder принимает те же webhook-события
- [x] Стресс-тест: 50 реальных сообщений, сверка качества

2026-05-11 — закрыто по подтверждению Антона в Telegram: «Это все сделано уже». Задача убрана из активной ежедневной сводки HQ.

**Блокер:** ждём готовности единого `instrumentburg-responder` (`tasks/long/responder-unification.md`). Без него миграция не стартует.

## Ссылки
- `/home/iamsohappy/projects/instrumentburg/apps/avito-responder`
- `tasks/long/responder-unification.md`
