# BA Agent (Local)

A personal business analysis assistant that helps with meeting analysis and personal task management.

## Features

### 📊 Meeting Analysis (Ollama-powered)
- **Summarize** meeting notes with executive summaries and action items
- **Extract decisions** with structured decision tables
- **Identify requirements** with MoSCoW prioritization
- **Update BRDs** by incorporating meeting notes into existing documents
- **Context-aware** using your team wiki (Global-Clients.wiki) as background knowledge

### 📋 Personal Kanban Board
- Track your daily work in a kanban board format
- View your to-do list when you ask "what should I be doing today"
- Log daily summaries of what you did and what you need to do
- Keep all data local (not shared with team)
- Simple CLI commands for task management

## Installation

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running (for meeting analysis features)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Pull the Ollama model (default: llama3.1)
ollama pull llama3.1

# Test the agent
python ba_agent.py --help
```

## Usage

### Personal Kanban Commands

#### View Today's To-Do List
```bash
python ba_agent.py today
```

#### Add Daily Summary
```bash
python ba_agent.py add-summary \
  --did "What I accomplished today" \
  --need "What I need to do next"
```

#### View Full Board
```bash
python ba_agent.py board
```

#### Task Management
```bash
# Add a task
python ba_agent.py add-task "Review ADR-008" \
  --description "Provide feedback on report strategy" \
  --status todo \
  --priority high \
  --tags documentation adr

# Update task status
python ba_agent.py update-task TASK-001 in_progress
python ba_agent.py update-task TASK-001 done
```

See [KANBAN_USAGE.md](KANBAN_USAGE.md) for detailed kanban board usage.

### Meeting Analysis Commands

#### Analyze Meeting Notes
```bash
# Summarize meeting notes
python ba_agent.py analyze summarize --input meeting_notes.txt

# Extract decisions
python ba_agent.py analyze decisions --input meeting_notes.txt

# Extract requirements
python ba_agent.py analyze requirements --input meeting_notes.txt

# Run all analyses
python ba_agent.py analyze all --input meeting_notes.txt --output analysis_output.md

# Update BRD with meeting notes
python ba_agent.py analyze update-brd --input meeting_notes.txt --brd existing_brd.md --output updated_brd.md
```

## Project Structure

```
BA-Agent-Local/
├── ba_agent.py           # Main agent implementation
├── kanban_manager.py     # Kanban board functionality
├── pii_masker.py         # PII masking utility
├── kanban.md             # Your personal task board (markdown, not committed to git)
├── outputs/              # Analysis outputs
├── KANBAN_USAGE.md       # Detailed kanban usage guide
├── README.md             # This file
├── CLAUDE.md             # Project instructions for Claude
└── requirements.txt      # Python dependencies
```

## Configuration

### Environment Variables

```bash
# Ollama model (default: llama3.1)
export BA_AGENT_MODEL=llama3.1

# Ollama API URL (default: http://localhost:11434/api/generate)
export BA_AGENT_OLLAMA_URL=http://localhost:11434/api/generate

# Team wiki root for context (default: auto-detected)
export BA_AGENT_WIKI_ROOT=/path/to/Global-Clients.wiki
```

### Privacy & Data Storage

- **Kanban data** (`kanban.md`) is stored as markdown locally and excluded from git
- **Meeting analysis** can output to `outputs/` directory (also excluded from git)
- **PII masking** is available via `pii_masker.py` for sensitive data

The kanban board uses markdown format, so you can:
- View it in any markdown viewer
- Edit it manually in any text editor
- Copy sections to other documents
- Keep it readable without the Python script

## Workflow Examples

### Daily Morning Routine
```bash
# Check what you should work on today
python ba_agent.py today
```

### After a Meeting
```bash
# Analyze meeting notes
python ba_agent.py analyze all --input meeting_notes.txt --output outputs/meeting_analysis.md

# Add any new tasks that came up
python ba_agent.py add-task "Follow up on API design" --status todo --priority high
```

### End of Day
```bash
# Log your daily summary
python ba_agent.py add-summary \
  --did "Reviewed ADR-008, attended planning meeting, updated BRD" \
  --need "Schedule stakeholder sync, complete data model review"
```

## Development

Built with:
- **Anthropic SDK** for AI capabilities
- **Ollama** for local LLM inference
- **Python 3.11+** for clean, modern syntax
- **Pydantic** for data validation

## License

Internal tool for personal use.
