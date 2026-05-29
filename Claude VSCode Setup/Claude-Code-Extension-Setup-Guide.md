# Claude Code Extension Setup Guide

This guide walks you through setting up the Claude Code Extension in VS Code from scratch, configured for use with Lingaro's LLM Gateway.

## Prerequisites

- **VS Code**: Download and install from [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Lingaro API Key**: Obtain your personal API key token from your Lingaro administrator

## Step 1: Install VS Code

1. Download VS Code from the official website
2. Run the installer and follow the installation wizard
3. Launch VS Code after installation completes

## Step 2: Install Claude Code Extension

1. Open VS Code
2. Click on the **Extensions** icon in the left sidebar (or press `Ctrl+Shift+X`)
3. Search for **"Claude Code"** in the extensions marketplace
4. Click **Install** on the official Claude Code extension by Anthropic
5. Wait for the installation to complete
6. Restart VS Code if prompted

## Step 3: Configure Environment Variables

Before using the Claude Code Extension, you need to set up three environment variables to connect to Lingaro's LLM Gateway.

### Windows Setup

1. Open **PowerShell** or **Command Prompt** as Administrator
2. Run the following commands one by one:

```powershell
setx ANTHROPIC_BASE_URL "https://llm.lingarogroup.com"
setx ANTHROPIC_AUTH_TOKEN "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx"
setx ANTHROPIC_MODEL "claude-sonnet-4-5"
```

> **Important**: Replace `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx` with your personal Lingaro API Key Token

3. You should see "SUCCESS: Specified value was saved." for each command
4. **Close all VS Code windows** and restart VS Code to apply the environment variables

### Verify Environment Variables

To verify the environment variables were set correctly:

1. Open a new PowerShell window
2. Run:
```powershell
echo $env:ANTHROPIC_BASE_URL
echo $env:ANTHROPIC_AUTH_TOKEN
echo $env:ANTHROPIC_MODEL
```

You should see your configured values displayed.

## Step 4: First-Time Extension Configuration

1. After restarting VS Code, the Claude Code extension should automatically detect your environment variables
2. Open the Command Palette (`Ctrl+Shift+P`)
3. Type **"Claude Code"** to see available commands
4. You can also access Claude Code from:
   - The Claude icon in the Activity Bar (left sidebar)
   - Right-click in any file and select "Claude Code" options

## Step 5: Verify Setup

Test that everything is working correctly:

1. Open the Claude Code panel (click the Claude icon in the left sidebar)
2. Try a simple query like: "Hello, can you verify this is working?"
3. If you see a response from Claude, your setup is complete!

## Troubleshooting

### Extension Not Connecting

**Issue**: Claude Code cannot connect to the service

**Solutions**:
- Verify environment variables are set correctly (see Step 3)
- Ensure you've restarted VS Code after setting environment variables
- Check that your `ANTHROPIC_AUTH_TOKEN` is valid and not expired
- Verify you have network access to `https://llm.lingarogroup.com`

### Environment Variables Not Recognized

**Issue**: VS Code doesn't detect the environment variables

**Solutions**:
- Close **all** VS Code windows completely
- Reopen VS Code (environment variables are loaded on startup)
- On Windows, system environment variables require a full application restart

### Authentication Errors

**Issue**: Receiving authentication or permission errors

**Solutions**:
- Verify your `ANTHROPIC_AUTH_TOKEN` is correct
- Contact your Lingaro administrator to confirm your API key is active
- Check that you're using the correct token format (should start with `sk-`)

## Additional Configuration

### Model Selection

The default model is set via the `ANTHROPIC_MODEL` environment variable to `claude-sonnet-4-5`. You can change this by:

1. Opening PowerShell as Administrator
2. Running:
```powershell
setx ANTHROPIC_MODEL "claude-opus-4-7"
```
3. Restarting VS Code

Available models:
- `claude-sonnet-4-5` (balanced - default)
- `claude-sonnet-4-6` (more capable)
- `claude-opus-4-7` (most capable)
- `claude-haiku-4-5-20251001` (fastest)

### Extension Settings

Access Claude Code settings:

1. Open Settings (`Ctrl+,`)
2. Search for "Claude Code"
3. Configure preferences such as:
   - Permission modes
   - Auto-save behavior
   - UI preferences

## Getting Help

- **VS Code Command Palette**: Press `Ctrl+Shift+P` and type `/help`
- **Claude Code Documentation**: [https://github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
- **Internal Support**: Contact your team lead or Lingaro IT support

## Security Notes

⚠️ **Important Security Reminders**:

- Never share your `ANTHROPIC_AUTH_TOKEN` with anyone
- Do not commit your API token to version control
- Environment variables are specific to your user account on your machine
- If you suspect your token is compromised, contact your administrator immediately to rotate it

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-19  
**Maintained By**: GCP Team
