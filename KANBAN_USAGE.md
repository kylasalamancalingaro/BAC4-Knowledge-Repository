# Personal Kanban Board - Usage Guide

Your BA Agent now includes a personal kanban board to track your daily work. This is stored locally and **not shared** with the team.

## Quick Start

### View Today's To-Do List
```bash
python ba_agent.py today
```

This shows:
- 🔄 Tasks currently in progress
- 📋 Tasks in your to-do list
- 📝 Your latest daily summary

### Add Daily Summary
```bash
python ba_agent.py add-summary \
  --did "Reviewed ADR-008, attended team sync, updated delivery gates" \
  --need "Complete data ownership docs, schedule stakeholder meeting"
```

Use this at the end of your day to capture what you accomplished and what's coming next.

### View Full Kanban Board
```bash
python ba_agent.py board
```

Shows all tasks across all columns: Backlog → To Do → In Progress → Done

## Task Management

### Add a New Task
```bash
# Basic task
python ba_agent.py add-task "Review data model design"

# With details
python ba_agent.py add-task "Update BRD for project Alpha" \
  --description "Incorporate feedback from stakeholder meeting" \
  --status todo \
  --priority high \
  --tags requirements documentation
```

**Status options**: `backlog`, `todo`, `in_progress`, `done`  
**Priority options**: `high`, `medium`, `low`

### Update Task Status
```bash
# Move task to in-progress
python ba_agent.py update-task TASK-001 in_progress

# Mark task as done
python ba_agent.py update-task TASK-001 done
```

## Typical Daily Workflow

### Morning
```bash
# Check what you should be working on today
python ba_agent.py today
```

### During the Day
```bash
# Start working on a task
python ba_agent.py update-task TASK-003 in_progress

# Add new tasks as they come up
python ba_agent.py add-task "Prepare Q2 metrics report" --status todo --priority high
```

### End of Day
```bash
# Log your daily summary
python ba_agent.py add-summary \
  --did "Completed BRD review, drafted technical requirements for Feature X" \
  --need "Schedule follow-up with PM, review API specifications"

# This automatically shows your updated to-do list
```

## Data Storage

- All kanban data is stored in `kanban.json` in your local repository
- This file is **excluded from git** (in `.gitignore`)
- Your personal tasks remain private and are not shared with the team

## Task Organization Tips

**Backlog**: Future work, ideas, things to consider  
**To Do**: Prioritized tasks ready to start  
**In Progress**: What you're actively working on (keep this small!)  
**Done**: Completed work (helps track accomplishments)

## Priority Guidelines

🔴 **High**: Urgent, deadline-driven, blocking others  
🟡 **Medium**: Important but not urgent (default)  
🟢 **Low**: Nice-to-have, background tasks
