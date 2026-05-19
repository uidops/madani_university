# RSS Feed Reader

Final project: a PyQt RSS feed reader with local encrypted SQLite storage and QR-code support.

## Files

| File | Description |
| --- | --- |
| `main.py` | Main PyQt application, RSS fetching, parsing, display, and feed actions. |
| `database.py` | SQLCipher-backed local database helper for RSS URLs and feed entries. |
| `dialog.py` | Dialog for adding a new RSS feed URL. |
| `qrcode_dialog.py` | Dialog for showing and copying a feed link QR code. |
| `rss.png` | Embedded image used in generated QR codes. |
| `error.png` | Fallback image for failed feed image loading. |

## Requirements

- Python 3
- PyQt5
- aiohttp
- Pillow
- qrcode
- sqlcipher3

Install Python packages if needed:

```bash
python3 -m pip install PyQt5 aiohttp pillow qrcode sqlcipher3
```

## Run

From this directory:

```bash
python3 main.py
```

## Notes

- The app creates `database.db` in this directory at runtime.
- `database.db` is runtime data and should not be committed.
- Right-clicking a feed item opens a QR-code dialog for the feed link.
