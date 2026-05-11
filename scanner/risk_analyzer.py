def analyze_risk(open_ports):
    ports = [p['port'] for p in open_ports]
    score = len(ports)
    rec = []
    if 23 in ports: score += 3; rec.append("Закрыть Telnet (порт 23).")
    if 21 in ports: score += 1; rec.append("Ограничить FTP и перейти на SFTP/SSH.")
    if 3389 in ports: score += 2; rec.append("Ограничить RDP по VPN/ACL.")
    if 443 in ports: score -= 1; rec.append("HTTPS найден: поддерживайте актуальные TLS-настройки.")
    level = "Низкий" if score <=2 else "Средний" if score<=5 else "Высокий"
    if not rec: rec=["Поддерживайте обновления, firewall и сегментацию сети."]
    return {"score": max(score,0), "level": level, "recommendations": rec}
