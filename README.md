# Archbot

Archbot is a minimal Arch Linux troubleshooting chatbot prototype. It maps natural-language prompts to:

- Arch Linux troubleshooting guidance linked to ArchWiki topics (Wi-Fi, boot, packages)
- Safe, allowlisted local OS checks (`df -h`, `free -h`, `systemctl --failed`)

## Run

```bash
python /home/runner/work/Archbot/Archbot/archbot.py
```

## Test

```bash
python -m unittest discover -s /home/runner/work/Archbot/Archbot/tests -v
```
