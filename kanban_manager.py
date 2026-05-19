#!/usr/bin/env python3
"""
Personal Kanban Board Manager for BA Agent
Stores tasks locally in kanban.json
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

# Type aliases
TaskStatus = Literal["backlog", "todo", "in_progress", "done"]

# Default kanban file location
KANBAN_FILE = Path(__file__).parent / "kanban.json"


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
        tags: list[str] | None = None,
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_date = created_date or datetime.now().isoformat()
        self.updated_date = updated_date or datetime.now().isoformat()
        self.tags = tags or []

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(**data)

    def __repr__(self) -> str:
        return f"Task({self.task_id}: {self.title} [{self.status}])"


class KanbanBoard:
    """Manages the kanban board and tasks"""

    def __init__(self, kanban_file: Path = KANBAN_FILE):
        self.kanban_file = kanban_file
        self.tasks: list[Task] = []
        self.daily_summaries: list[dict] = []
        self.load()

    def load(self) -> None:
        """Load kanban board from JSON file"""
        if not self.kanban_file.exists():
            self.save()  # Create empty board
            return

        with open(self.kanban_file) as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
            self.daily_summaries = data.get("daily_summaries", [])

    def save(self) -> None:
        """Save kanban board to JSON file"""
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "daily_summaries": self.daily_summaries,
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.kanban_file, "w") as f:
            json.dump(data, f, indent=2)

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
                task.updated_date = datetime.now().isoformat()
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
            "date": datetime.now().isoformat(),
            "what_i_did": what_i_did,
            "what_i_need_to_do": what_i_need_to_do,
        }
        self.daily_summaries.append(summary)
        self.save()

    def get_recent_summaries(self, limit: int = 5) -> list[dict]:
        """Get recent daily summaries"""
        return self.daily_summaries[-limit:]

    def format_board(self) -> str:
        """Format the kanban board as a readable string"""
        lines = ["=" * 80, "PERSONAL KANBAN BOARD", "=" * 80, ""]

        for status in ["backlog", "todo", "in_progress", "done"]:
            status_display = status.upper().replace("_", " ")
            tasks = self.get_tasks_by_status(status)  # type: ignore

            lines.append(f"\n## {status_display} ({len(tasks)} tasks)")
            lines.append("-" * 80)

            if not tasks:
                lines.append("  (no tasks)")
            else:
                for task in tasks:
                    priority_marker = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢",
                    }.get(task.priority, "⚪")

                    lines.append(f"\n  {priority_marker} [{task.task_id}] {task.title}")
                    if task.description:
                        lines.append(f"     {task.description}")
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
                    lines.append(f"     {task.description}")
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
                    lines.append(f"     {task.description}")
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
            date = datetime.fromisoformat(last["date"]).strftime("%Y-%m-%d %H:%M")
            lines.append(f"Date: {date}")
            lines.append(f"\nWhat I did:")
            lines.append(f"  {last['what_i_did']}")
            lines.append(f"\nWhat I need to do:")
            lines.append(f"  {last['what_i_need_to_do']}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


def main() -> None:
    """Demo usage"""
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
