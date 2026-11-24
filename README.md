# Code Mode Antigravity

> Tiếng Việt: [README.vi.md](README.vi.md)

A lightweight, **zero-dependency** Python REPL MCP server for **Antigravity** (and other MCP agents).  
It keeps Python variables and imports alive between calls so your AI can batch multi-file reads, JSON/CSV/SQLite checks, and calculations into **one step** instead of dozens of tool calls.

## Install

Requires **Python 3.8+** and **Git**. Run in your terminal:

```bash
git clone https://github.com/kninrin-droid/code-mode-antigravity.git
cd code-mode-antigravity
python install_antigravity.py --write
```

*(Use `python3` on macOS/Linux or `py` on Windows if `python` is not found. Then **restart Antigravity**.)*

<details>
<summary>Advanced: manual setup, Claude Code / Cursor, tests &amp; details</summary>

### What the installer does
- Backs up your existing MCP config (`*.bak-...`) before editing.
- Adds `code-mode` (`py_exec` with `eager: true` and `py_reset`) to Antigravity's MCP config.
- Installs `plugin/` (`rules/AGENTS.md`) into `~/.gemini/config/plugins/code-mode` (pass `--no-plugin` to skip).
- Pass no flags (`python install_antigravity.py`) to preview changes without writing.

### Run smoke test
```bash
python -u test_client.py
```

### Manual JSON (Antigravity)
Add to `~/.gemini/config/mcp_config.json` (or **Settings > MCP**):
```json
{
  "mcpServers": {
    "code-mode": {
      "command": "python",
      "args": ["-u", "/absolute/path/to/code-mode-antigravity/server.py"],
      "tools": {
        "py_exec": {
          "eager": true
        }
      }
    }
  }
}
```

### Other MCP clients (Claude Code, Cursor, etc.)
```json
{
  "mcpServers": {
    "code-mode": {
      "command": "python",
      "args": ["-u", "/absolute/path/to/code-mode-antigravity/server.py"]
    }
  }
}
```

### Tools &amp; limits
- `py_exec(code, cwd?, timeout?)`: runs Python in a persistent subprocess; output is capped around 50,000 characters; timeout is 1–600s (default 60s).
- `py_reset()`: clears session variables and imports.
- **Security:** `py_exec` runs with your user permissions (not a sandbox). Use only in trusted environments.

</details>

## License

MIT — [LICENSE](LICENSE)
