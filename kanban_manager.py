#!/usr/bin/env python3
"""
Personal Kanban Board Manager for BA Agent
Stores tasks in a markdown file (kanban.md)
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Literal

# Type aliases
TaskStatus = Literal["backlog", "todo", "in_progress", "done"]

# Default kanban file location
KANBAN_FILE = Path(__file__).parent / "kanban.md"


class Task:
    """Represents a single task on the kanban board"""

    def __init__(
        self,
        task_id: str,
        title: str,
        description: str = "",
        status: TaskStatus = "backlog",
        priority: str = "medium",
        created_date: str | None = None,
        updated_date: str | None = None,
        completed_date: str | None = None,
        tags: list[str] | None = None,
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d")
        self.updated_date = updated_date or datetime.now().strftime("%Y-%m-%d")
        self.completed_date = completed_date
        self.tags = tags or []

    def __repr__(self) -> str:
        return f"Task({self.task_id}: {self.title} [{self.status}])"


class KanbanBoard:
    """Manages the kanban board in markdown format"""

    def __init__(self, kanban_file: Path = KANBAN_FILE):
        self.kanban_file = kanban_file
        self.tasks: list[Task] = []
        self.daily_summaries: list[dict] = []
        self.load()

    def load(self) -> None:
        """Load kanban board from markdown file"""
        if not self.kanban_file.exists():
            self.save()  # Create empty board
            return

        content = self.kanban_file.read_text(encoding="utf-8")
        self.tasks = []
        self.daily_summaries = []

        # Parse tasks from each section
        current_status: TaskStatus | None = None
        current_task: Task | None = None

        for line in content.split("\n"):
            # Detect section headers
            if line.startswith("## 🗂️ Backlog"):
                current_status = "backlog"
                continue
            elif line.startswith("## 📋 To Do"):
                current_status = "todo"
                continue
            elif line.startswith("## 🔄 In Progress"):
                current_status = "in_progress"
                continue
            elif line.startswith("## ✅ Done"):
                current_status = "done"
                continue
            elif line.startswith("## 📝 Daily Summaries"):
                current_status = None
                continue

            # Parse task line: - [ ] or - [x] **[TASK-001]** Title (Priority: High) #tag1 #tag2
            task_match = re.match(
                r"^- \[([ x])\] \*\*\[([^\]]+)\]\*\* (.+?)(?:\s+\(Priority: (\w+)\))?(?:\s+(#\S+(?:\s+#\S+)*))?$",
                line,
            )
            if task_match and current_status:
                checked = task_match.group(1) == "x"
                task_id = task_match.group(2)
                title = task_match.group(3)
                priority = task_match.group(4) or "medium"
                tags_str = task_match.group(5) or ""
                tags = [t.strip("#") for t in tags_str.split() if t.startswith("#")]

                current_task = Task(
                    task_id=task_id,
                    title=title,
                    status=current_status,
                    priority=priority.lower(),
                    tags=tags,
                )
                self.tasks.append(current_task)
                continue

            # Parse task description/metadata
            if current_task and line.strip().startswith("- "):
                desc_line = line.strip()[2:].strip()
                if desc_line.startswith("Created:"):
                    current_task.created_date = desc_line.replace("Created:", "").strip()
                elif desc_line.startswith("Updated:"):
                    current_task.updated_date = desc_line.replace("Updated:", "").strip()
                elif desc_line.startswith("Completed:"):
                    current_task.completed_date = desc_line.replace("Completed:", "").strip()
                elif not desc_line.startswith("Created:") and not desc_line.startswith("Updated:"):
                    if current_task.description:
                        current_task.description += "\n" + desc_line
                    else:
                        current_task.description = desc_line

            # Parse daily summaries
            summary_date_match = re.match(r"^### (\d{4}-\d{2}-\d{2})$", line)
            if summary_date_match:
                summary_date = summary_date_match.group(1)
                # Look for the next lines with What I did and What I need to do
                # This is a simplified parser - in practice you'd need to read ahead
                continue

    def save(self) -> None:
        """Save kanban board to markdown file"""
        lines = [
            "# 📊 Personal Kanban Board",
            "",
            f"_Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
            "",
            "---",
            "",
        ]

        # Backlog section
        lines.append("## 🗂️ Backlog")
        lines.append("")
        backlog_tasks = [t for t in self.tasks if t.status == "backlog"]
        if not backlog_tasks:
            lines.append("_No tasks in backlog_")
        else:
            for task in backlog_tasks:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # To Do section
        lines.append("## 📋 To Do")
        lines.append("")
        todo_tasks = [t for t in self.tasks if t.status == "todo"]
        if not todo_tasks:
            lines.append("_No tasks to do_")
        else:
            for task in todo_tasks:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # In Progress section
        lines.append("## 🔄 In Progress")
        lines.append("")
        in_progress_tasks = [t for t in self.tasks if t.status == "in_progress"]
        if not in_progress_tasks:
            lines.append("_No tasks in progress_")
        else:
            for task in in_progress_tasks:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # Done section
        lines.append("## ✅ Done")
        lines.append("")
        done_tasks = [t for t in self.tasks if t.status == "done"]
        if not done_tasks:
            lines.append("_No completed tasks_")
        else:
            # Show most recent completed tasks first
            for task in sorted(done_tasks, key=lambda t: t.updated_date, reverse=True)[:20]:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # Daily Summaries section
        lines.append("---")
        lines.append("")
        lines.append("## 📝 Daily Summaries")
        lines.append("")
        if not self.daily_summaries:
            lines.append("_No daily summaries yet_")
        else:
            # Show most recent summaries first
            for summary in reversed(self.daily_summaries[-10:]):
                date = summary["date"]
                if "T" in date:
                    date = date.split("T")[0]
                lines.append(f"### {date}")
                lines.append("")
                lines.append(f"**What I did:** {summary['what_i_did']}")
                lines.append("")
                lines.append(f"**What I need to do:** {summary['what_i_need_to_do']}")
                lines.append("")

        self.kanban_file.write_text("\n".join(lines), encoding="utf-8")

    def _format_task_markdown(self, task: Task) -> list[str]:
        """Format a task as markdown lines"""
        lines = []

        # Checkbox and title
        checkbox = "[x]" if task.status == "done" else "[ ]"
        priority_str = f" (Priority: {task.priority.capitalize()})" if task.priority != "medium" else ""
        tags_str = " " + " ".join(f"#{tag}" for tag in task.tags) if task.tags else ""

        lines.append(f"- {checkbox} **[{task.task_id}]** {task.title}{priority_str}{tags_str}")

        # Description
        if task.description:
            for desc_line in task.description.split("\n"):
                lines.append(f"  - {desc_line}")

        # Metadata
        lines.append(f"  - Created: {task.created_date}")
        if task.status == "done" and task.completed_date:
            lines.append(f"  - Completed: {task.completed_date}")

        return lines

    def add_task(
        self,
        title: str,
        description: str = "",
        status: TaskStatus = "backlog",
        priority: str = "medium",
        tags: list[str] | None = None,
    ) -> Task:
        """Add a new task to the board"""
        task_id = f"TASK-{len(self.tasks) + 1:03d}"
        task = Task(task_id, title, description, status, priority, tags=tags)
        self.tasks.append(task)
        self.save()
        return task

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> Task | None:
        """Update task status"""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = new_status
                task.updated_date = datetime.now().strftime("%Y-%m-%d")
                if new_status == "done":
                    task.completed_date = datetime.now().strftime("%Y-%m-%d")
                self.save()
                return task
        return None

    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        """Get all tasks with given status"""
        return [t for t in self.tasks if t.status == status]

    def get_active_tasks(self) -> list[Task]:
        """Get tasks that are todo or in progress"""
        return [t for t in self.tasks if t.status in ["todo", "in_progress"]]

    def add_daily_summary(self, what_i_did: str, what_i_need_to_do: str) -> None:
        """Add a daily summary entry"""
        summary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "what_i_did": what_i_did,
            "what_i_need_to_do": what_i_need_to_do,
        }
        self.daily_summaries.append(summary)
        self.save()

    def get_recent_summaries(self, limit: int = 5) -> list[dict]:
        """Get recent daily summaries"""
        return self.daily_summaries[-limit:]

    def format_board(self) -> str:
        """Format the kanban board as a readable string for terminal"""
        lines = ["=" * 80, "PERSONAL KANBAN BOARD", "=" * 80, ""]

        for status_key, status_display in [
            ("backlog", "🗂️  BACKLOG"),
            ("todo", "📋 TO DO"),
            ("in_progress", "🔄 IN PROGRESS"),
            ("done", "✅ DONE"),
        ]:
            tasks = self.get_tasks_by_status(status_key)  # type: ignore

            lines.append(f"\n## {status_display} ({len(tasks)} tasks)")
            lines.append("-" * 80)

            if not tasks:
                lines.append("  (no tasks)")
            else:
                display_tasks = tasks if status_key != "done" else tasks[-10:]
                for task in display_tasks:
                    priority_marker = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢",
                    }.get(task.priority, "⚪")

                    lines.append(f"\n  {priority_marker} [{task.task_id}] {task.title}")
                    if task.description:
                        for desc_line in task.description.split("\n"):
                            lines.append(f"     {desc_line}")
                    if task.tags:
                        lines.append(f"     Tags: {', '.join(task.tags)}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def format_today(self) -> str:
        """Format today's to-do list"""
        lines = [
            "=" * 80,
            f"TODAY'S TO-DO LIST - {datetime.now().strftime('%A, %B %d, %Y')}",
            "=" * 80,
            "",
        ]

        # In Progress tasks
        in_progress = self.get_tasks_by_status("in_progress")
        if in_progress:
            lines.append("## 🔄 IN PROGRESS")
            lines.append("-" * 80)
            for task in in_progress:
                lines.append(f"  [{task.task_id}] {task.title}")
                if task.description:
                    for desc_line in task.description.split("\n"):
                        lines.append(f"     {desc_line}")
            lines.append("")

        # To Do tasks
        todo = self.get_tasks_by_status("todo")
        if todo:
            lines.append("## 📋 TO DO")
            lines.append("-" * 80)
            for task in todo:
                priority_marker = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(task.priority, "⚪")
                lines.append(f"  {priority_marker} [{task.task_id}] {task.title}")
                if task.description:
                    for desc_line in task.description.split("\n"):
                        lines.append(f"     {desc_line}")
            lines.append("")

        if not in_progress and not todo:
            lines.append("✅ No active tasks! Time to plan your next moves or enjoy some free time.")
            lines.append("")

        # Recent summary
        recent = self.get_recent_summaries(limit=1)
        if recent:
            lines.append("## 📝 LATEST SUMMARY")
            lines.append("-" * 80)
            last = recent[0]
            date = last["date"]
            lines.append(f"Date: {date}")
            lines.append(f"\nWhat I did:")
            lines.append(f"  {last['what_i_did']}")
            lines.append(f"\nWhat I need to do:")
            lines.append(f"  {last['what_i_need_to_do']}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


def main() -> None:
    """Demo usage"""
    import sys

    # Fix Windows console encoding for emojis
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

    board = KanbanBoard()

    # Example: Add some tasks
    board.add_task(
        "Review ADR-008",
        "Review and provide feedback on Standard Report Publication Strategy",
        status="todo",
        priority="high",
        tags=["documentation", "adr"],
    )

    board.add_task(
        "Update GCP delivery gates",
        "Incorporate SA engagement integration feedback",
        status="in_progress",
        priority="medium",
        tags=["gcp", "process"],
    )

    # Add a daily summary
    board.add_daily_summary(
        what_i_did="Reviewed data ownership documentation, attended team sync",
        what_i_need_to_do="Complete ADR review, update delivery gates documentation",
    )

    # Print today's view
    print(board.format_today())
    print("\n")

    # Print full board
    print(board.format_board())


if __name__ == "__main__":
    main()
