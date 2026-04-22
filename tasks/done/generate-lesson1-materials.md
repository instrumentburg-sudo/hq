---
type: long
status: completed
project: personal-corp
priority: P2
created: 2026-04-22
completed: 2026-04-22
---

# Сгенерировать учебные материалы из транскрипта 1-го урока

## Контекст
Домашка Серёжи Риса из 1-го урока Personal Corp: «на основе транскрипта, который лежит в папке курса, сделай HTML по первому уроку. Извлеки оттуда термины, методы, фреймворки, цели и домашние задания. И сделай дэшбот курса».

До задачи транскрипт лежал прямо в `personal corp/lesson1.txt`; отдельного выжимка не существовало.

## Цель
`personal corp/lesson1.html` — одностраничный dark-editorial выжимок 1-го урока с разделами: термины, методы, фреймворки, цели, ДЗ, цитаты. Публичная копия — `hq/course/lesson1.html` (через GitHub Pages).

## План
- [x] Перенести `lesson1.txt` → `personal corp/transcripts/lesson1.txt`
- [x] Извлечь структуру урока в `personal corp/lesson1.json` (субагент)
- [x] Сгенерировать `personal corp/lesson1.html` (dark theme, Oswald + Roboto Condensed, бренд-правила сайтовика)
- [x] Положить публичную копию в `hq/course/lesson1.html`
- [x] Обновить `hq/index.html` — счётчики, прогресс курса, ссылка на урок
- [x] Push → GitHub Pages

## Делегирование
- Извлечение структуры → general-purpose subagent. Вход: транскрипт 120 КБ. Выход: `lesson1.json` (valid JSON, 10 терминов / 9 методов / 7 фреймворков / 5 целей / 5 ДЗ / 5 цитат).

## Заметки
- Применены дизайн-правила из `~/.openclaw/workspace-sitebuilder/knowledge/design-resources.md`: шрифты Oswald + Roboto Condensed (не Inter/Arial), charcoal `#1a1a1a` (не чистый `#000`), ≤6 секций, 1 H1, 1 CTA, без bounce, без cyan-on-dark.
- Акцент — тёплый oxide `#E05A32`, гармонирует с HQ light-версией (там `#B53A22`).
- В ДЗ-чеклисте живые статусы: ✓ собран HQ, ✓ dashboard, ◐ реальный проект (пути в карточках всё ещё `_(уточнить)_`), ✓ учебные материалы (эта задача), ○ поделиться с потоком.

## Ссылки
- Транскрипт: `personal corp/transcripts/lesson1.txt`
- Структура: `personal corp/lesson1.json`
- Урок: `personal corp/lesson1.html` (локально) + `hq/course/lesson1.html` (Pages)
- Публичный URL: https://instrumentburg-sudo.github.io/hq/course/lesson1.html
