---
title: HQ redesign — directions + practices
date: 2026-04-23
status: approved
---

# HQ redesign — directions + practices

## Контекст

Текущий `hq/index.html` (editorial dark, 287 строк, 3 блока задач) не даёт пользователю нужной «наглядности». Урок 2 Personal Corp («Масштабирование без оверинженеринга», «Два штаба», «Правила на двух этажах») предлагает естественное решение — разбить хаб на направления. У пользователя 3 глобальных направления бизнеса (+ личное) и 30 проектов.

## Архитектура

**Структура:**
```
hq/ (публичный, GitHub Pages)
  index.html            — главный HQ: карта 4 направлений + live-задачи + applied practices
  service/index.html    — подробный под-хаб (следующая итерация)
  marketplaces/...      — placeholder
  tenders/...           — placeholder
  course/lesson1.html, lesson2.html
  practices/*.md        — source of truth для «Applied practices»

hq-personal/            — ОТДЕЛЬНЫЙ штаб, локально, без GitHub Pages
  AGENTS.md с Human Gate наверху
```

## Решения (принятые через brainstorming)

1. **Блок «Applied practices» (C)** — отдельная секция на главном HQ. Показывает, что из курса реально приземлилось в работу. Не дублирует lesson-страницы.
2. **Источник практик (D)** — `hq/practices/*.md`, frontmatter `status | lesson | title`. Ручной куратор. `skipped` не рендерится, но остаётся в md как «осознанный отказ».
3. **Визуальный vibe (B)** — Modern SaaS dashboard dark. Референсы: linear.app, vercel dashboard.
4. **Цвет (B)** — 4 muted-акцента по направлениям, статусы без цвета (через иконки):
   - `--service` #d97706 · `--marketplaces` #65a30d · `--tenders` #0284c7 · `--personal` #9333ea
5. **Layout (C)** — двухколоночный desktop (40/60): направления слева, live-задачи справа. Applied practices — широкая полоса снизу. На mobile: стэк direction → tasks → practices.
6. **Карточка направления (B)** — название + цветная полоса 3px + счётчик `N проектов · M активных задач` + 1-строчный status line (priority из highest-priority задачи этого направления).
7. **Personal** — показывается на публичном HQ с битой ссылкой (напоминание, что штаб существует). Клик ведёт `file://.../hq-personal/`.
8. **Рендер задачи (B)** — двухстрочно: `[status-icon] title` + мета-строка `direction · due · priority`. Токен направления цветом, остальное dim.

## Typography

- Display/body — **Geist** (sans)
- Mono — **JetBrains Mono** (метаданные, due, priority, lesson-tag, счётчики)

## Color tokens

```
--bg: #0a0a0a
--bg-elevated: #141414
--border: #262626
--text: #e5e5e5
--text-dim: #737373
--text-faint: #404040

--service: #d97706
--marketplaces: #65a30d
--tenders: #0284c7
--personal: #9333ea
```

## Маппинг направлений → проекты (из AGENTS.md §6.1)

- **service** — ядро (3) + операции (9, кроме Tenders) + база знаний (2) + клиенты (3) = **17 проектов**
- **marketplaces** — 0 проектов (placeholder, база знаний в планах)
- **tenders** — Blagoystroystvo + Tenders = **2 проекта**
- **personal** — personal-corp + health-tracker = **2 проекта** (публичное представление; agent-second-brain формально в платформенных, фактически — личный второй мозг)
- **infra (скрыто)** — 6 платформенных: hq, claude-skills, openclaw-hub, srv-kvm, telethon, agent-second-brain. Доступны через AGENTS.md и footer.

## Mobile (<768px)

Stack: header → 4 карточки направлений (full width) → live-задачи → applied practices. Цветная полоса 3px остаётся. Navigation в header прячется в footer. Шрифты на step меньше.

## Rendering

На этой итерации — статический HTML, вручную с живыми данными из `tasks/*.md` + `practices/*.md` + `AGENTS.md §6.1`. Скрипт автоматической сборки — позже, отдельной задачей (из практики урока 2 «надзиратель-агент по расписанию»).

## Out of scope этой итерации

- Под-хаб `service/index.html` — следующая итерация
- Placeholders `marketplaces/` и `tenders/` — следующая итерация
- `hq-personal/` каркас — отдельная задача
- Скрипт автосборки `index.html` из источников — отдельная задача
- Метрики/KPI в карточках направлений — когда появятся реальные числа (урок 2: не строить систему для нерешённой задачи)
