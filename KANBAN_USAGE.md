# Personal Kanban Board - Usage Guide

Your BA Agent now includes a personal kanban board with three simple sections: **TO-DO**, **DOING**, and **DONE**.

## 📋 Quick Commands

### 1. TODO - Add a Task

Add a new task to your TO-DO list. The agent will ask you for details:

```bash
python ba_agent.py todo "Review data model design"
```

You'll be prompted for:
- **Project Name**: Which project does this belong to?
- **Sprint Item (Y/N)**: Is this part of the current sprint?
- **Details**: Additional information about the task
- **Deadline**: When is it due? (YYYY-MM-DD format)

**Quick add with all details:**
```bash
python ba_agent.py todo "Update BRD" \
  --project "Alpha Project" \
  --sprint \
  --details "Incorporate stakeholder feedback from meeting" \
  --deadline "2026-05-25"
```

### 2. LIST - Show Active Tasks

View your TO-DO and DOING tasks:

```bash
python ba_agent.py list
```

### 2a. LIST ALL - Show All Tasks

View all tasks including completed ones:

```bash
python ba_agent.py list all
```

### 3. DONE - Mark Task Complete

Mark a task as done:

```bash
python ba_agent.py done TASK-001
```

Or run without the task ID and the agent will show you your active tasks and ask which one you completed:

```bash
python ba_agent.py done
```

## 📝 Daily Summary

Track what you did and what's next:

```bash
python ba_agent.py summary
```

You'll be prompted for:
- What did you do today?
- What do you need to do next?

**Quick summary:**
```bash
python ba_agent.py summary \
  --did "Reviewed ADR-008, attended team sync" \
  --need "Complete data ownership docs"
```

## 🎯 Typical Workflow

### Morning - Check Your Tasks
```bash
python ba_agent.py list
```

### During the Day - Add Tasks as They Come
```bash
# Quick add
python ba_agent.py todo "Schedule stakeholder meeting"

# Or with details for sprint work
python ba_agent.py todo "Implement validation rules" \
  --project "Data Platform" \
  --sprint \
  --deadline "2026-05-22"
```

### Mark Progress
When you start working on a task, you can manually move it to DOING by editing `kanban.md`, or just mark it DONE when finished:

```bash
python ba_agent.py done TASK-003
```

### End of Day - Log Summary
```bash
python ba_agent.py summary
```

## 📂 Kanban Board Sections

**📋 TO-DO**: Tasks waiting to be started (sorted by deadline)  
**🔄 DOING**: Tasks you're actively working on  
**✅ DONE**: Completed tasks (shows last 30)

## 🏃 Sprint Items

Mark important sprint tasks with the `--sprint` flag. They'll show up with a 🏃 marker in your list:

```bash
python ba_agent.py todo "Critical bug fix" --sprint
```

## 📅 Deadlines

Tasks with deadlines appear at the top of your TO-DO list:

```bash
python ba_agent.py todo "Submit report" --deadline "2026-05-20"
```

## 🔒 Privacy

Your `kanban.md` file:
- Stored locally in your repository
- Excluded from git (in `.gitignore`)
- Viewable in any markdown viewer
- Manually editable in any text editor

## 💡 Tips

1. **Keep DOING small**: Only have 1-3 tasks in progress at a time
2. **Use deadlines**: Help prioritize your TO-DO list
3. **Mark sprint items**: Easily see what's time-sensitive
4. **Daily summaries**: Build a record of your progress
5. **Manual editing**: Open `kanban.md` to quickly reorganize tasks

## 📄 Example Kanban Board

```markdown
# 📊 Personal Kanban Board

## 📋 TO-DO

- [ ] **[TASK-001]** Review ADR-008 🏃
  - **Project:** Documentation
  - **Sprint Item:** Yes
  - **Details:** Provide feedback on report strategy
  - **Deadline:** 2026-05-22
  - **Created:** 2026-05-19

- [ ] **[TASK-002]** Schedule stakeholder meeting
  - **Project:** Alpha Project
  - **Sprint Item:** No
  - **Deadline:** 2026-05-25
  - **Created:** 2026-05-19

## 🔄 DOING

- [ ] **[TASK-003]** Update data model
  - **Project:** Data Platform
  - **Sprint Item:** Yes
  - **Details:** Add validation rules
  - **Created:** 2026-05-18

## ✅ DONE

- [x] **[TASK-004]** Review API specifications
  - **Project:** Integration
  - **Sprint Item:** No
  - **Created:** 2026-05-17
  - **Completed:** 2026-05-19
```

## 🚀 Command Reference

| Command | Description | Interactive? |
|---------|-------------|--------------|
| `todo` | Add task to TO-DO | Yes (if args not provided) |
| `list` | Show TO-DO and DOING tasks | No |
| `list all` | Show all tasks including DONE | No |
| `done` | Mark task as DONE | Yes (if task ID not provided) |
| `summary` | Add daily summary | Yes (if args not provided) |

All commands can be run interactively (agent asks questions) or with command-line arguments for automation.
