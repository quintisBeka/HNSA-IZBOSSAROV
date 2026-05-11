"""Safe scanner for educational/authorized environments only."""
import ipaddress, socket, time, subprocess
from concurrent.futures import ThreadPoolExecutor

PORTS = {20:'FTP-DATA',21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',135:'RPC',139:'NetBIOS',143:'IMAP',443:'HTTPS',445:'SMB',3306:'MySQL',3389:'RDP',8080:'HTTP-Alt'}

def _check_port(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(timeout)
    try:
        return port if s.connect_ex((ip, port)) == 0 else None
    finally:
        s.close()

def scan_ip(ip, timeout=0.8):
    open_ports=[]; started=time.time()
    with ThreadPoolExecutor(max_workers=40) as ex:
        for p in ex.map(lambda x: _check_port(ip, x, timeout), PORTS.keys()):
            if p:
                open_ports.append({"port": p, "service": PORTS[p], "status": "open"})
    return {"target": ip, "open_ports": sorted(open_ports,key=lambda x:x['port']), "duration": round(time.time()-started,2)}

def scan_target(target, timeout=0.8):
    if '/' in target:
        net = ipaddress.ip_network(target, strict=False)
        all_results=[]
        for h in net.hosts():
            all_results.extend(scan_ip(str(h), timeout)["open_ports"])
        return {"target": target, "open_ports": all_results, "duration": 0}
    ipaddress.ip_address(target)
    return scan_ip(target, timeout)

def discover_hosts(cidr):
    net=ipaddress.ip_network(cidr, strict=False); active=[]
    for h in list(net.hosts())[:20]:
        ip=str(h)
        if subprocess.call(["ping","-c","1","-W","1",ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)==0:
            try: host=socket.gethostbyaddr(ip)[0]
            except: host="unknown"
            active.append({"ip":ip,"hostname":host,"status":"online","mac":"N/A"})
    return active

def dns_lookup(domain):
    try: return socket.gethostbyname_ex(domain)
    except Exception as e: return str(e)
def reverse_dns(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except Exception as e: return str(e)
def whois_lookup(target):
    return "WHOIS summary placeholder (install python-whois for full data)"
def uptime_check(ip):
    return "online" if subprocess.call(["ping","-c","1","-W","1",ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)==0 else "offline"
