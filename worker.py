#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Persistent Python worker for Code Mode Antigravity: reads JSON lines and preserves state."""
import ast
import io
import json
import linecache
import os
import sys
import traceback

sys.stdout.reconfigure(encoding="utf-8", newline="\n")
sys.stdin.reconfigure(encoding="utf-8")

STATE = {"__name__": "__main__"}
_EXEC_SEQ = 0
_MAX_LINECACHE_ENTRIES = 200


def _safe_repr(value, limit=20000):
    try:
        return repr(value)[:limit]
    except BaseException as exc:
        return "<repr failed: %s: %s>" % (type(exc).__name__, exc)


def execute(code, cwd=None):
    global _EXEC_SEQ
    out_buf = io.BytesIO()
    err_buf = io.BytesIO()
    out = io.TextIOWrapper(out_buf, encoding="utf-8", errors="replace", newline="\n")
    err = io.TextIOWrapper(err_buf, encoding="utf-8", errors="replace", newline="\n")
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    value = None
    has_value = False
    ok = True
    try:
        if cwd:
            os.chdir(cwd)
        _EXEC_SEQ += 1
        filename = "<py_exec_%d>" % _EXEC_SEQ
        linecache.cache[filename] = (len(code), None, code.splitlines(keepends=True), filename)
        if _EXEC_SEQ > _MAX_LINECACHE_ENTRIES:
            linecache.cache.pop("<py_exec_%d>" % (_EXEC_SEQ - _MAX_LINECACHE_ENTRIES), None)
        tree = ast.parse(code, filename, "exec")
        last_expr = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_expr = tree.body.pop()
        if tree.body:
            exec(compile(tree, filename, "exec"), STATE)
        if last_expr is not None:
            value = eval(compile(ast.Expression(last_expr.value), filename, "eval"), STATE)
            has_value = True
    except BaseException:
        ok = False
        traceback.print_exc()
    finally:
        for stream in (out, err):
            if not stream.closed:
                stream.flush()
        sys.stdout, sys.stderr = old_out, old_err
    return {
        "ok": ok,
        "stdout": out_buf.getvalue().decode("utf-8", "replace"),
        "stderr": err_buf.getvalue().decode("utf-8", "replace"),
        "value": _safe_repr(value) if has_value else None,
        "has_value": has_value,
    }


def main():
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            request = json.loads(raw)
        except ValueError:
            sys.stdout.write(json.dumps({"ok": False, "error": "Invalid JSON"}, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue
        result = execute(request.get("code") or "", request.get("cwd") or None)
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
