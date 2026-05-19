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
TaskStatus = Literal["todo", "doing", "done"]

# Default kanban file location
KANBAN_FILE = Path(__file__).parent / "kanban.md"


class Task:
    """Represents a single task on the kanban board"""

    def __init__(
        self,
        task_id: str,
        title: str,
        project_name: str = "",
        sprint_item: bool = False,
        details: str = "",
        deadline: str = "",
        status: TaskStatus = "todo",
        created_date: str | None = None,
        updated_date: str | None = None,
        completed_date: str | None = None,
    ):
        self.task_id = task_id
        self.title = title
        self.project_name = project_name
        self.sprint_item = sprint_item
        self.details = details
        self.deadline = deadline
        self.status = status
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d")
        self.updated_date = updated_date or datetime.now().strftime("%Y-%m-%d")
        self.completed_date = completed_date

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

        current_status: TaskStatus | None = None
        current_task: Task | None = None

        for line in content.split("\n"):
            # Detect section headers
            if line.startswith("## 📋 TO-DO"):
                current_status = "todo"
                continue
            elif line.startswith("## 🔄 DOING"):
                current_status = "doing"
                continue
            elif line.startswith("## ✅ DONE"):
                current_status = "done"
                continue
            elif line.startswith("## 📝 Daily Summaries"):
                current_status = None
                continue

            # Parse task line: - [ ] or - [x] **[TASK-001]** Title
            task_match = re.match(r"^- \[([ x])\] \*\*\[([^\]]+)\]\*\* (.+)$", line)
            if task_match and current_status:
                checked = task_match.group(1) == "x"
                task_id = task_match.group(2)
                title = task_match.group(3)

                current_task = Task(
                    task_id=task_id,
                    title=title,
                    status=current_status,
                )
                self.tasks.append(current_task)
                continue

            # Parse task metadata
            if current_task and line.strip().startswith("- "):
                meta_line = line.strip()[2:].strip()
                if meta_line.startswith("**Project:**"):
                    current_task.project_name = meta_line.replace("**Project:**", "").strip()
                elif meta_line.startswith("**Sprint Item:**"):
                    sprint_val = meta_line.replace("**Sprint Item:**", "").strip()
                    current_task.sprint_item = sprint_val.lower() in ["yes", "y", "true"]
                elif meta_line.startswith("**Details:**"):
                    current_task.details = meta_line.replace("**Details:**", "").strip()
                elif meta_line.startswith("**Deadline:**"):
                    current_task.deadline = meta_line.replace("**Deadline:**", "").strip()
                elif meta_line.startswith("**Created:**"):
                    current_task.created_date = meta_line.replace("**Created:**", "").strip()
                elif meta_line.startswith("**Completed:**"):
                    current_task.completed_date = meta_line.replace("**Completed:**", "").strip()

            # Parse daily summaries
            summary_date_match = re.match(r"^### (\d{4}-\d{2}-\d{2})$", line)
            if summary_date_match:
                summary_date = summary_date_match.group(1)
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

        # TO-DO section
        lines.append("## 📋 TO-DO")
        lines.append("")
        todo_tasks = [t for t in self.tasks if t.status == "todo"]
        if not todo_tasks:
            lines.append("_No tasks in to-do list_")
        else:
            for task in todo_tasks:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # DOING section
        lines.append("## 🔄 DOING")
        lines.append("")
        doing_tasks = [t for t in self.tasks if t.status == "doing"]
        if not doing_tasks:
            lines.append("_No tasks in progress_")
        else:
            for task in doing_tasks:
                lines.extend(self._format_task_markdown(task))
        lines.append("")

        # DONE section
        lines.append("## ✅ DONE")
        lines.append("")
        done_tasks = [t for t in self.tasks if t.status == "done"]
        if not done_tasks:
            lines.append("_No completed tasks_")
        else:
            # Show most recent completed tasks first
            for task in sorted(done_tasks, key=lambda t: t.completed_date or t.updated_date, reverse=True)[:
                30
            ]:
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

        # Checkbox and title (no emoji in markdown, just metadata)
        checkbox = "[x]" if task.status == "done" else "[ ]"
        lines.append(f"- {checkbox} **[{task.task_id}]** {task.title}")

        # Metadata
        if task.project_name:
            lines.append(f"  - **Project:** {task.project_name}")
        lines.append(f"  - **Sprint Item:** {'Yes' if task.sprint_item else 'No'}")
        if task.details:
            lines.append(f"  - **Details:** {task.details}")
        if task.deadline:
            lines.append(f"  - **Deadline:** {task.deadline}")
        lines.append(f"  - **Created:** {task.created_date}")
        if task.status == "done" and task.completed_date:
            lines.append(f"  - **Completed:** {task.completed_date}")

        return lines

    def add_task(
        self,
        title: str,
        project_name: str = "",
        sprint_item: bool = False,
        details: str = "",
        deadline: str = "",
    ) -> Task:
        """Add a new task to the to-do list"""
        task_id = f"TASK-{len(self.tasks) + 1:03d}"
        task = Task(
            task_id=task_id,
            title=title,
            project_name=project_name,
            sprint_item=sprint_item,
            details=details,
            deadline=deadline,
            status="todo",
        )
        self.tasks.append(task)
        self.save()
        return task

    def move_to_doing(self, task_id: str) -> Task | None:
        """Move task from TO-DO to DOING"""
        task = self.get_task(task_id)
        if task and task.status == "todo":
            task.status = "doing"
            task.updated_date = datetime.now().strftime("%Y-%m-%d")
            self.save()
            return task
        return None

    def mark_done(self, task_id: str) -> Task | None:
        """Mark task as DONE"""
        task = self.get_task(task_id)
        if task and task.status in ["todo", "doing"]:
            task.status = "done"
            task.completed_date = datetime.now().strftime("%Y-%m-%d")
            task.updated_date = task.completed_date
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
        """Get tasks that are todo or doing"""
        return [t for t in self.tasks if t.status in ["todo", "doing"]]

    def add_daily_summary(self, what_i_did: str, what_i_need_to_do: str) -> None:
        """Add a daily summary entry"""
        summary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "what_i_did": what_i_did,
            "what_i_need_to_do": what_i_need_to_do,
        }
        self.daily_summaries.append(summary)
        self.save()

    def format_list(self, include_done: bool = False) -> str:
        """Format active tasks (or all tasks if include_done=True)"""
        lines = [
            "=" * 80,
            "TASK LIST",
            "=" * 80,
            "",
        ]

        # DOING section
        doing_tasks = self.get_tasks_by_status("doing")
        lines.append(f"## 🔄 DOING ({len(doing_tasks)} tasks)")
        lines.append("-" * 80)
        if not doing_tasks:
            lines.append("  (no tasks in progress)")
        else:
            for task in doing_tasks:
                lines.extend(self._format_task_display(task))
        lines.append("")

        # TO-DO section
        todo_tasks = self.get_tasks_by_status("todo")
        lines.append(f"## 📋 TO-DO ({len(todo_tasks)} tasks)")
        lines.append("-" * 80)
        if not todo_tasks:
            lines.append("  (no tasks to do)")
        else:
            # Sort by deadline (tasks with deadline first, then by date)
            sorted_todo = sorted(
                todo_tasks,
                key=lambda t: (t.deadline == "", t.deadline if t.deadline else "9999-99-99"),
            )
            for task in sorted_todo:
                lines.extend(self._format_task_display(task))
        lines.append("")

        # DONE section (if requested)
        if include_done:
            done_tasks = self.get_tasks_by_status("done")
            lines.append(f"## ✅ DONE ({len(done_tasks)} tasks)")
            lines.append("-" * 80)
            if not done_tasks:
                lines.append("  (no completed tasks)")
            else:
                # Show most recent 20 completed tasks
                recent_done = sorted(
                    done_tasks,
                    key=lambda t: t.completed_date or t.updated_date,
                    reverse=True,
                )[:20]
                for task in recent_done:
                    lines.extend(self._format_task_display(task))
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    def _format_task_display(self, task: Task) -> list[str]:
        """Format task for display in terminal"""
        lines = []

        # Main task line
        sprint_marker = "🏃 " if task.sprint_item else "   "
        deadline_str = f" ⏰ {task.deadline}" if task.deadline else ""
        lines.append(f"\n  {sprint_marker}[{task.task_id}] {task.title}{deadline_str}")

        # Project and details
        if task.project_name:
            lines.append(f"     Project: {task.project_name}")
        if task.details:
            lines.append(f"     Details: {task.details}")
        if task.status == "done" and task.completed_date:
            lines.append(f"     Completed: {task.completed_date}")

        return lines


def main() -> None:
    """Demo usage"""
    import sys

    # Fix Windows console encoding for emojis
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

    board = KanbanBoard()

    # Example: Add some tasks
    board.add_task(
        title="Review ADR-008",
        project_name="Documentation",
        sprint_item=True,
        details="Review and provide feedback on Standard Report Publication Strategy",
        deadline="2026-05-22",
    )

    board.add_task(
        title="Update GCP delivery gates",
        project_name="GCP Process",
        sprint_item=False,
        details="Incorporate SA engagement integration feedback",
        deadline="2026-05-25",
    )

    # Add a daily summary
    board.add_daily_summary(
        what_i_did="Reviewed data ownership documentation, attended team sync",
        what_i_need_to_do="Complete ADR review, update delivery gates documentation",
    )

    # Print list
    print(board.format_list(include_done=False))


if __name__ == "__main__":
    main()
