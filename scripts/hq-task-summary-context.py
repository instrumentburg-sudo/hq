#!/usr/bin/env python3
"""Collect compact, read-only HQ context for the daily Telegram summary."""

from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable


DEFAULT_GITHUB_OWNER = "instrumentburg-sudo"
DEFAULT_GITHUB_PROJECT_NUMBER = "1"
DEFAULT_HQ_ROOT = Path("/home/iamsohappy/projects/Githab/hq")
DEFAULT_CRM_ROOT = Path("/home/iamsohappy/projects/Githab/crm")
MAX_SECTION_CHARS = 520
MAX_TASKS_PER_GROUP = 20
MAX_DONE = 5
MAX_PROJECT_ITEMS = 8

STATUS_LABELS = {
    "in_progress": "в работе",
    "blocked": "заблокирована",
    "pending": "ждет старта",
    "completed": "закрыта",
    "done": "закрыта",
}

PROJECT_STATUS_LABELS = {
    "In Progress": "в работе",
    "This Week": "на этой неделе",
    "Backlog": "в очереди",
    "Done": "закрыто",
    "NO_STATUS": "без статуса",
}

FIELD_LABELS = {
    "priority": "приоритет",
    "status": "статус",
    "project": "проект",
    "deadline": "срок",
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(bearer|basic)\s+[a-z0-9._~+/=-]{16,}"),
    re.compile(r"(?i)(token|api[_-]?key|password|secret)\s*[:=]\s*['\"]?[^'\"\s`]+"),
]

DONE_STATUSES = {"completed", "done", "archived"}
CRM_TEMPLATE_PARTS = {"_templates"}
CRM_CARD_DIRS = ("10_Accounts", "20_People", "30_Opportunities")
ACTIVE_CRM_STATUSES = {"active", "idea", "verbal_yes", "negotiation", "confirmed"}


def redact(text: str) -> str:
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub(lambda m: f"{m.group(1)} [REDACTED]", result)
    return result


def truncate(text: str, limit: int = MAX_SECTION_CHARS) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip()
    return f"{cut}..."


def split_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---", 4)
    if end == -1:
        return {}, raw
    block = raw[4:end].strip()
    body = raw[end + 4 :].lstrip()
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip("\"'")
        if value in {"[]", "{}", "null", "None"}:
            value = ""
        meta[key.strip()] = value
    return meta, body


def extract_title(body: str, path: Path) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ")


def extract_section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    if not match:
        return ""
    return truncate(match.group("body"))


def extract_checklist(body: str) -> list[str]:
    items: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]") or stripped.startswith("- [x]"):
            items.append(stripped)
    return items[:8]


def parse_date(value: str) -> dt.date | None:
    value = str(value or "").strip().strip('"\'')
    if not value or value in {"—", "-", "TBD", "todo"}:
        return None
    for pattern in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return dt.datetime.strptime(value[:10], pattern).date()
        except ValueError:
            pass
    return None


def read_task(path: Path, root: Path) -> dict[str, object]:
    raw = redact(path.read_text(encoding="utf-8", errors="replace"))
    meta, body = split_frontmatter(raw)
    return {
        "path": str(path.relative_to(root)),
        "title": extract_title(body, path),
        "type": meta.get("type", ""),
        "status": meta.get("status", ""),
        "project": meta.get("project", ""),
        "priority": meta.get("priority", ""),
        "created": meta.get("created", ""),
        "completed": meta.get("completed", ""),
        "deadline": meta.get("deadline", ""),
        "goal": extract_section(body, "Цель"),
        "context": extract_section(body, "Контекст"),
        "plan": extract_checklist(body),
    }


def sort_key(task: dict[str, object]) -> tuple[int, str, str]:
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    priority = str(task.get("priority") or "")
    created = str(task.get("created") or "")
    return priority_order.get(priority, 9), created, str(task.get("title") or "")


def render_task(task: dict[str, object]) -> list[str]:
    meta = []
    for key in ("priority", "status", "project", "deadline"):
        value = str(task.get(key) or "")
        if value:
            label = FIELD_LABELS.get(key, key)
            if key == "status":
                value = STATUS_LABELS.get(value, value)
            meta.append(f"{label}: {value}")

    lines = [f"- {task['title']}"]
    if meta:
        lines.append(f"  Данные: {', '.join(meta)}")
    if task.get("goal"):
        lines.append(f"  Цель: {task['goal']}")
    elif task.get("context"):
        lines.append(f"  Суть: {task['context']}")
    plan = task.get("plan") or []
    if plan:
        lines.append("  Шаги:")
        for item in plan:
            lines.append(f"    {item}")
    lines.append(f"  Файл: {task['path']}")
    return lines


