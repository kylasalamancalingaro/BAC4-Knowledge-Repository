#!/usr/bin/env python3
"""
BA Agent (local, Ollama-backed)

Features:
- Summarize meeting notes
- Extract key decisions
- Extract business requirements
- Draft BRD updates from notes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
from pathlib import Path
from urllib import error, request

from kanban_manager import KanbanBoard


DEFAULT_MODEL = "llama3.1"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_WIKI_ROOT = (
    "c:/Users/kyla.salamanca/OneDrive - Lingaro Sp. z o. o/Compass/GCP/Global-Clients.wiki"
)


def read_text_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8")


def write_text_file(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


def _score_doc(query_tokens: set[str], content: str, name: str) -> int:
    doc_tokens = _tokenize(name) | _tokenize(content[:4000])
    return len(query_tokens & doc_tokens)


def load_wiki_context(
    wiki_root: str,
    query_text: str,
    *,
    top_k: int = 5,
    max_chars_per_doc: int = 3500,
    max_total_chars: int = 14000,
) -> str:
    root = Path(wiki_root)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Wiki root not found or not a directory: {wiki_root}")

    query_tokens = _tokenize(query_text)
    if not query_tokens:
        query_tokens = {"business", "requirement", "meeting", "decision"}

    candidates: list[tuple[int, Path, str]] = []
    for md_file in root.rglob("*.md"):
        if any(part.startswith(".") for part in md_file.parts):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001
            continue
        score = _score_doc(query_tokens, text, md_file.name)
        if score > 0:
            candidates.append((score, md_file, text))

    candidates.sort(key=lambda x: x[0], reverse=True)
    selected = candidates[:top_k]

    if not selected:
        return ""

    parts: list[str] = [
        "Knowledge source: Global-Clients.wiki repository.",
        "Use this context as organizational source-of-truth where relevant.",
    ]
    total = 0
    for score, path, text in selected:
        rel = path.relative_to(root).as_posix()
        snippet = text[:max_chars_per_doc].strip()
        block = f"\n\n## Wiki Document: {rel} (score={score})\n{snippet}"
        if total + len(block) > max_total_chars:
            break
        parts.append(block)
        total += len(block)

    return "\n".join(parts).strip()


class OllamaClient:
    def __init__(self, model: str = DEFAULT_MODEL, url: str = DEFAULT_OLLAMA_URL):
        self.model = model
        self.url = url

    def generate(self, prompt: str, system: str) -> str:
        payload = {
            "model": self.model,
            "system": system,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }

        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=240) as resp:
                raw = resp.read().decode("utf-8")
                obj = json.loads(raw)
                return obj.get("response", "").strip()
        except error.URLError as e:
            raise RuntimeError(
                "Could not connect to Ollama. Ensure Ollama is installed, running, and available at "
                f"{self.url}. Underlying error: {e}"
            ) from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response from Ollama: {e}") from e


SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a senior Business Analyst copilot.
    Produce clear, structured, actionable outputs.
    Be faithful to source notes; do not invent facts.
    If something is unclear, explicitly state assumptions/questions.
    Use concise professional language.
    """
).strip()


def summarize_prompt(notes: str) -> str:
    return textwrap.dedent(
        f"""
        Task: Summarize the meeting notes.

        Output format:
        1) Executive Summary (5-8 bullets)
        2) Detailed Summary (grouped by topic)
        3) Open Questions / Risks
        4) Action Items (Owner, Action, Due Date if available)

        Notes:
        {notes}
        """
    ).strip()


def decisions_prompt(notes: str) -> str:
    return textwrap.dedent(
        f"""
        Task: Extract key decisions and decision-ready items from the notes.

        Output format:
        1) Confirmed Decisions Table:
           - Decision ID (DEC-001...)
           - Decision Statement
           - Rationale
           - Impacted Areas
           - Owner
           - Date (if known)
        2) Pending Decisions:
           - Decision Topic
           - Options Discussed
           - Required Inputs
           - Decision Owner
           - Target Date

        Notes:
        {notes}
        """
    ).strip()


def requirements_prompt(notes: str) -> str:
    return textwrap.dedent(
        f"""
        Task: Extract and structure business requirements from the notes.

        Output format:
        1) Functional Requirements (FR-001...)
           - Requirement
           - Priority (MoSCoW if inferable)
           - Source Evidence (quote/paraphrase)
           - Acceptance Criteria (Given/When/Then)
        2) Non-Functional Requirements (NFR-001...)
        3) Data Requirements
        4) Reporting / KPI Requirements
        5) Dependencies & Constraints
        6) Gaps / Clarifications Needed

        Notes:
        {notes}
        """
    ).strip()


def brd_update_prompt(brd: str, notes: str) -> str:
    return textwrap.dedent(
        f"""
        Task: Update the BRD draft based on recent meeting notes.

        Instructions:
        - Keep existing BRD structure where possible.
        - Add or revise sections for scope, requirements, assumptions, decisions, risks, and next steps.
        - Keep a section named "Change Log (AI Draft)" with bullet list of what was changed.
        - Do not remove valid existing content unless contradicted by new notes.
        - Mark uncertain additions with [TO VALIDATE].

        Existing BRD:
        {brd}

        New Notes:
        {notes}
        """
    ).strip()


