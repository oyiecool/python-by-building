import os, requests

def chat_alert(text: str) -> None:
    url = os.environ["CHAT_WEBHOOK_URL"]             # treat this URL like a password
    key = "content" if "discord.com" in url else "text"   # Discord uses "content", Slack "text"
    r = requests.post(url, json={key: text}, timeout=10)
    r.raise_for_status()

chat_alert(":rotating_light: web01 CPU at 97% for 15 minutes")