def render_group(title: str, tasks: Iterable[dict[str, object]]) -> list[str]:
    task_list = list(tasks)
    lines = [f"## {title}", ""]
    if not task_list:
        lines.extend(["Нет задач.", ""])
        return lines
    for task in task_list[:MAX_TASKS_PER_GROUP]:
        lines.extend(render_task(task))
        lines.append("")
    if len(task_list) > MAX_TASKS_PER_GROUP:
        lines.append(f"…и еще {len(task_list) - MAX_TASKS_PER_GROUP}.")
        lines.append("")
    return lines


def run_command(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "timeout"
    return completed.returncode, completed.stdout, completed.stderr


def item_title(item: dict[str, object]) -> str:
    content = item.get("content") if isinstance(item.get("content"), dict) else {}
    return str(item.get("title") or content.get("title") or "Без названия")


def item_ref(item: dict[str, object]) -> str:
    content = item.get("content") if isinstance(item.get("content"), dict) else {}
    repo = str(content.get("repository") or item.get("repository") or "").replace(
        "instrumentburg-sudo/", ""
    )
    number = content.get("number")
    if repo and number:
        return f"{repo}#{number}"
    if repo:
        return repo
    return "черновик"


def item_url(item: dict[str, object]) -> str:
    content = item.get("content") if isinstance(item.get("content"), dict) else {}
    return str(content.get("url") or "")


def collect_github_project(hq_root: Path) -> tuple[list[str], dict[str, object]]:
    owner = os.environ.get("HQ_GITHUB_OWNER", DEFAULT_GITHUB_OWNER)
    project_number = os.environ.get("HQ_GITHUB_PROJECT_NUMBER", DEFAULT_GITHUB_PROJECT_NUMBER)
    code, stdout, stderr = run_command(
        [
            "gh",
            "project",
            "item-list",
            project_number,
            "--owner",
            owner,
            "--limit",
            "200",
            "--format",
            "json",
        ],
        cwd=hq_root,
    )
    lines = ["## GitHub-проект «Антон — Всё»", ""]
    state: dict[str, object] = {"ok": False, "active_count": 0, "this_week_count": 0}
    if code != 0:
        message = truncate((stderr or stdout or "unknown error").strip(), 360)
        lines.extend([f"Не прочитан: {message}", ""])
        state["error"] = message
        return lines, state

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        lines.extend([f"Не прочитан: GitHub вернул не JSON ({exc}).", ""])
        state["error"] = str(exc)
        return lines, state

    items = data.get("items", []) if isinstance(data, dict) else []
    counts = collections.Counter(str(item.get("status") or "NO_STATUS") for item in items)
    active_items = [item for item in items if str(item.get("status") or "") != "Done"]
    in_progress = [item for item in items if item.get("status") == "In Progress"]
    this_week = [item for item in items if item.get("status") == "This Week"]
    queue = [item for item in items if item.get("status") == "Backlog"]

    state.update(
        {
            "ok": True,
            "total": len(items),
            "open_count": len(active_items),
            "work_count": len(in_progress) + len(this_week),
            "in_progress_count": len(in_progress),
            "this_week_count": len(this_week),
            "queue_count": len(queue),
        }
    )

    lines.append(f"Всего пунктов: {len(items)}.")
    if counts:
        rendered_counts = []
        for status, count in counts.most_common():
            rendered_counts.append(f"{PROJECT_STATUS_LABELS.get(status, status)}: {count}")
        lines.append(f"Разбивка: {', '.join(rendered_counts)}.")
    lines.append("")

    def render_items(title: str, selected: list[dict[str, object]]) -> None:
        lines.append(f"### {title}")
        if not selected:
            lines.extend(["Нет.", ""])
            return
        for item in selected[:MAX_PROJECT_ITEMS]:
            status = PROJECT_STATUS_LABELS.get(str(item.get("status") or "NO_STATUS"), str(item.get("status") or ""))
            url = item_url(item)
            suffix = f" — {url}" if url else ""
            lines.append(f"- {item_ref(item)} — {item_title(item)}; статус: {status}{suffix}")
        if len(selected) > MAX_PROJECT_ITEMS:
            lines.append(f"…и еще {len(selected) - MAX_PROJECT_ITEMS}.")
        lines.append("")

    render_items("В работе", in_progress)
    render_items("На этой неделе", this_week)
    if queue:
        render_items("В очереди, не тащить в день без решения Антона", queue[:MAX_PROJECT_ITEMS])

    return lines, state


def read_crm_card(path: Path, root: Path) -> dict[str, object]:
    raw = redact(path.read_text(encoding="utf-8", errors="replace"))
    meta, body = split_frontmatter(raw)
    return {
        "path": str(path.relative_to(root)),
        "title": meta.get("name") or meta.get("title") or extract_title(body, path),
        "status": meta.get("status", ""),
        "stage": meta.get("stage", ""),
        "next_step": meta.get("next_step", ""),
        "next_step_date": meta.get("next_step_date", ""),
        "last_touch": meta.get("last_touch", ""),
        "account": meta.get("account", ""),
        "telegram": meta.get("telegram", ""),
    }


def crm_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for directory in CRM_CARD_DIRS:
        base = root / directory
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if any(part in CRM_TEMPLATE_PARTS for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def collect_crm(root: Path, today: dt.date) -> tuple[list[str], dict[str, object]]:
    lines = ["## CRM: люди, встречи, сделки", ""]
    state: dict[str, object] = {"ok": root.exists(), "cards": 0, "due_count": 0}
    if not root.exists():
        lines.extend([f"Папка не найдена: {root}", ""])
        return lines, state

    files = crm_markdown_files(root)
    cards = [read_crm_card(path, root) for path in files]
    due: list[dict[str, object]] = []
    stale: list[dict[str, object]] = []
    active_opportunities: list[dict[str, object]] = []

    for card in cards:
        due_date = parse_date(str(card.get("next_step_date") or ""))
        if due_date and due_date <= today:
            due.append(card)
        last_touch = parse_date(str(card.get("last_touch") or ""))
        if last_touch and (today - last_touch).days >= 21:
            stale.append(card)
        path = str(card.get("path") or "")
        status = str(card.get("status") or "").lower()
        stage = str(card.get("stage") or "").lower()
        if path.startswith("30_Opportunities/") and (status in ACTIVE_CRM_STATUSES or stage in ACTIVE_CRM_STATUSES):
            active_opportunities.append(card)

    state.update({"cards": len(cards), "due_count": len(due), "stale_count": len(stale), "active_opportunities": len(active_opportunities)})

    if not cards:
        lines.extend(
            [
                "Скаффолд есть, живых карточек нет.",
                "Минимальный следующий шаг: завести 1 реальный контакт и 1 встречу из урока 3, иначе CRM не участвует в управлении.",
                "",
            ]
        )
        return lines, state

    lines.append(f"Карточек: {len(cards)}; шаги на сегодня/просроченные: {len(due)}; сделки в работе: {len(active_opportunities)}; давно без касания: {len(stale)}.")
    lines.append("")

    def render_cards(title: str, selected: list[dict[str, object]]) -> None:
        lines.append(f"### {title}")
        if not selected:
            lines.extend(["Нет.", ""])
            return
        for card in selected[:MAX_PROJECT_ITEMS]:
            bits = []
            if card.get("next_step"):
                bits.append(f"следующий шаг: {card['next_step']}")
            if card.get("next_step_date"):
                bits.append(f"дата: {card['next_step_date']}")
            if card.get("status"):
                bits.append(f"статус: {card['status']}")
            lines.append(f"- {card['title']} — {', '.join(bits) if bits else 'без заполненных полей'}; файл: {card['path']}")
        if len(selected) > MAX_PROJECT_ITEMS:
            lines.append(f"…и еще {len(selected) - MAX_PROJECT_ITEMS}.")
        lines.append("")

    render_cards("Нужно действие", due)
    render_cards("Сделки в работе", active_opportunities)
    render_cards("Давно без касания", stale)
    return lines, state


def latest_markdown(directory: Path) -> Path | None:
    if not directory.exists():
        return None
    files = sorted(directory.glob("*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    return files[0] if files else None


def extract_numbered_focus(path: Path, root: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"## Итоговое решение\s*(?P<body>.*?)(?=^##\s+|\Z)", raw, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    lines: list[str] = []
    for line in match.group("body").splitlines():
        stripped = line.strip()
        if re.match(r"^\d+\.\s+", stripped):
            cleaned = re.sub(r"^\d+\.\s+", "", stripped)
            lines.append(f"- {cleaned}")
    return lines[:6]


def collect_week_context(hq_root: Path, today: dt.date) -> list[str]:
    year, week, _ = today.isocalendar()
    week_id = f"W{week:02d}"
    retro_path = hq_root / "docs" / "retro" / f"{week_id}.md"
    plan_path = hq_root / "docs" / "planning" / f"{week_id}-outcomes.md"
    priority_path = latest_markdown(hq_root / "priorities")

    lines = ["## Недельный разбор и план", ""]
    lines.append(f"Текущая неделя: {year}-{week_id}.")
    lines.append(f"Разбор недели: {'есть' if retro_path.exists() else 'нет'} — {retro_path.relative_to(hq_root)}.")
    lines.append(f"План недели: {'есть' if plan_path.exists() else 'нет'} — {plan_path.relative_to(hq_root)}.")
    if priority_path:
        lines.append(f"Последняя приоритизация: {priority_path.relative_to(hq_root)}.")
        focus = extract_numbered_focus(priority_path, hq_root)
        if focus:
            lines.append("Фокус из приоритизации:")
            lines.extend(focus)
    else:
        lines.append("Приоритизация не найдена.")
    lines.append("")
    return lines


def main() -> int:
    hq_root = Path(os.environ.get("HQ_ROOT", DEFAULT_HQ_ROOT)).expanduser().resolve()
    crm_root = Path(os.environ.get("CRM_ROOT", DEFAULT_CRM_ROOT)).expanduser().resolve()
    tasks_root = hq_root / "tasks"
    if not tasks_root.exists():
        raise SystemExit(f"Tasks directory not found: {tasks_root}")

    task_files = sorted(tasks_root.glob("*/*.md"))
    tasks = [read_task(path, hq_root) for path in task_files]

    active = [
        task
        for task in tasks
        if str(task.get("status") or "").lower() not in DONE_STATUSES
    ]
    done = [
        task
        for task in tasks
        if str(task.get("status") or "").lower() in {"completed", "done"}
    ]

    blocked = sorted(
        [task for task in active if str(task.get("status") or "").lower() == "blocked"],
        key=sort_key,
    )
    in_progress = sorted(
        [task for task in active if str(task.get("status") or "").lower() == "in_progress"],
        key=sort_key,
    )
    pending = sorted(
        [task for task in active if str(task.get("status") or "").lower() == "pending"],
        key=sort_key,
    )
    recent_done = sorted(
        done,
        key=lambda task: (
            str(task.get("completed") or task.get("created") or ""),
            str(task.get("title") or ""),
        ),
        reverse=True,
    )[:MAX_DONE]

    now = dt.datetime.now(dt.UTC)
    today = now.date()
    project_lines, project_state = collect_github_project(hq_root)
    crm_lines, crm_state = collect_crm(crm_root, today)

    lines = [
        "# Контекст утренней сводки штаба",
        "",
        f"Сформировано: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Штаб: {hq_root}",
        f"CRM: {crm_root}",
        "",
        "## Главное расхождение",
        "",
    ]

    project_open = int(project_state.get("open_count") or 0)
    project_work = int(project_state.get("work_count") or 0)
    project_queue = int(project_state.get("queue_count") or 0)
    if project_state.get("ok") and not active and project_open:
        lines.extend(
            [
                f"Локальные задачи штаба показывают 0 активных, но в GitHub-проекте есть {project_work} пунктов в работе/на неделе и {project_queue} в очереди.",
                "В пользовательской сводке не писать «задач нет» без этого уточнения.",
                "",
            ]
        )
    else:
        lines.extend(["Критичного расхождения источников не найдено.", ""])

    lines.extend(project_lines)
    lines.extend(crm_lines)
    lines.extend(collect_week_context(hq_root, today))

    lines.extend(
        [
            "## Локальные задачи штаба",
            "",
            f"Активных: {len(active)}; в работе: {len(in_progress)}; заблокировано: {len(blocked)}; ждут старта: {len(pending)}; недавно закрытых в справке: {len(recent_done)}.",
            "",
        ]
    )
    lines.extend(render_group("В работе", in_progress))
    lines.extend(render_group("Заблокировано", blocked))
    lines.extend(render_group("Ждут старта", pending))
    lines.extend(render_group("Недавно закрыто", recent_done))

    lines.extend(
        [
            "## Правила для итоговой Telegram-сводки",
            "",
            "- Писать по-русски и по делу, без лишних англицизмов.",
            "- Сначала вывод: что требует внимания сегодня.",
            "- Не предлагать читать Telegram-историю без отдельного разрешения и белого списка чатов.",
            "- Если CRM пустая — так и написать, без имитации работы.",
            "- Очередь не выдавать за задачу дня: брать только после решения Антона.",
        ]
    )

    print("\n".join(lines).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
