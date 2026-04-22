# Dashboard · Editorial Dark — Design Doc

| Поле     | Значение                                                |
|----------|---------------------------------------------------------|
| Дата     | 2026-04-22                                              |
| Статус   | согласовано, готово к реализации                        |
| Область  | `hq/index.html` (публичный) + задел под `hq/private/me.html` (приватный, отдельной сессией) |
| Источник | brainstorm-сессия (Claude Code, 2026-04-22)             |

## 1. Цель

Пересобрать публичный дашборд `hq/index.html` в тёмной теме с применением дашборд-практик 2026 (SaaSFrame, Muzli, Layout Scene) — сохранив editorial-характер (Instrument Serif + IBM Plex Sans + JetBrains Mono) и усилив персонализацию под владельца (30 проектов, 10 P1, две юр-линии, OpenClaw-оркестра, курс Personal Corp).

## 2. Контекст и ограничения

- Дашборд **публичный**, публикуется на `https://instrumentburg-sudo.github.io/hq/` из `main`.
- `AGENTS.md §9.3` запрещает на дашборде: SSH-адреса, Shop ID, Metrika ID, абсолютные пути, содержимое заметок, финансовые цифры.
- Source of truth — `AGENTS.md`. Дашборд — производная.
- Приватная панель с операционкой (финансы Россети, «Don't Touch»-гардрейл, Metrika snapshot, agent-статусы в реальном времени) — отдельный файл `hq/private/me.html`, в `.gitignore`. В этом doc’е не рассматривается — будет отдельным design-doc.

## 3. Принятые решения (из brainstorm)

1. **Два файла параллельно.** Публичный сейчас, приватный позже.
2. **Editorial Dark.** Сохраняем Instrument Serif, газетный ритм, `§ I / § II`. Переходим в warm charcoal с oxide/brass/moss/amber/stale семантикой.
3. **Hero — D-hybrid.** Headline-позиционирование + live pulse-strip + chip «ex Personal Corp lab».
4. **9 блоков** в вертикальном потоке: Hero → KPI-strip → Chronicle → P1 Bento → Agent Mesh → Full Registry → Tasks → Personal Corp → Footer.
5. **Agent Mesh** — editorial list. Source of truth — новая секция `AGENTS.md § 11`.
6. **Focus — Chronicle.** 4–6 последних событий, лента-моно с семантическими dot-ами.
7. **Bento P1** — 4 hero 2×1 + 6 compact 1×1, выбор по бизнес-критичности + recency-heat overlay (5-dot шкала).
8. **Две юр-линии разделены** — `Blagoystroystvo` выносится в 8-ю группу `ИП Дедков · Россети Урал (1)`.

## 4. Визуальный язык

### 4.1 Палитра (OKLCH)

```css
:root {
  /* Surface (4 уровня elevation) */
  --surface-0:  oklch(0.14 0.012 65);   /* base — почти чёрный, тёплый */
  --surface-1:  oklch(0.18 0.012 65);   /* карточки, панели */
  --surface-2:  oklch(0.22 0.015 65);   /* hover, selected */
  --surface-3:  oklch(0.27 0.018 65);   /* popover, tooltip */

  /* Text */
  --ink-hi:     oklch(0.93 0.012 80);   /* primary, ~14:1 к surface-0 */
  --ink-mid:    oklch(0.72 0.020 80);   /* secondary, ~6:1 */
  --ink-lo:     oklch(0.55 0.020 80);   /* meta, ~3:1 — только large/mono */

  /* Семантика (бренд) */
  --oxide:      oklch(0.66 0.18 30);    /* accent, ржавчина, ссылки, hero */
  --brass:      oklch(0.76 0.12 75);    /* secondary, numbers */
  --moss:       oklch(0.74 0.17 145);   /* active */
  --amber:      oklch(0.80 0.15 82);    /* paused/warn */
  --stale:      oklch(0.55 0.16 28);    /* stale/blocked */

  --border:     oklch(0.28 0.010 65 / 0.6);
}
```

- sRGB-fallback через `@supports not (color: oklch(0 0 0))`.
- Light fallback через `@media (prefers-color-scheme: light)` — переключает `:root` на текущую paper-палитру (сохраняем возможность светлой версии).
- High-contrast через `@media (prefers-contrast: more)`.
- `forced-colors: active` — системные цвета (Canvas, CanvasText, LinkText, AccentColor).

### 4.2 Типографика

- **Instrument Serif** (характер). Hero-numerals — `font-weight: 500` + `text-shadow: 0 0 1px currentColor` (synthetic bolder для компенсации тонких штрихов на тёмном). Features: `"ss01", "cv11", "dlig", "kern"`. Italic — 1.2rem минимум (на тёмном italic читается тяжелее).
- **IBM Plex Sans** (тело). 1rem body, line-height 1.55. Features: `"ss01", "ss02", "cv11", "tnum"` (tabular для таблиц и chronicle).
- **JetBrains Mono** (данные). 0.7–0.85rem, uppercase, `letter-spacing: 0.14em`. Features: `"ss01", "ss02", "zero"` (slashed zero).
- Font-smoothing: `antialiased` / `grayscale` — критично для серифов на dark.
- Meta-текст (weight 300) — не ниже 0.8rem.

### 4.3 Ритм

- Base unit 8px (`0.5rem`). Scale: 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 160.
- Section: `border-top: 1px solid var(--border)` + `padding-top: 2.5rem` + `padding-bottom: 3.5rem`.
- Container: `max-width: 1260px`, padding `clamp(1.75rem, 4vw, 3rem) clamp(1.25rem, 4vw, 2.5rem) 6rem`.

## 5. Структура секций

### 5.1 Masthead / Hero (D-hybrid)

- Nav-rail сверху (mono): `● LIVE · instrumentburg-sudo/hq · AGENTS.md ↗ · Last build: <time>`.
- Hero composition: `mono-mark "30"` + `&` oxide italic + serif caption `hq — центр оркестрации`.
- Two-col lede:
  - Слева (serif italic): «Хаб агент-оркестрации. Один человек, два контура, тридцать проектов.»
  - Справа (mono pulse-strip):
    ```
    UPDATED  22·04·2026
    ACTIVE   14 · PAUSED 10 · STALE 6
    P1       10 · P2 14 · P3 6
    LAST     apps/dashboard · 22·04
    COURSE   Personal Corp · lesson 01 ✓
    ```
- Chip в углу: `ex Personal Corp · sereja.tech ↗` — 0.7rem mono uppercase, border oxide, hover → oxide-fill.

### 5.2 § 0 · KPI Strip

4 тайла, разделены `1px solid var(--border)`:

| #           | Число  | Подпись            | Акцент        |
|-------------|--------|--------------------|---------------|
| 1 (top-left)| 30     | проектов в хабе    | oxide (F-pt)  |
| 2           | 14     | active             | moss pulse-dot|
| 3           | 10     | P1 ядро            | brass         |
| 4           | 22·04  | updated · live     | ink-mid mono  |

Цифра — serif 3.5rem, подпись — mono uppercase 0.7rem, подзаголовок — sans 0.9rem.

### 5.3 § I · Focus — Chronicle

Лента 4–6 последних событий:

```
22·04  ●  HQ           обновил index.html под editorial dark
22·04  ●  DASHBOARD    fetch_modulbank cron ok
21·04  ●  CALCULATOR   +UTM tracking
20·04  ●  AVITO-ADS    партия каруселей v12
20·04  ●  CORP         урок 01 опубликован
```

- Дата: mono brass 0.85rem.
- Dot: семантический (moss=active, amber=paused, oxide=release).
- Тикер: mono uppercase bold 0.8rem, цвет — per-project chip.
- Событие: serif italic 1.1rem.
- События старше 7 дней не показываются.
- Empty state: «_Период консолидации — за неделю коммитов по P1 не было._» + `/LOG · WEEKLY · 00/05`.

### 5.4 § II · Ядро P1 (Bento)

4 hero 2×1:
- `instrumentburg` (монорепо)
- `apps/website` (instrumentburg.ru)
- `Blagoystroystvo` (Россети)
- `apps/avito-ads` (пайплайн)

6 compact 1×1:
- `apps/dashboard`, `apps/calculator`
- `apps/avito-responder` (paused), `instrumentburg-responder` (paused)
- `hq`, `claude-skills`

Grid desktop: `repeat(4, 1fr)`, hero = `span 2`. Tablet: `repeat(2, 1fr)`. Mobile: `repeat(1, 1fr)`, hero = `min-height: 200px`, compact = `min-height: 140px`.

Карточка: номер `01`–`10`, priority pill (P1 · active/paused), name serif с `slash` разделителем, goal sans 1rem, meta stack mono, recency-dots, commit date.

Recency-heat шкала (5 dots):

| Давность       | Dots        | Цвет         |
|----------------|-------------|--------------|
| ≤ 3 дней       | `●●●●●`     | moss         |
| 4–7            | `●●●●○`     | moss         |
| 8–14           | `●●●○○`     | brass        |
| 15–30          | `●●○○○`     | brass-dim    |
| > 30           | `●○○○○`     | stale        |
| paused         | `◐◐◐◐◐`     | amber        |

Hover: `translateY(-2px)` + `border-color: var(--oxide)` + `box-shadow: 0 8px 24px -12px oklch(0.66 0.18 30 / 0.3)`.

### 5.5 § III · Agent Mesh OpenClaw

Editorial list, 2 колонки × 5 строк desktop, 1 колонка mobile.

```
§ III · ОРКЕСТРА
10 агентов OpenClaw · Telegram-инстанс на VPS

●  main clawd    ·  дирижёр, общий контроль
●  sitebuilder   ·  сайт instrumentburg.ru (SEO)
●  master        ·  мастер-агент категорий
●  marketer      ·  Метрика, Wordstat, Direct
●  advertiser    ·  Avito, Direct-объявления
●  chaser        ·  заказы Ozon / WB
●  mailer        ·  рассылки клиентам
●  dispatcher    ·  маршрутизация сообщений
◐  finik         ·  финансовый ассистент
◐  nutritionist  ·  личный, вне ИБ

легенда: ● active · ◐ partial · ○ paused
```

Имя: mono 0.95rem. Роль: serif italic 1rem. Разделитель `·` — brass. Вертикальная `border-left: 1px solid var(--border)` между колонками.

Source of truth — `AGENTS.md § 11. OpenClaw агенты` (новая секция, см. §6 ниже).

### 5.6 § IV · Полный реестр

**8 групп** (вместо 7 сейчас):

1. ИнструментБург · ядро (3)
2. ИнструментБург · операции (10) — `Blagoystroystvo` выносится
3. ИнструментБург · база знаний (2)
4. **ИП Дедков · Россети Урал (1)** — новая группа, `Blagoystroystvo`
5. Клиенты (3)
6. Персональные (2)
7. Платформенные (6)
8. Архив / эксперименты (3)

Итого 30 проектов.

Группа `ИП Дедков · Россети Урал` визуально выделена: заголовок brass вместо ink-hi, pre-текст mono italic «юр. контур 2».

Строки реестра: priority pill (P1/P2/P3), status-dot (moss/amber/stale), name + subtitle, stack, commit date. Borders между рядами `1px solid oklch(var(--border) / 0.4)`, hover `background: var(--surface-1)`. Title-attr (абсолютный путь) сохраняется для локального использования.

### 5.7 § V · Задачи

2 колонки (Long / Short). Empty state усиливается:

```
ДЛИННЫЕ                              0 / 0 открыты
────────────────────────────────────────────────
—
инбокс пуст

  ⌘  новая длинная задача            /tasks/long/
  ↳  последняя закрытая: <name>      → /done/
```

Относительные пути, mono-подсказки, archive-строка как сигнал живости.

### 5.8 § VI · Personal Corp

Текущий блок с прогресс-барами. Bar-fill — gradient brass → oxide, bar-bg — surface-2. Strip-note снизу: «_следующий урок публикуется в hq/course/lessonN.html_».

### 5.9 Footer

4 колонки mono 0.75rem uppercase: `© MMXXVI · ИнструментБург` · `Правила: AGENTS.md` · `Репо: instrumentburg-sudo / hq` · `Build: <timestamp>`.

## 6. Изменения в source of truth (`AGENTS.md`)

Одним коммитом перед генерацией HTML:

1. **§ 6.1** — вынести `Blagoystroystvo` из группы «ИнструментБург · операции» в новую группу `ИП Дедков · Россети Урал (1)`. Обновить счётчик «операций» (11 → 10).
2. **§ 11. OpenClaw агенты** (новая секция в конец) — таблица 10 агентов:
   - колонки: имя, роль, канал (Telegram @handle — **общий**, не индивидуальный, т.к. dashboard публичный: вместо `@ib_site_ai_bot` → `sitebuilder`), статус (●/◐/○).
   - легенда.
   - примечание: «Machine-readable source для `hq/index.html § III`.»
3. **§ 9.2** — дополнить список того, что показывает dashboard: KPI-strip (4 числа), Chronicle (4–6 событий), Agent Mesh (10 агентов, без @handle), recency-heat на карточках.
4. **§ 9.3** — дополнить исключение: **полные Telegram @handle-адреса агентов не публикуем**, только имена ролей.

## 7. Accessibility

- Text contrast: primary 4.5:1, secondary 4.5:1, meta 3:1 (только large/mono).
- Non-text contrast: 3:1 (borders, focus-ring, icons, pulse-dots).
- Focus-ring: `outline: 2px solid var(--oxide); outline-offset: 2px`.
- `prefers-color-scheme: light` → paper fallback.
- `prefers-contrast: more` → ink-hi borders, no pulse.
- `prefers-reduced-motion: reduce` → без pulse и reveal.
- `forced-colors: active` → системные цвета.
- Semantic HTML + aria-labels для статус-дотов.

## 8. Micro-interactions

- Pulse-dot: 2.4s ease-out (как сейчас), off на reduced-motion.
- Hero-numerals reveal: opacity 0→1, translateY 8px→0, 600ms, cascade 80ms.
- Карточка hover: transform + border + shadow.
- Recency-dots: статично.

## 9. План работы

1. ✓ Brainstorm + design-doc (2026-04-22).
2. Обновить `AGENTS.md` (§6.1 новая группа, §11 OpenClaw, §9.2/§9.3 update). Commit + push.
3. Сгенерировать `index.html` через скиллы: **frontend-design** (ядро), **arrange** (layout), **typeset** (типографика), **colorize** (палитра), **polish** (финальный проход). Для критичных участков — codex review.
4. Локальная проверка: open file, переключить prefers-color-scheme (DevTools), WCAG contrast smoke, focus-ring на Tab-обходе.
5. Commit `dashboard: rebuild to editorial dark (2026 best practices)` + push. GitHub Pages 1–2 мин.
6. (Отдельная сессия) Приватный `hq/private/me.html` — design-doc отдельно.

## 10. Out of scope (не делаем сейчас)

- Приватный дашборд `me.html` — отдельной сессией.
- Автоматический сбор данных (cron по git log всех 30 репо) — ручной pulse-strip / chronicle пока достаточно.
- Переключатель тем light/dark в UI — работает только через OS `prefers-color-scheme`.
- Экспорт в PDF / публикация в RSS.
- Интеграция с Яндекс.Метрикой / Convex / LiveSklad (это публичный, §9.3 запрещает).

## 11. Источники best practices (2026)

- SaaSFrame — «Anatomy of High-Performance SaaS Dashboard Design» (2026-01), F-pattern, operational dashboards, next-best-action, data-viz golden rule.
- SaaSFrame — «Designing Bento Grids That Actually Work» (2026-02), compartmentalization, size = hierarchy, uniform gutters 16–24px.
- Muzli — «Dark Mode Design Systems» (2026-04), 4-level elevation, semantic tokens, dark-first as design decision.
- Greeden blog — «Dark Mode / High Contrast Accessibility Guide» (2026-02), WCAG 2.1 AA для dark.
- Orami / Medium — «Responsive Accessible Color Schemes in CSS 2026», OKLCH, semantic tokens, @supports fallbacks.

---

_Design-doc фиксирует состояние на 2026-04-22. Все правки концепции — через новый design-doc в `hq/docs/plans/`._
