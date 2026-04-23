# lesson-pipeline — скилл упаковки уроков Personal Corp

**Статус:** design · **Дата:** 2026-04-23 · **Автор:** Антон + Клод

## Контекст

ДЗ урока 02 Серёжи Риса: упаковать один повторяющийся пайплайн через `Superpowers:Writing Skills`. Кандидат идеален — только что вручную прошли цепочку `transcript → lesson.json → lesson.html → публикация в hq/ → commit+push` второй раз подряд. К уроку 03 не будем копировать руками.

## Scope — C2

Скилл автоматизирует шаги 1-5, `git push` — через Human Gate (урок 02, Серёжа):

1. Прочитать транскрипт из указанного файла
2. Извлечь структуру → `lesson{N}.json`
3. Отрендерить выжимку → `lesson{N}.html`
4. Скопировать в `hq/course/lesson{N}.html` + обновить `hq/index.html` (футер + задача «На очереди»)
5. Обновить `hq/AGENTS.md` карточку personal-corp + memory `project_personal_corp.md`
6. `git add` + `git commit` готовы, **push только после явного «да»** на показанный `git diff --stat`

## Вход

Путь к файлу транскрипта явным аргументом:

```
/lesson-pipeline "personal corp/transcripts/lesson3.txt"
```

Номер урока парсится из имени файла (`lesson3.txt` → 3). Имя — единственный аргумент; `--title=`, `--date=` — optional overrides.

## Архитектура

**Расположение скилла:** `~/.claude/skills/personal-corp/lesson-pipeline/` (глобальный, привязан к HQ Антона)

**Структура папки:**

```
lesson-pipeline/
  SKILL.md                 # инструкции для LLM
  template.html            # зашитый dark-editorial шаблон lesson1 с плейсхолдерами
  render.py                # JSON + template → HTML (Python, без LLM)
  validate.py              # проверка HTML парсится, все 6 блоков JSON не пусты
  prompts/
    extract.md             # промпт извлечения JSON с few-shot ссылками на примеры
  examples/
    lesson1.json           # симлинк или копия реального lesson1.json
    lesson2.json           # симлинк или копия реального lesson2.json
  tests/
    fixtures/
      lesson1.txt          # кусок транскрипта lesson1 для smoke test
    test_render.py         # unit-тест render.py на lesson1.json → ожидаемый HTML
```

**Разделение труда:**
- **LLM делает:** только извлечение JSON из транскрипта по промпту + примерам (шаг 2), генерацию commit-message при необходимости
- **Python делает:** всё остальное — render.py, валидацию, файловые операции, `sed`-правки в `hq/index.html` и `AGENTS.md`, git команды

Смысл — LLM не трогает проверенный CSS/HTML/разметку dashboard, чтобы стиль не дрейфовал от прогона к прогону.

## JSON — извлечение

Метод: **промпт + два примера** (`lesson1.json`, `lesson2.json`), без жёсткой JSON Schema. 6 блоков: `terms` (~10), `methods` (~9), `frameworks` (~7-8), `goals` (~5), `homework` (~5), `quotes` (~5). Cardinalities плавающие — валидируем только «не пусто». В уроке 02 Серёжа прямо ругался на zipped-промпты в JSON Schema — идём по мягкому пути.

## Title

LLM генерирует из транскрипта по few-shot паттерну lesson1/lesson2 (`"HQ — первый шаг к агент-оркестрации"`, `"Масштабирование без оверинженеринга"`). Override: `--title="..."`.

## Defaults

| Поле | Default |
|------|---------|
| ДЗ статусы | все `todo` для нового урока |
| Commit message | `course: lesson{N}.html + dashboard update` |
| Задача на dashboard | первая строка `homework[0].task` нового JSON |
| Дата | `date +%d·%m·%y` + римский формат `II · 23·04·26` |
| Дата override | `--date=` |
| Формат ссылки в футере dashboard | всегда на последний урок (`lesson{N}.html`), текст `курс Personal Corp · {N:02d}` |

## Валидация перед push

`validate.py` проверяет:
1. HTML парсится (`html.parser`)
2. JSON содержит все 6 блоков, ни один не пуст
3. В `hq/course/lesson{N}.html` есть «Личный корп» в rail, `§ I` — `§ IV`, CTA на HQ
4. `hq/index.html` ссылается на свежий `lesson{N}.html`
5. `git status` показывает только ожидаемые изменения

Упала любая проверка → скилл останавливается, не пушит, рапортует какой чек упал.

## Human Gate на push

После commit:
- Показать `git log -1 --stat`
- Показать `git diff HEAD~1 --stat` (сравнение с предыдущим коммитом)
- Написать: «Пушить в main? [да/нет]»
- Только после «да» → `git push origin main`

## Edge cases

- **lesson{N}.* уже существует** → ask «перегенерировать?», не молча перетирать
- **hq/ dirty** (несохранённые изменения вне lesson-pipeline) → стоп, попросить разрулить
- **Транскрипт пустой или < 1 KB** → стоп, наверняка не тот файл
- **Валидация не прошла** → показать какой чек упал, не коммитить

## TDD план (для writing-skills)

1. Зафиксировать текущий `lesson1.txt` как golden fixture
2. Упасть: запустить скилл на lesson1.txt → он должен воспроизвести текущий `lesson1.json` и `lesson1.html` (примерно). Писать скилл итеративно, пока тест не пройдёт.
3. Упасть 2: `lesson2.txt` → текущий `lesson2.json` / `lesson2.html`.
4. Когда оба fixture воспроизводятся — упаковка в `SKILL.md`.

## Открытые вопросы (решим при имплементации)

- Установочный путь — `~/.claude/skills/personal-corp/lesson-pipeline/` (global) vs `hq/.claude/skills/` (привязано к репо). Склоняюсь к global, т.к. скилл знает абсолютные пути `personal corp/` и `hq/`.
- Как «имя файла = номер урока» парсится: regex `lesson(\d+)\.txt` — fine.
- Нужен ли rollback при ошибке после частичного выполнения (уже скопировано в `hq/course/`, но валидация упала).

## Ссылки

- Транскрипт lesson02: `personal corp/transcripts/lesson2.txt`
- Шаблон: `personal corp/lesson1.html` (600 строк CSS + разметка)
- Примеры JSON: `personal corp/lesson1.json`, `personal corp/lesson2.json`
- HQ dashboard: `hq/index.html`, `hq/AGENTS.md`
- Memory: `~/.claude/projects/-home-iamsohappy-projects-Githab/memory/project_personal_corp.md`
