# Code Mode (`py_exec`)

- When you need to read or filter multiple files, inspect tabular/JSON/CSV data, cross-check many records, or run repetitive steps, batch them into **one `py_exec` call** (pass `cwd` pointing to the project directory on the first call) instead of making separate tool calls.
- Only `print()` summaries, metrics, or relevant error lines; never dump entire large files to stdout (output is truncated around 50,000 characters).
- Reuse variables and imported modules across calls in the same session; call `py_reset` when switching tasks or clearing state (state is also cleared if the server restarts or a call exceeds its timeout, 60s default / 600s max).
- Keep using dedicated tools for single-file edits (`edit_file`), browser automation, or long-running shell commands (`run_command`, e.g., package installs or builds).
- Check `sys.version` if unsure which Python version the configured interpreter runs, and prefer standard-library compatibility when writing quick scripts.
