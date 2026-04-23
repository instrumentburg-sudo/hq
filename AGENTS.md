# HQ — Правила агента

Хаб для оркестрации агентов и управления проектами ИнструментБург. Этот файл — **единственный источник правды** о том, как устроена папка, как работает агент, и какие проекты активны.

## Оглавление

1. [Назначение папки](#1-назначение-папки)
2. [Структура](#2-структура)
3. [Workflow агента](#3-workflow-агента)
4. [Задачи: классификация и жизненный цикл](#4-задачи)
5. [Шаблоны задач](#5-шаблоны-задач)
6. [Проекты: реестр и карточки](#6-проекты)
7. [Делегирование субагентам](#7-делегирование-субагентам)
8. [Архив завершённых задач](#8-архив-завершённых-задач)
9. [Dashboard и GitHub Pages](#9-dashboard-и-github-pages)
10. [Что НЕ делать](#10-что-не-делать)
11. [OpenClaw агенты](#11-openclaw-агенты)

---

## 1. Назначение папки

Здесь **не живёт код** проектов. Здесь живут:
- правила работы (этот файл);
- карточки активных проектов (инлайн ниже, раздел 6);
- задачи — длинные и короткие, в подпапках `tasks/`, создаются по мере появления.

Код проектов — в их реальных директориях. Путь указан в карточке каждого проекта.

---

## 2. Структура

**Сейчас:**

```
hq/
├── AGENTS.md           — правила (этот файл)
├── CLAUDE.md           — указатель на AGENTS.md для Claude Code
└── index.html          — dashboard, публикуется на GitHub Pages
```

**По мере появления задач:**

```
hq/
├── AGENTS.md
├── CLAUDE.md
├── index.html
└── tasks/
    ├── long/<название>.md
    ├── short/<YYYY-MM-DD-название>.md
    └── done/<перенесённые>.md
```

Подпапки `tasks/long/`, `tasks/short/`, `tasks/done/` агент создаёт по требованию при появлении первой задачи соответствующего типа.

---

## 3. Workflow агента

### 3.1. Порядок входа в HQ

При первом входе / новой сессии агент делает строго в таком порядке:

1. Читает `AGENTS.md` (этот файл).
2. Смотрит активные проекты в разделе [Реестр проектов](#61-реестр-активных-проектов).
3. Смотрит `tasks/long/` и `tasks/short/` (если существуют) — что в работе.
4. Если пользователь даёт новую задачу:
   - классифицирует (короткая / длинная) — см. 4.1;
   - создаёт файл из шаблона в нужной подпапке (создавая папку, если её нет);
   - если задача связана с проектом — сначала читает карточку проекта в разделе 6.2, **потом** исполняет или делегирует.

### 3.2. Execution contract

Каждое действие агента проходит **5 фаз** в строгом порядке:

1. **Explore** — собрать минимально достаточный контекст (карточка проекта, файл задачи, релевантные файлы кода). Не больше, не меньше.
2. **Plan** — определить шаги и зависимости. Для длинной задачи — записать план в task-файл.
3. **Execute** — выполнить шаг самому или делегировать субагенту (см. раздел 7).
4. **Verify** — проверить результат: файл существует, не пустой, содержимое корректно. **Не верить отчёту субагента** — читать артефакт.
5. **Update** — обновить task-файл (статус, галочки плана, заметки) и кратко отчитаться пользователю.

Жёсткие правила:
- Не считать задачу завершённой без фазы **Verify**.
- Не путать действие и отчёт: сначала сделать, потом сообщить.
- Если упираешься в недостающие данные / доступы — перевести задачу в `blocked` и зафиксировать условие разблокировки.

### 3.3. Формат отчёта пользователю (фаза Update)

После каждого завершённого шага сообщать кратко (≤4 строк):

- **Что сделано** — конкретный артефакт / действие.
- **Что проверено** — как убедился, что работает.
- **Статус** — `in_progress` / `completed` / `blocked`.
- **Следующий шаг** — если есть.

Для `blocked` дополнительно: что именно нужно для разблокировки.

---

## 4. Задачи

### 4.1. Классификация

**Короткая** (`short`) — задача, в которой одновременно выполняются **ВСЕ** условия:
- один основной результат;
- нет необходимости в декомпозиции на шаги;
- нет длинной цепочки зависимостей;
- обычно укладывается в один рабочий подход (<1 день).

Примеры: «проверить метрику за вчера», «обновить прайс на Avito», «добавить sameAs в schema».

**Длинная** (`long`) — задача, в которой выполняется **хотя бы одно** условие:
- нужен план из нескольких шагов;
- есть зависимости между шагами или внешними системами;
- несколько артефактов или этапов;
- нужна координация субагентов;
- работа вероятно не закончится за один подход.

Примеры: «SEO 20 категорий», «LiveSklad-интеграция в бот», «НДС за квартал».

**Правило по умолчанию:** если нужен план — `long`. При сомнениях — `long` (легче потом понизить до `short`, чем наоборот).

Отдельно: `info` — запрос, на который достаточно ответить без создания task-файла. Не сохраняется.

### 4.2. Жизненный цикл

```
pending  →  in_progress  →  completed  →  (перенос в done/)
                ↓
             blocked  (с указанием причины и условия разблокировки)
```

Статус — в frontmatter файла. Обновляется агентом по ходу работы.

### 4.3. Именование файлов

- **Короткие:** `YYYY-MM-DD-краткое-описание.md` — дата создания в имени, задача короткоживущая.
- **Длинные:** `краткое-описание.md` — дата только во frontmatter, задача живёт долго.
- Kebab-case, кириллица допустима, **без пробелов**.

### 4.4. Работа с задачей

| Действие | Что делает агент |
|---|---|
| Создать | Файл в `tasks/long/` или `tasks/short/` по шаблону из раздела 5 |
| Начать | Во frontmatter `status: in_progress` |
| Завершить | `status: completed`, добавить `completed: YYYY-MM-DD`, перенести в `tasks/done/` |
| Заблокировать | `status: blocked`, в `## Заметки` — причина и условие разблокировки |

### 4.5. Критерий завершения

Задача считается завершённой только если **ВСЕ** условия выполнены одновременно:

1. **Артефакт существует.** Создан или изменён требуемый файл / PR / отчёт / запись в системе.
2. **Результат проверен.** Не «агент сказал done», а прочитан файл / запущен grep / проверен вывод.
3. **Task-файл обновлён.** План с галочками, заметки о ходе, зафиксированные решения.
4. **Статус переведён** в `completed` (или `blocked` с условием разблокировки).
5. **Итог зафиксирован** в `## Заметки` — что получилось, какие выводы.

Если хотя бы одно условие не выполнено — задача **не завершена**, даже если кажется, что «всё сделано».

---

## 5. Шаблоны задач

### 5.1. Длинная задача

Файл: `tasks/long/<название>.md`

```markdown
---
type: long
status: pending
project: <имя проекта из реестра, например instrumentburg-website>
priority: P1
created: YYYY-MM-DD
deadline: YYYY-MM-DD
---

# <Название задачи>

## Контекст
Зачем делается. Какую проблему решает. Откуда пришла задача.

## Цель
Проверяемый критерий готовности. Не «улучшить SEO», а «описания 20 категорий раздела X опубликованы и проиндексированы Вебмастером».

## План
- [ ] Шаг 1 — что делаем, какой результат
- [ ] Шаг 2
- [ ] Шаг 3

## Делегирование
- Шаг 1 → агент/скилл X. Вход: <путь>. Выход: <артефакт>.
- Шаг 2 → ...

## Заметки
Что выяснили, блокеры, принятые решения.

## Ссылки
- Связанные короткие задачи: tasks/short/...
- Дашборды, документы, тикеты: ...
```

### 5.2. Короткая задача

Файл: `tasks/short/YYYY-MM-DD-<название>.md`

```markdown
---
type: short
status: pending
project: <имя проекта или "—">
priority: P1
created: YYYY-MM-DD
---

# <Название задачи>

## Что сделать
Одно-два предложения. Без плана — короткая задача не требует декомпозиции.

## Результат
Что должно получиться. Куда положить / отправить / кому показать.

## Заметки
_(заполняется по ходу или после завершения, если были нюансы)_
```

---

## 6. Проекты

### 6.1. Полный реестр

**Итого: 30 проектов** — 14 active, 10 paused, 6 stale. Приоритеты: 10 × P1, 14 × P2, 6 × P3.

Полная машиночитаемая версия реестра — в `/tmp/projects-registry.json` (генерится по запросу, в git не хранится).

#### ИнструментБург · ядро (3)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| [instrumentburg](#instrumentburg) | `/home/iamsohappy/projects/instrumentburg` | Convex, Node.js, MD vault | **P1** | active | 2026-04-21 |
| [apps/website](#instrumentburg-apps-website) | `/home/iamsohappy/projects/instrumentburg/apps/website` | ocStore 3, OpenCart, Twig, PHP 8.3 | **P1** | active | 2026-04-08 |
| [instrumentburg-responder](#instrumentburg-responder) | `/home/iamsohappy/projects/instrumentburg-responder` | Python, Anthropic SDK | **P1** | paused | 2026-03-09 |

#### ИнструментБург · операции (10)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| [apps/avito-ads](#instrumentburg-apps-avito-ads) | `/home/iamsohappy/projects/instrumentburg/apps/avito-ads` | Python, YAML, XML feed | **P1** | active | 2026-04-20 |
| apps/avito-responder | `/home/iamsohappy/projects/instrumentburg/apps/avito-responder` | Python, Anthropic API, systemd | **P1** | paused | 2026-03-08 |
| [apps/calculator](#instrumentburg-apps-calculator) | `/home/iamsohappy/projects/instrumentburg/apps/calculator` | Vite, TS, Convex, Chart.js, Vercel | **P1** | active | 2026-04-21 |
| [apps/dashboard](#instrumentburg-apps-dashboard) | `/home/iamsohappy/projects/instrumentburg/apps/dashboard` | HTML, ApexCharts, Python, cron | **P1** | active | 2026-04-22 |
| apps/b2b-outreach | `/home/iamsohappy/projects/instrumentburg/apps/b2b-outreach` | Python, CSV pipelines, DaData | P2 | paused | 2026-03-10 |
| apps/max-miniapp | `/home/iamsohappy/projects/instrumentburg/apps/max-miniapp` | Vite, React 18, FastAPI | P2 | paused | 2026-03-04 |
| AIzakaznaryad | `/home/iamsohappy/projects/AIzakaznaryad` | Vite, vanilla JS, Supabase, jsPDF | P2 | paused | 2026-03-23 |
| Rentalnew | `/home/iamsohappy/projects/Rentalnew` | Next.js 14, Supabase, shadcn/ui | P2 | paused | 2026-03-04 |
| Tenders | `/home/iamsohappy/projects/Tenders` | JSON state files, DOCX/XLSX | P2 | active | — |
| apps/DMDGU | `/home/iamsohappy/projects/instrumentburg/apps/DMDGU` | документация (DOCX, PDF, XLSX) | P3 | stale | 2026-02-02 |

#### ИнструментБург · база знаний (2)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| ib-digest | `/home/iamsohappy/projects/ib-digest` | Python, HTML, OpenClaw cron | P2 | active | 2026-04-22 |
| ib-vault | `/home/iamsohappy/projects/ib-vault` | Markdown (Obsidian), JSON schema | P2 | active | — |

#### ИП Дедков · Россети Урал (1)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| [Blagoystroystvo](#blagoystroystvo) | `/home/iamsohappy/projects/Blagoystroystvo` | Next.js 16, Convex, Tailwind v4, OpenAI | **P1** | active | 2026-04-22 |

#### Клиенты (3)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| tagil-instrument | `/home/iamsohappy/projects/tagil-instrument` | Next.js 15, Payload CMS 3, Postgres | P2 | active | 2026-04-01 |
| TheJungle | `/home/iamsohappy/projects/TheJungle` | FastAPI, React 18, Vite, Docker | P2 | paused | 2026-04-02 |
| Stroyka | `/home/iamsohappy/projects/Stroyka` | документы (ИП Пихенек, СОШ Кушва) | P3 | stale | — |

#### Персональные (2)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| [personal-corp](#personal-corp) | `/home/iamsohappy/projects/Githab/personal corp` | HTML, JSON, транскрипты | P2 | active | — |
| health-tracker | `/home/iamsohappy/projects/health-tracker` | Markdown vault (Obsidian-like) | P2 | paused | 2026-03-04 |

#### Платформенные (6)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| [hq](#hq) | `/home/iamsohappy/projects/Githab/hq` | Markdown, HTML (static) | **P1** | active | 2026-04-22 |
| [claude-skills](#claude-skills) | `/home/iamsohappy/projects/claude-skills` | Markdown prompts, shell/python | **P1** | active | 2026-04-21 |
| agent-second-brain | `/home/iamsohappy/projects/agent-second-brain` | Python, aiogram, Deepgram, Todoist | P2 | active | 2026-04-13 |
| openclaw-hub | `/home/iamsohappy/projects/openclaw-hub` | Python, MD templates | P2 | paused | 2026-03-09 |
| srv-kvm | `/home/iamsohappy/projects/srv-kvm` | KVM/QEMU, libvirtd, ZFS, OpenVPN | P2 | paused | — |
| telethon | `/home/iamsohappy/projects/telethon` | Python, Telethon (single login.py) | P3 | stale | — |

#### Архив / эксперименты (3)

| Проект | Путь | Стек | Приор. | Статус | Коммит |
|---|---|---|:-:|:-:|:-:|
| Brainstorm | `/home/iamsohappy/projects/Brainstorm` | (только docs) InfographicsGen концепция | P3 | stale | 2026-01-22 |
| `Brainstorm ` | `/home/iamsohappy/projects/Brainstorm ` | случайная папка с XLSX-шаблоном | P3 | stale | — |
| DashboardAI | `/home/iamsohappy/projects/DashboardAI` | ранний прототип, заменён apps/dashboard | P3 | stale | — |

---

### 6.2. Подробные карточки P1

Ниже — карточки проектов с приоритетом **P1**. Для P2/P3 хватает строки в реестре 6.1; подробная карточка заводится при переходе в P1 или при появлении нетривиальных «ключевых точек» / «не трогать».

---

<a id="instrumentburg"></a>

#### instrumentburg

- **Путь:** `/home/iamsohappy/projects/instrumentburg`
- **Статус:** active · **Приоритет:** P1
- **Цель:** монорепо ИнструментБург — Convex backend, Telegram-бот онбординга, Obsidian-like база знаний, все `apps/*` подпроекты.
- **Стек:** Convex, Node.js, Markdown vault

**Контекст.** Основное пространство разработки бизнеса. Внутри — и код (apps/), и операционная информация (00-meta, 01-onboarding, 04-clients, 08-pricing).

**Ключевые точки:**
- Convex: **dev deployment** (прод не использовать).
- LiveSklad Shop ID: `5c615f26149eb4750c36b897`.
- Obsidian vault в `knowledge/` — дубль `ib-vault`.

**Не трогать:** Convex prod deployment.

---

<a id="instrumentburg-apps-website"></a>

#### instrumentburg / apps / website

- **Путь:** `/home/iamsohappy/projects/instrumentburg/apps/website`
- **Статус:** active · **Приоритет:** P1
- **Цель:** SEO-продвижение категорий ремонта и рост органического трафика.
- **Стек:** ocStore 3 (OpenCart), Twig, PHP 8.3, MariaDB

**Контекст.** Основной сайт бизнеса. Отдельный git `instrumentburg-website`. Мониторится через Яндекс.Вебмастер и Метрику.

**Ключевые точки:**
- Прод URL: https://instrumentburg.ru
- Прод SSH: `ssh c50684@h31.netangels.ru`, путь `/home/c50684/instrumentburg.ru/www/`
- Метрика ID: `77310175`
- Агент в OpenClaw: `sitebuilder` (@ib_site_ai_bot)

**Не трогать:** `header.twig`, `header_4.twig` — недавно правились, стабильны.

---

<a id="instrumentburg-responder"></a>

#### instrumentburg-responder

- **Путь:** `/home/iamsohappy/projects/instrumentburg-responder`
- **Статус:** paused · **Приоритет:** P1
- **Цель:** единый агент-ответчик для клиентов во всех каналах (Авито, MAX, Telegram, сайт).
- **Стек:** Python, Anthropic SDK, knowledge_base (MD + JSON)

**Контекст.** Ядро + канальные адаптеры на OpenClaw VPS. Наследник раздельных `avito-responder` / `max-miniapp` и т.п.

**Не трогать:** прод-деплой (канальные адаптеры зеркалят сообщения — ломается вся цепочка ответов).

---

<a id="instrumentburg-apps-avito-ads"></a>

#### instrumentburg / apps / avito-ads

- **Путь:** `/home/iamsohappy/projects/instrumentburg/apps/avito-ads`
- **Статус:** active · **Приоритет:** P1
- **Цель:** пайплайн объявлений Авито — YAML-объявления, 9-слайдовые карусели, XML-фид, деплой на сервер автозагрузки.
- **Стек:** Python, YAML, XML feed, HTML templates

**Ключевые точки:**
- Скилл: `avito-feed-pipeline` (в `~/.claude/skills/`).
- Процесс: YAML → 9 слайдов → фид → деплой, с security-валидацией.

---

<a id="instrumentburg-apps-calculator"></a>

#### instrumentburg / apps / calculator

- **Путь:** `/home/iamsohappy/projects/instrumentburg/apps/calculator`
- **Статус:** active · **Приоритет:** P1
- **Цель:** Калькулятор СЦ — расчёт ремонта, трекер запчастей, сметы, технические заключения.
- **Стек:** Vite, TypeScript, Convex, Chart.js, Vercel

**Контекст.** Отдельный git, хостится на Vercel. Использует Convex из монорепо.

---

<a id="instrumentburg-apps-dashboard"></a>

#### instrumentburg / apps / dashboard

- **Путь:** `/home/iamsohappy/projects/instrumentburg/apps/dashboard`
- **Статус:** active · **Приоритет:** P1
- **Цель:** финансовый и маркетинговый дашборд (7 вкладок): Метрика, Avito, Direct, LiveSklad, Модульбанк, Convex.
- **Стек:** HTML, ApexCharts, Python (fetch_modulbank, gen_pnl), bash cron

**Ключевые точки:**
- Cron: 18:00 Asia/Yekaterinburg (автоматическое обновление данных).

---

<a id="blagoystroystvo"></a>

#### Blagoystroystvo

- **Путь:** `/home/iamsohappy/projects/Blagoystroystvo`
- **Статус:** active · **Приоритет:** P1
- **Цель:** внутренний сервис ИП Дедков для работы по договору благоустройства с **ПАО Россети Урал** — сметы КС-2/КС-3/ЛС, учёт расходов, маржа.
- **Стек:** Next.js 16, React 19, Convex, Tailwind v4, OpenAI, ExcelJS

**Контекст.** Отдельная юр-сущность (ИП Дедков как подрядчик), отдельная денежная линия. Финразрыв 107К, ожидание оплат 400–500К.

---

<a id="hq"></a>

#### hq

- **Путь:** `/home/iamsohappy/projects/Githab/hq`
- **Статус:** active · **Приоритет:** P1
- **Цель:** оркестрация агентов и реестр проектов (этот файл + dashboard).
- **Стек:** Markdown, HTML (static, GitHub Pages)
- **Публично:** https://instrumentburg-sudo.github.io/hq/

---

<a id="claude-skills"></a>

#### claude-skills

- **Путь:** `/home/iamsohappy/projects/claude-skills`
- **Статус:** active · **Приоритет:** P1
- **Цель:** коллекция кастомных скиллов Claude Code (66+ шт: geo, audit, humanizer-ru, avito-feed-pipeline, tax-reporting-ib и др.).
- **Стек:** Markdown prompts, shell/python helpers

---

<a id="personal-corp"></a>

#### personal-corp

- **Путь:** `/home/iamsohappy/projects/Githab/personal corp` *(пробел в имени — квотировать при обращении)*
- **Статус:** active · **Приоритет:** P2
- **Цель:** материалы курса Серёжи Риса «Personal Corp» (агент-оркестрация).
- **Стек:** HTML, JSON, Markdown транскрипты

**Контекст.** Уроки курса + извлечённые материалы. Урок 01 — HQ и агент-оркестрация; урок 02 — масштабирование без оверинженеринга (слои стратегии/исполнения, скиллы, Human Gate, Claude+Codex). Публичные копии выжимок в `hq/course/lesson{N}.html`.

---

### 6.3. Правила работы с реестром

- **Новый проект** → добавить строку в таблицу соответствующей группы в 6.1. Если P1 — завести подробную карточку в 6.2.
- **Повышение до P1** → добавить подробную карточку в 6.2.
- **На паузу / stale** → статус в колонке, карточка (если была) остаётся без изменений.
- **Архивация** → в подраздел «Архив / эксперименты» в 6.1; из 6.2 удалить.
- **Обязательные поля** в реестре: Путь (абсолютный), Стек, Приоритет, Статус.
- **Обязательные поля** в карточке P1: Путь, Статус, Приоритет, Цель, Стек.
- **Не дублировать** информацию о проекте вне этого файла — все «ключевые точки» и «не трогать» только в карточке.
- **Регенерация реестра:** discovery-субагент сканирует `~/projects/`, пишет JSON в `/tmp/projects-registry.json`, агент сверяет с 6.1 и обновляет разницу.

---

## 7. Делегирование субагентам

Для длинных задач агент работает **как оркестратор, не как исполнитель**.

1. **Подготовка контекста.** Перед делегированием — прочитать карточку проекта в разделе 6.2 (путь, стек, ключевые точки, «не трогать»).
2. **Фокусированный input.** Субагент получает:
   - путь к реальному проекту (абсолютный);
   - ссылку на файл задачи `tasks/long/X.md`;
   - конкретный шаг (не «разберись сам»).
3. **Чёткий output.** Что должно быть на выходе: файл, PR, отчёт, лог.
4. **Верификация.** После завершения шага — **проверить файлы на диске** (существуют, не пустые, содержимое корректно). Не верить отчёту субагента: отчёт описывает намерение, а не результат.
5. **Обновление задачи.** Отметить шаг как выполненный в файле задачи, добавить заметку о результате в `## Заметки`.

---

## 8. Архив завершённых задач

Живёт в `tasks/done/`. Правила переноса:

- Файл переносится **как есть**, структура frontmatter и секций сохраняется.
- Во frontmatter: `status: completed` + добавляется `completed: YYYY-MM-DD`.
- В `## Заметки` — финальный итог: что получилось, какие выводы, что пригодится в похожих задачах.

**Поиск по архиву:**

```bash
grep -rli "keyword" tasks/done/
grep -l "project: instrumentburg-bot" tasks/done/
```

---

## 9. Dashboard и GitHub Pages

Визуальная сводка проектов и задач — файл `index.html` в корне `hq/`, публикуется на GitHub Pages.

- **URL:** https://instrumentburg-sudo.github.io/hq/
- **Репозиторий:** https://github.com/instrumentburg-sudo/hq

### 9.1. Когда перезаписывать

Агент **полностью перезаписывает** `index.html` и пушит в `origin/main` при любом из событий:

- создание новой задачи (long или short);
- изменение статуса задачи (`pending` → `in_progress` → `completed` → `blocked`);
- перенос задачи в `tasks/done/`;
- добавление, изменение или удаление проекта в разделе 6;
- изменение приоритета проекта или задачи.

### 9.2. Что показывает

Dashboard ориентирован **на задачи, не на проекты**. Три блока:

- **В работе** — задачи со статусом `in_progress` из `tasks/long/` и `tasks/short/`. Формат строки: проект · краткое название задачи.
- **На очереди** — задачи со статусом `pending`.
- **Ждёт** — задачи со статусом `blocked` (с коротким описанием условия разблокировки в задаче).

В футере — 4 ссылки: полный реестр проектов (§6), оркестра агентов (§11), курс Personal Corp — последний урок (`course/lesson{N}.html`, сейчас `lesson2.html`), репозиторий на GitHub.

Всё остальное (реестр 30 проектов, подробные карточки, OpenClaw, прогресс курса) — **в AGENTS.md**, не на дашборде. Dashboard — операционная панель «что делать прямо сейчас», а не витрина проектов.

### 9.3. Что НЕ показывает

Чувствительные точки из карточек проектов:

- SSH-адреса серверов;
- Shop ID, Metrika ID и прочие идентификаторы;
- абсолютные пути к локальным репо;
- содержимое секции `## Заметки` из task-файлов;
- полные Telegram @handle агентов OpenClaw — только имена ролей;
- финансовые цифры, суммы договоров, ожидаемые оплаты.

Dashboard **публичный** — всё, что не должно быть видно всем, в HTML не попадает.

### 9.4. Процесс обновления

После любого изменения задач/проектов:

```bash
cd ~/projects/Githab/hq

# 1. Перезаписать index.html полностью
#    (источники: AGENTS.md и содержимое tasks/)

# 2. Коммит и пуш
git add .
git commit -m "dashboard: <краткое описание изменения>"
git push origin main
```

GitHub Pages автоматически пересобирает страницу за 1–2 минуты после push.

### 9.5. Source of truth

`index.html` — **производная** от `AGENTS.md` и содержимого `tasks/`. Редактировать напрямую нельзя — только перегенерировать из источников. Если в dashboard расхождение с реальностью — починить источник (AGENTS.md или task-файл), потом перегенерировать.

---

## 10. Что НЕ делать

- ❌ **Не класть** код проектов в `hq/` — он живёт по пути из карточки.
- ❌ **Не дублировать** информацию о проектах вне этого файла — реестр и карточки только здесь.
- ❌ **Не оставлять** завершённые задачи в `long/` или `short/` — переносить в `done/`.
- ❌ **Не путать** короткую и длинную задачу: нужен план → длинная.
- ❌ **Не исполнять** длинные задачи в лоб — делегировать субагентам через раздел 7.
- ❌ **Не редактировать** шаблоны из раздела 5 под конкретную задачу — копировать, переименовывать и менять копию.

---

## 11. OpenClaw агенты

Мультиагентная оркестра на VPS. Каждый агент — Telegram-инстанс с фокусированной ролью. Дирижёр — `main clawd`, делегирует задачи специализированным агентам.

### 11.1 Реестр ролей

| Роль          | Зона ответственности                         | Статус |
|---------------|----------------------------------------------|:------:|
| main clawd    | дирижёр, общий контроль                      |   ●    |
| sitebuilder   | сайт instrumentburg.ru (SEO)                 |   ●    |
| master        | мастер-агент категорий                       |   ●    |
| marketer      | Метрика, Wordstat, Direct                    |   ●    |
| advertiser    | Avito, Direct-объявления                     |   ●    |
| chaser        | заказы Ozon / WB                             |   ●    |
| mailer        | рассылки клиентам                            |   ●    |
| dispatcher    | маршрутизация сообщений                      |   ●    |
| finik         | финансовый ассистент                         |   ◐    |
| nutritionist  | личный (вне ИБ)                              |   ◐    |

Легенда: ● active · ◐ partial · ○ paused.

### 11.2 Правила

- Таблица выше — **source of truth** для секции `§ III · Оркестра` в `hq/index.html`.
- Telegram @handle конкретных ботов **не публикуем** (см. §9.3) — только имена ролей.
- При добавлении / удалении агента — править таблицу выше, потом перегенерировать dashboard.
- Workspace каждого агента — `~/.openclaw/workspace-<роль>/` (локально, не публикуется).
