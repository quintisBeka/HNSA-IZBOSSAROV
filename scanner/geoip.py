import requests

def geo_lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        d = r.json()
        return {k: d.get(k) for k in ["country","city","isp","lat","lon","query","status"]}
    except Exception as e:
        return {"status":"fail", "error": str(e)}
