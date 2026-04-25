---
type: long
status: in_progress
project: instrumentburg
priority: P2
created: 2026-04-25
deadline: 2026-05-09
---

# Миграция видимых Telegram-ботов в скрытые исполнители

## Контекст
2026-04-25 в OpenClaw зафиксирована новая архитектура: топик = контекст работы, агент = роль/способность. Видимый Telegram-бот нужен только там, где есть отдельная аудитория, права или внешний рабочий процесс. Сейчас пять ролей (`marketer`, `advertiser`, `sitebuilder`, `chaser`, `mailer`) имеют видимого бота без обоснования — это вынуждает Антона быть «шиной» между ботами и плодит несколько голосов в одном чате.

Источники решения:
- `~/.openclaw/workspace-topic-system/ORCHESTRATION.md`
- `~/.openclaw/workspace-topic-system/COMMUNICATION_PROTOCOL.md`
- `~/.openclaw/workspace-topic-system/TELEGRAM_BOT_MIGRATION.md`
- `hq/AGENTS.md` §11 — OpenClaw агенты

## Цель
Пять ролей-кандидатов (`marketer`, `advertiser`, `sitebuilder`, `chaser`, `mailer`) перестают принимать входящие групповые триггеры в Telegram и работают как внутренние исполнители, которых вызывает `topic-system` или профильный topic-агент через `sessions_spawn` / `sessions_send`. Workspace, skills, tools и исходящий cron сохраняются.

Критерий готовности: 1–2 дня наблюдения без потери задач из старых групп; в `TELEGRAM_BOT_MIGRATION.md` зафиксирован финальный режим каждого из пяти ботов.

## План
- [ ] Шаг 1 — Антон подтверждает по каждому из 5 ботов: оставлять видимым, отключать, отложить
- [ ] Шаг 2 — Бэкап `openclaw.json` (`groupPolicy`, `groupAllowFrom`, allowlists)
- [ ] Шаг 3 — Отключить групповые триггеры для подтверждённых ролей (обратимая правка конфигурации)
- [ ] Шаг 4 — `openclaw config validate`, рестарт gateway
- [ ] Шаг 5 — Проверить вызовы исполнителей через `sessions_spawn` от `topic-system` и topic-агентов
- [ ] Шаг 6 — 1–2 дня наблюдения: не теряются ли задачи из старых групп; cron `mailer` исходящий не сломан
- [ ] Шаг 7 — Финальная фиксация в `TELEGRAM_BOT_MIGRATION.md` и в OpenClaw `STATE.md`

## Делегирование
- Шаги 1, 6 — ручное решение Антона (Human Gate на отключение видимого интерфейса)
- Шаги 2–5 — `topic-system` в `~/.openclaw/workspace-topic-system/`
- Шаг 7 — `topic-system` обновляет MIGRATION.md и OpenClaw STATE.md

## Заметки
Не трогать в рамках задачи:
- `master`, `dispatcher`, `nutritionist` — остаются видимыми
- Главный вход `@ClawdIamsohappy_bot` — остаётся
- Токены и аккаунты у BotFather — не удалять
- Исходящий cron `mailer` — не отключать

Откат: вернуть `groupPolicy: allowlist` и `groupAllowFrom` из бэкапа, рестарт gateway.

Связанная инфра:
- `groupAllowFrom fix` (11.03.2026): если `groupPolicy: "allowlist"` без `groupAllowFrom`, групповые сообщения дропаются без ошибки.
- workspaces исполнителей: `workspace-marketer`, `workspace-advertiser`, `workspace-sitebuilder`, `workspace-chaser`, `workspace-mailer` — сохраняются как есть.

## Ссылки
- `~/.openclaw/workspace-topic-system/ORCHESTRATION.md`
- `~/.openclaw/workspace-topic-system/COMMUNICATION_PROTOCOL.md`
- `~/.openclaw/workspace-topic-system/TELEGRAM_BOT_MIGRATION.md`
- `~/.openclaw/workspace/STATE.md`
- `hq/AGENTS.md` §11
