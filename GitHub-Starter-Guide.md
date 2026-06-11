# GitHub Starter Guide for Business Analysts & Project Managers

## What is GitHub and Why Should You Care?

GitHub is like **Azure DevOps for code**, but it's more widely used in the software industry. While Azure DevOps helps you manage user stories and tasks, GitHub helps manage the actual code and documentation files.

Think of it this way:
- **Azure DevOps Repos** = Where your team might store code internally
- **GitHub** = The industry-standard platform where most open-source projects and modern teams collaborate on code
- **Git** = The underlying technology (like the engine in a car)
- **GitHub** = The platform built on top of Git (like the car itself with all the features)

### Why GitHub Matters for You

Even as a non-developer, you'll benefit from GitHub because:
- **Documentation lives here** - Requirements, guides, and project docs are often stored alongside code
- **Transparency** - You can see exactly what changed, when, and why
- **Collaboration** - You can review, comment, and suggest changes to documents
- **Version history** - Never worry about "Final_v2_FINAL_USE_THIS.docx" again
- **LLM Integration** - Tools like Claude Code work directly with GitHub to help you write, review, and manage content

---

## GitHub vs Azure DevOps: A Quick Comparison

| Concept | Azure DevOps | GitHub |
|---------|--------------|--------|
| Work Items/User Stories | Work Items, Boards | Issues, Projects |
| Code Storage | Repos | Repositories |
| Code Review | Pull Requests | Pull Requests |
| Documentation | Wiki | README.md, Wiki, Pages |
| CI/CD | Pipelines | Actions |
| Discussion | Comments | Issues, Discussions |

---

## Core Concepts (In Plain English)

### Repository (Repo)
A **repository** is like a project folder that contains all your files and tracks every change ever made to them.
- Think of it as a shared project folder with superpowers
- Contains code, documentation, images, and any other files
- Has a complete history of all changes

### Branch
A **branch** is like creating a copy of your project to work on without affecting the original.
- The main branch is usually called `main` or `master` (the "official" version)
- You create feature branches to work on changes safely
- Similar to creating a "draft" version of a document

**Example**: If you're updating a requirements document:
- `main` branch = The approved, current version
- `update-requirements-q2` branch = Your draft with changes
- Once approved, your branch gets merged back into `main`

### Commit
A **commit** is like saving a checkpoint of your work with a description of what changed.
- Each commit is a snapshot in time
- Includes a message explaining what was changed and why
- You can always go back to any previous commit

**Example commit messages**:
- "Updated stakeholder list in requirements doc"
- "Added data privacy requirements section"
- "Fixed typos in user guide"

### Pull Request (PR)
A **pull request** is like submitting your draft for review.
- You're asking to "pull" your changes into the main branch
- Others can review, comment, and request changes
- Very similar to Azure DevOps Pull Requests

### Clone
**Cloning** means downloading a complete copy of a repository to your computer.
- You get all files and all history
- You can work on it locally on your machine

### Push & Pull
- **Push** = Upload your local changes to GitHub
- **Pull** = Download changes others made from GitHub to your computer

---

## Getting Started: Setup

