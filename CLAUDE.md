# CLAUDE.md

Правила работы в этой папке универсальны для любого агента (Claude, Codex, Gemini и др.).

Единственный источник правды — @AGENTS.md.

Там: назначение папки, структура, workflow, классификация и шаблоны задач, реестр и карточки проектов, правила делегирования субагентам, архив завершённых задач.

## Ris Manager Config

### GitHub owner
- owner: instrumentburg-sudo

### Default GitHub Project
- project_owner: instrumentburg-sudo
- project_number: 1
- project_title: Антон — Всё
- project_url: https://github.com/users/instrumentburg-sudo/projects/1

### Repos to scan
Основной штаб — эта репа:
- /home/iamsohappy/projects/Githab/hq # instrumentburg-sudo/hq

Репозитории из GitHub Project `Антон — Всё`:
- /home/iamsohappy/projects/instrumentburg # instrumentburg-sudo/instrumentburg
- /home/iamsohappy/clawd # instrumentburg-sudo/clawd
- /home/iamsohappy/projects/instrumentburg/apps/website # instrumentburg-sudo/instrumentburg-website
- /home/iamsohappy/projects/Rentalnew # instrumentburg-sudo/toolrent-manager
- /home/iamsohappy/projects/health-tracker # instrumentburg-sudo/health-tracker
- /home/iamsohappy/projects/openclaw-hub # instrumentburg-sudo/openclaw-hub

### Tasks index file
- tasks_index: /home/iamsohappy/projects/Githab/hq/AGENTS.md
- tasks_dir: /home/iamsohappy/projects/Githab/hq/tasks

### Domain → repo routing
| Domain | Repo |
|---|---|
| штаб / orchestration / project tracking | hq |
| ИнструментБург / operations / repair / mail / КП | instrumentburg |
| agents / skills / OpenClaw workspaces | clawd |
| site / SEO / ocStore / instrumentburg.ru | instrumentburg-website |
| rental / calculator / tool rent | toolrent-manager |
| health | health-tracker |
| infra / VPS / OpenClaw hub | openclaw-hub |

### Issue title domains
- product, content, partner, crm, infra, legal, ops, site, marketplace, tender, health, meta, hq

### W-label convention
- enabled: true
- format: W{NN}

### Standing write authorization
- mode: ask-each-time

## Ris Prioritize Config

### Default framework
Если нет количественных данных по reach/impact, использовать быстрый качественный скоринг.
- default_framework: ICE

### Default resource constraint
- sprint_capacity: 20 person-days per Sprint

### Backlog source
- backlog_source: github-project
- gh_owner: instrumentburg-sudo
- github_project_owner: instrumentburg-sudo
- github_project_number: 1
- github_project_title: Антон — Всё
- tasks_file: /home/iamsohappy/projects/Githab/hq/AGENTS.md

## Утренняя сводка

- script_source: /home/iamsohappy/projects/Githab/hq/scripts/hq-task-summary-context.py
- script_cron_link: /home/iamsohappy/.hermes/scripts/hq-task-summary-context.py
- cron_name: daily-hq-task-summary-ekb-1000
- delivery: Telegram Антону
- sources:
  - GitHub Project «Антон — Всё»
  - /home/iamsohappy/projects/Githab/hq/tasks
  - /home/iamsohappy/projects/Githab/crm
  - /home/iamsohappy/projects/Githab/hq/docs/retro
  - /home/iamsohappy/projects/Githab/hq/docs/planning
- style: по-русски, коротко, предпринимательский контекст, минимум англицизмов

## Недельный цикл

### Разбор недели
- path: /home/iamsohappy/projects/Githab/hq/docs/retro/WNN.md
- goal: факт недели, зависшие хвосты, решения Антона, что агент может сделать сам
- write_authorization: draft-only-until-anton-confirms

### План недели
- path: /home/iamsohappy/projects/Githab/hq/docs/planning/WNN-outcomes.md
- goal: 3–7 проверяемых результатов недели
- source_order:
  - последний разбор недели
  - GitHub Project «Антон — Всё»
  - свежая приоритизация в hq/priorities
  - CRM-шаги с датами
- write_authorization: ask-each-time
