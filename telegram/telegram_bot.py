import requests

def send_telegram_notification(token, chat_id, target, count, risk, duration):
    if token in ["BOT_TOKEN",""] or chat_id in ["CHAT_ID",""]:
        return False
    text = f"[Hybrid] Scan done\nTarget: {target}\nOpen ports: {count}\nRisk: {risk}\nDuration: {duration}s"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=4)
        return True
    except Exception:
        return False