### 1. Install Git
1. Download Git from [git-scm.com](https://git-scm.com/)
2. Run the installer (accept default options)
3. Verify installation by opening PowerShell/Command Prompt and typing: `git --version`

### 2. Create a GitHub Account
1. Go to [github.com](https://github.com)
2. Sign up with your work email
3. Enable Two-Factor Authentication (2FA) for security

### 3. Configure Git
Open PowerShell or Command Prompt and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

This ensures your name appears on your commits.

---

## Working with GitHub in Visual Studio

Visual Studio has built-in GitHub integration, making it easy to work without using command lines!

### Cloning a Repository in Visual Studio

1. **Open Visual Studio**
2. Click **"Clone a repository"** on the start screen
3. **Sign in to GitHub** (if prompted)
4. **Browse or search** for the repository you want
5. **Choose a local path** (where to save it on your computer)
6. Click **"Clone"**

### Making Changes

1. **Open the repository** in Visual Studio
2. **Edit files** normally (documents, markdown files, etc.)
3. **Save your changes**

### Committing Changes (Saving a Checkpoint)

1. Go to **View → Git Changes** (or press `Ctrl + 0, Ctrl + G`)
2. You'll see all files you've modified
3. **Review your changes** in the diff view
4. **Write a commit message** describing what you changed
   - Keep it short but descriptive
   - Example: "Added Q2 objectives to business requirements"
5. Click **"Commit All"** (saves locally) or **"Commit All and Push"** (saves and uploads to GitHub)

### Creating a Branch

1. In the **Git Changes** panel, click the branch dropdown (usually shows "main")
2. Click **"New Branch"**
3. Name your branch (use descriptive names like `update-user-guide` or `add-q2-requirements`)
4. Click **"Create"**

You're now working on your own branch!

### Pushing Changes to GitHub

After committing:
1. Click **"Push"** in the Git Changes panel
2. Your changes are now on GitHub for others to see

### Creating a Pull Request

1. Go to your repository on **GitHub.com**
2. You'll see a banner: **"Compare & pull request"** - click it
3. **Write a description** of your changes
4. **Add reviewers** (team members who should review)
5. Click **"Create pull request"**

Now others can review, comment, and approve your changes!

---

## Essential Git Commands (For Reference)

While Visual Studio's UI handles most tasks, knowing these commands helps when you need more control:

### Getting Started
```bash
# Clone a repository
git clone https://github.com/username/repository-name.git

# Check repository status
git status
```

### Basic Workflow
```bash
# Create and switch to a new branch
git checkout -b my-feature-branch

# See what branch you're on
git branch

# Stage changes (prepare to commit)
git add .

# Commit changes
git commit -m "Descriptive message about what changed"

# Push to GitHub
git push origin my-feature-branch

# Pull latest changes from GitHub
git pull
```

### Working with Branches
```bash
# Switch to a different branch
git checkout branch-name

# Switch to main branch
git checkout main

# Update your current branch with latest from main
git pull origin main

# Delete a branch (after it's merged)
git branch -d branch-name
```

### Viewing History
```bash
# See commit history
git log

# See a simpler version of history
git log --oneline

# See who changed what in a file
git blame filename.md
```

---

## Working with LLMs (Claude Code, GitHub Copilot)

### Claude Code + GitHub
Claude Code is an AI assistant that works directly with your GitHub repositories:

**What Claude Code Can Do**:
- Write and edit documentation
- Review your changes
- Create pull requests
- Answer questions about files in the repository
- Suggest improvements to your documents

**How to Use**:
1. Open Visual Studio Code
2. Install the Claude Code extension
3. Open your GitHub repository
4. Use Claude to help with tasks like:
   - "Help me draft a requirements document"
   - "Review this PR for clarity"
   - "Create a user guide based on these user stories"

**Tips for Working with LLMs on GitHub**:
- Commit frequently so the AI can see your progress
- Use descriptive commit messages - they help the AI understand context
- Ask the AI to explain what changed in a PR
- Have the AI review your documentation for clarity

### GitHub Copilot (for VS Code)
- AI pair programmer built into Visual Studio Code
- Suggests code completions and documentation
- Works well with markdown files for documentation

---

## Common Workflows for BAs and PMs

### Workflow 1: Creating Documentation

1. **Clone the repository** (if you haven't already)
2. **Create a new branch**: `git checkout -b add-requirements-doc`
3. **Create or edit your markdown file** (e.g., `requirements.md`)
4. **Commit your changes**: `git commit -m "Added initial requirements document"`
5. **Push to GitHub**: `git push origin add-requirements-doc`
6. **Create a Pull Request** on GitHub
7. **Request review** from team members
8. **Address feedback** if needed
9. **Merge** once approved

### Workflow 2: Updating Existing Documentation

1. **Pull latest changes**: `git pull` (ensures you have the latest version)
2. **Create a new branch**: `git checkout -b update-user-guide`
3. **Make your edits**
4. **Review changes** in Visual Studio's diff view
5. **Commit and push**
6. **Create Pull Request**

### Workflow 3: Reviewing Someone Else's Changes

1. Go to the **Pull Request** on GitHub
2. Click **"Files changed"** tab
3. Review the differences (additions in green, deletions in red)
4. **Add comments** by clicking the "+" next to line numbers
5. **Submit review**: Approve, request changes, or just comment

### Workflow 4: Linking GitHub to Azure DevOps

You can reference Azure DevOps work items in your commits:

```bash
git commit -m "Updated requirements doc - Relates to AB#12345"
```

Where `AB#12345` is your Azure DevOps work item number.

---

## Markdown Basics

Most documentation on GitHub is written in **Markdown** (.md files) - a simple formatting language.

### Quick Markdown Reference

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*

- Bullet point
- Another bullet point

1. Numbered list
2. Second item

[Link text](https://url.com)

![Image alt text](image-url.jpg)

`inline code`

```
Code block
```

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

---

## Best Practices for Non-Technical Users

### Commit Messages
**Good commit messages**:
- "Added data governance requirements section"
- "Updated stakeholder contact information"
- "Fixed formatting in user guide"

**Poor commit messages**:
- "Update"
- "Changes"
- "Fixed stuff"

### Branching Strategy
- Always create a new branch for changes
- Use descriptive branch names: `update-requirements`, `add-glossary`, `fix-typos`
- Never commit directly to `main`

### Pull Requests
- Write clear descriptions of what changed and why
- Add screenshots if you changed visual elements
- Link to related Azure DevOps work items
- Request reviews from relevant team members
- Respond to feedback promptly

### File Organization
- Use clear, descriptive file names
- Keep related files in folders
- Add a README.md in each folder explaining its contents

---

## Helpful Tips & Tricks

### Tip 1: Use .gitignore
Create a `.gitignore` file to exclude files you don't want to track (temp files, credentials, etc.)

```
# Ignore temporary files
*.tmp
*.bak

# Ignore sensitive files
*.env
credentials.json

# Ignore system files
.DS_Store
Thumbs.db
```

### Tip 2: Use GitHub Issues for Discussions
- Create issues to track questions, suggestions, or problems
- Similar to Azure DevOps work items but more lightweight
- Great for documentation feedback

### Tip 3: Use Templates
Many repositories have templates for:
- Pull requests
- Issues
- Documentation

These help you provide consistent, complete information.

### Tip 4: Watch Repositories
Click **"Watch"** on repositories you work with often to get notifications about changes.

### Tip 5: Use Draft Pull Requests
If you're not ready for review yet:
1. Create a **Draft Pull Request**
2. Others can see your progress but know it's not ready for formal review
3. Mark it **"Ready for review"** when done

### Tip 6: Compare Branches
On GitHub, use the compare view to see differences between branches:
```
https://github.com/username/repo/compare/main...your-branch
```

### Tip 7: Keyboard Shortcuts
On GitHub.com:
- `t` - File finder
- `?` - Show all keyboard shortcuts
- `g` + `c` - Go to code
- `g` + `i` - Go to issues

---

## Troubleshooting Common Issues

### Problem: "I can't push my changes"
**Solution**: Someone else made changes. Pull their changes first:
```bash
git pull origin main
```
Resolve any conflicts, then push again.

### Problem: "I committed to the wrong branch"
**Solution**: Don't panic! You can move your commit:
```bash
git checkout correct-branch
git cherry-pick commit-hash
```

### Problem: "I want to undo my last commit"
**Solution**:
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes
git reset --hard HEAD~1
```

### Problem: "Merge conflict"
**Solution**:
1. Open the file in Visual Studio
2. Look for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Choose which changes to keep
4. Remove the conflict markers
5. Commit the resolution

### Problem: "I don't know what branch I'm on"
**Solution**:
```bash
git branch
```
The current branch has an asterisk (*) next to it.

---

## Quick Reference Cheat Sheet

| Task | Visual Studio | Command Line |
|------|--------------|--------------|
| Clone repo | File → Clone Repository | `git clone <url>` |
| Create branch | Git Changes → New Branch | `git checkout -b <name>` |
| Switch branch | Git Changes → Branch dropdown | `git checkout <name>` |
| See changes | Git Changes panel | `git status` |
| Commit | Git Changes → Commit message → Commit | `git commit -m "message"` |
| Push | Git Changes → Push | `git push` |
| Pull | Git Changes → Pull | `git pull` |
| View history | Git Changes → View History | `git log` |

---

## Learning Resources

### Official Documentation
- [GitHub Docs](https://docs.github.com) - Official GitHub documentation
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - Git basics

### Interactive Learning
- [GitHub Skills](https://skills.github.com/) - Interactive tutorials
- [Visualizing Git](https://git-school.github.io/visualizing-git/) - See how Git commands work

### Video Tutorials
- [GitHub for Beginners](https://www.youtube.com/githubguides) - Official YouTube channel
- Search "GitHub for non-developers" on YouTube

### Tools
- [Visual Studio](https://visualstudio.microsoft.com/) - IDE with built-in Git support
- [VS Code](https://code.visualstudio.com/) - Lightweight editor with GitHub integration
- [GitHub Desktop](https://desktop.github.com/) - Simple GUI for GitHub (alternative to VS)

---

## Getting Help

### Within Your Team
- Ask your developers or DevOps team
- Check your team's internal documentation
- Use your company's Teams/Slack channel

### Online
- [GitHub Community](https://github.community/) - Ask questions
- [Stack Overflow](https://stackoverflow.com/questions/tagged/git) - Tagged questions
- Your friendly LLM assistant (Claude Code, ChatGPT, etc.)

### Quick Commands for Help
```bash
# Help for a specific command
git help <command>

# Example
git help commit
```

---

## Next Steps

Now that you understand the basics:

1. **Practice with a test repository** - Create a personal repo to experiment
2. **Clone your team's repository** - Start with read-only exploration
3. **Make your first edit** - Update a simple document
4. **Create your first Pull Request** - Get comfortable with the review process
5. **Set up Claude Code or GitHub Copilot** - Enhance your productivity with AI

Remember: Everyone was a beginner once. Don't be afraid to ask questions, and make mistakes in a test repository where it's safe!

---

## Glossary

- **Branch**: A parallel version of your repository
- **Clone**: Download a repository to your computer
- **Commit**: A saved snapshot of changes
- **Fork**: Your personal copy of someone else's repository
- **Merge**: Combining changes from one branch into another
- **Origin**: The default name for the remote repository
- **Pull**: Download changes from GitHub
- **Pull Request (PR)**: Proposed changes for review
- **Push**: Upload changes to GitHub
- **Remote**: A repository hosted on GitHub (or elsewhere)
- **Repository (Repo)**: A project folder with version control
- **Staged**: Changes marked to be included in the next commit
- **Upstream**: The original repository (when you've forked)

---

**Happy GitHubbing!** 🚀

*Remember: Git tracks changes, GitHub hosts them, and you're in control. Take it one step at a time, and you'll be comfortable in no time.*