def run_task(client: OllamaClient, task: str, notes: str, brd: str | None = None) -> str:
    wiki_context = load_wiki_context(
        os.getenv("BA_AGENT_WIKI_ROOT", DEFAULT_WIKI_ROOT),
        query_text=notes,
    )
    if wiki_context:
        notes = f"{wiki_context}\n\n---\n\nUser Notes:\n{notes}"

    if task == "summarize":
        return client.generate(summarize_prompt(notes), SYSTEM_PROMPT)
    if task == "decisions":
        return client.generate(decisions_prompt(notes), SYSTEM_PROMPT)
    if task == "requirements":
        return client.generate(requirements_prompt(notes), SYSTEM_PROMPT)
    if task == "update-brd":
        if brd is None:
            raise ValueError("BRD content is required for update-brd task")
        return client.generate(brd_update_prompt(brd, notes), SYSTEM_PROMPT)
    if task == "all":
        parts = [
            "# Meeting Summary\n" + client.generate(summarize_prompt(notes), SYSTEM_PROMPT),
            "# Key Decisions\n" + client.generate(decisions_prompt(notes), SYSTEM_PROMPT),
            "# Requirements\n" + client.generate(requirements_prompt(notes), SYSTEM_PROMPT),
        ]
        return "\n\n".join(parts)
    raise ValueError(f"Unsupported task: {task}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local Business Analyst agent powered by Ollama"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Analysis commands (original functionality)
    analysis_parser = subparsers.add_parser("analyze", help="Analyze meeting notes")
    analysis_parser.add_argument(
        "task",
        choices=["summarize", "decisions", "requirements", "update-brd", "all"],
        help="BA task to run",
    )
    analysis_parser.add_argument("--input", required=True, help="Path to meeting notes (.txt/.md)")
    analysis_parser.add_argument(
        "--brd", help="Path to existing BRD file (required for update-brd task)"
    )
    analysis_parser.add_argument(
        "--output",
        help="Output file path. If omitted, result is printed to console.",
    )
    analysis_parser.add_argument(
        "--model",
        default=os.getenv("BA_AGENT_MODEL", DEFAULT_MODEL),
        help=f"Ollama model name (default: {DEFAULT_MODEL})",
    )
    analysis_parser.add_argument(
        "--url",
        default=os.getenv("BA_AGENT_OLLAMA_URL", DEFAULT_OLLAMA_URL),
        help=f"Ollama API URL (default: {DEFAULT_OLLAMA_URL})",
    )
    analysis_parser.add_argument(
        "--wiki-root",
        default=os.getenv("BA_AGENT_WIKI_ROOT", DEFAULT_WIKI_ROOT),
        help=(
            "Path to the Global-Clients.wiki repository used as background knowledge "
            f"(default: {DEFAULT_WIKI_ROOT})"
        ),
    )

    # Kanban commands (new functionality)
    subparsers.add_parser("today", help="Show today's to-do list")

    subparsers.add_parser("board", help="Show full kanban board")

    summary_parser = subparsers.add_parser("add-summary", help="Add daily summary")
    summary_parser.add_argument("--did", required=True, help="What I did today")
    summary_parser.add_argument("--need", required=True, help="What I need to do")

    task_parser = subparsers.add_parser("add-task", help="Add a new task")
    task_parser.add_argument("title", help="Task title")
    task_parser.add_argument("--description", default="", help="Task description")
    task_parser.add_argument(
        "--status",
        choices=["backlog", "todo", "in_progress", "done"],
        default="backlog",
        help="Task status (default: backlog)",
    )
    task_parser.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="Task priority (default: medium)",
    )
    task_parser.add_argument("--tags", nargs="*", default=[], help="Task tags")

    update_parser = subparsers.add_parser("update-task", help="Update task status")
    update_parser.add_argument("task_id", help="Task ID (e.g., TASK-001)")
    update_parser.add_argument(
        "status",
        choices=["backlog", "todo", "in_progress", "done"],
        help="New status",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        # Kanban commands
        if args.command == "today":
            board = KanbanBoard()
            print(board.format_today())
            return 0

        if args.command == "board":
            board = KanbanBoard()
            print(board.format_board())
            return 0

        if args.command == "add-summary":
            board = KanbanBoard()
            board.add_daily_summary(args.did, args.need)
            print("✅ Daily summary added!")
            print("\nYour updated to-do list:")
            print(board.format_today())
            return 0

        if args.command == "add-task":
            board = KanbanBoard()
            task = board.add_task(
                args.title,
                args.description,
                args.status,  # type: ignore
                args.priority,
                args.tags,
            )
            print(f"✅ Task added: {task.task_id} - {task.title}")
            return 0

        if args.command == "update-task":
            board = KanbanBoard()
            task = board.update_task_status(args.task_id, args.status)  # type: ignore
            if task:
                print(f"✅ Task updated: {task.task_id} → {args.status.upper()}")
            else:
                print(f"❌ Task not found: {args.task_id}")
                return 1
            return 0

        # Analysis commands (original functionality)
        if args.command == "analyze":
            notes = read_text_file(args.input)
            brd = read_text_file(args.brd) if hasattr(args, 'brd') and args.brd else None

            if args.task == "update-brd" and not brd:
                parser.error("--brd is required when task is 'update-brd'")

            os.environ["BA_AGENT_WIKI_ROOT"] = args.wiki_root

            client = OllamaClient(model=args.model, url=args.url)
            result = run_task(client, args.task, notes=notes, brd=brd)

            if args.output:
                write_text_file(args.output, result)
                print(f"Output written to: {args.output}")
            else:
                print(result)

            return 0

        # No command specified
        parser.print_help()
        return 1

    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
