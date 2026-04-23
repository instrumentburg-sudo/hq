---
type: long
status: completed
project: hq
priority: P1
created: 2026-04-22
completed: 2026-04-23
---

# Пересобрать панель в минимализм

## Контекст
Первая версия editorial dark (2026-04-22) оказалась перегруженной: 9 секций, 1785 строк HTML, на мобильном невозможно смотреть. Пользователь: «фокус размывается, на мобильнике невозможно смотреть, не должно быть информационного шума вообще».

## Цель
`hq/index.html` показывает операционный фокус без информационного шума: что сейчас делаю / куда это относится / что из курса приземлилось в работу. 1 экран desktop, mobile-first.

## План
- [x] Собрать feedback (каталог → задачи, минимализм, без шума)
- [x] Сохранить правила в память (feedback_minimalism.md)
- [x] Завести 7 реальных задач в tasks/long и tasks/short
- [x] Переписать `hq/index.html` — итог: карта 4 направлений + 5 top-задач + applied practices (не «3 блока задач», как планировалось — решение уточнилось по ходу)
- [x] Создать под-хабы `service/`, `marketplaces/`, `tenders/`
- [x] Создать `hq-personal/` каркас с Human Gate (второй штаб из урока 2)
- [x] Русификация UI: штаб / сервис / площадки / тендера / личное
- [x] Commit и push в origin/main (279dbca, 1263e45, c54a29e, 63c1ce4)

## Как отклонились от плана
Исходный план — «3 блока задач (в работе · на очереди · ждёт) на одном экране». По ходу brainstorming-а с пользователем решили иначе: **карта направлений** (3 бизнеса + личное) + top-5 задач + блок «применённые практики» из курса. Это легло на урок 2 Personal Corp («два штаба», «правила на двух этажах»). Минимализм сохранён (1 экран desktop, mobile stack), просто ось другая.

## Заметки
- Новый источник правды остался прежним: `tasks/*.md` + `practices/*.md` + `AGENTS.md §6.1`
- Стиль: Modern SaaS dark (General Sans + JetBrains Mono, muted direction-accents), заменил editorial dark
- Обновлена память: `project_hq.md` переписан, добавлен `feedback_language_ru.md`
- Design doc: `hq/docs/plans/2026-04-23-hq-directions-redesign.md`

## Ссылки
- Публичный штаб: https://instrumentburg-sudo.github.io/hq/
- Под-хаб сервиса: https://instrumentburg-sudo.github.io/hq/service/
- Design doc: `docs/plans/2026-04-23-hq-directions-redesign.md`
- feedback_minimalism.md (остаётся актуальным)
