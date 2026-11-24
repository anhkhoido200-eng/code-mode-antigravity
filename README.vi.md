# Code Mode Antigravity

> English: [README.md](README.md)

Máy chủ Python REPL siêu nhẹ (**không cần cài thêm thư viện ngoài**) dành cho **Antigravity** và các AI agent hỗ trợ MCP.  
Giúp AI chạy Python giữ nguyên biến giữa các lần gọi, gộp việc đọc nhiều file, lọc dữ liệu JSON/CSV/SQLite, tính toán… vào **1 bước duy nhất** để tiết kiệm lượt gọi và token.

## Cài đặt

Yêu cầu máy đã có **Python 3.8+** và **Git**. Chạy trong Terminal / PowerShell:

```bash
git clone https://github.com/kninrin-droid/code-mode-antigravity.git
cd code-mode-antigravity
python install_antigravity.py --write
```

*(Nếu báo không tìm thấy `python`, thử thay bằng `py` trên Windows hoặc `python3` trên macOS/Linux. Sau đó **mở lại Antigravity** là dùng được ngay.)*

<details>
<summary>Nâng cao: xem cơ chế, cài thủ công, dùng cho Claude Code / Cursor &amp; kiểm thử</summary>

### Lệnh trên tự làm những gì?
- Tự sao lưu file cấu hình cũ (`*.bak-...`) trước khi sửa để đảm bảo an toàn.
- Thêm máy chủ `code-mode` (kèm `eager: true` cho `py_exec`) vào file cấu hình MCP của Antigravity.
- Cài bộ quy tắc `plugin/` (`AGENTS.md`) vào `~/.gemini/config/plugins/code-mode` (thêm `--no-plugin` nếu không muốn cài phần này).
- Chạy không tham số (`python install_antigravity.py`) nếu chỉ muốn xem trước, chưa ghi file.

### Chạy kiểm thử nhanh
```bash
python -u test_client.py
```

### Cài thủ công (Antigravity)
Thêm vào `~/.gemini/config/mcp_config.json` (hoặc **Settings > MCP**):
```json
{
  "mcpServers": {
    "code-mode": {
      "command": "python",
      "args": ["-u", "/duong/dan/day/du/toi/code-mode-antigravity/server.py"],
      "tools": {
        "py_exec": {
          "eager": true
        }
      }
    }
  }
}
```

### Dùng cho Claude Code, Cursor hoặc MCP client khác
```json
{
  "mcpServers": {
    "code-mode": {
      "command": "python",
      "args": ["-u", "/duong/dan/day/du/toi/code-mode-antigravity/server.py"]
    }
  }
}
```

### Công cụ &amp; lưu ý
- `py_exec(code, cwd?, timeout?)`: chạy Python trong phiên giữ biến; cắt output ở ~50.000 ký tự; `timeout` từ 1–600 giây (mặc định 60 giây).
- `py_reset()`: xóa sạch biến và thư viện đã nạp trong phiên.
- **Bảo mật:** `py_exec` chạy bằng quyền người dùng hiện tại trên máy (không phải sandbox), chỉ dùng trong môi trường tin cậy.

</details>

## Giấy phép

MIT — [LICENSE](LICENSE)
