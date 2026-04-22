---
type: long
status: blocked
project: instrumentburg-responder
priority: P1
created: 2026-04-22
---

# Единый responder — merge канальных адаптеров

## Контекст
Было несколько раздельных ответчиков: `apps/avito-responder`, `apps/max-miniapp` и др. Архитектурное решение — единый агент-ответчик `instrumentburg-responder`: ядро + канальные адаптеры (Авито, MAX, Telegram, сайт). Общий knowledge_base.

## Цель
`instrumentburg-responder` получает сообщения из всех 4 каналов через адаптеры, отвечает единой логикой. Старые responder'ы переведены в архив или удалены.

## План
- [ ] Архитектура канальных адаптеров (интерфейс, форматы)
- [ ] Миграция knowledge_base в общую (MD + JSON)
- [ ] Адаптер Авито (на базе apps/avito-responder)
- [ ] Адаптер MAX (из apps/max-miniapp)
- [ ] Адаптер Telegram
- [ ] Адаптер сайта (чат-виджет)
- [ ] Протестировать каждый канал на stage
- [ ] Деплой на OpenClaw VPS, финальное переключение с rollback-планом

## Заметки
**Блокер:** канальные адаптеры зеркалят сообщения — если деплой сломает цепочку, клиенты перестанут получать ответы. Условие разблокировки — готовый stage с прогоном всех 4 каналов и rollback-план.

## Ссылки
- `/home/iamsohappy/projects/instrumentburg-responder`
- `/home/iamsohappy/projects/instrumentburg/apps/avito-responder`
- `/home/iamsohappy/projects/instrumentburg/apps/max-miniapp`
