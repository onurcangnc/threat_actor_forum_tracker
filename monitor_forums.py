import asyncio, aiohttp
from flask import Flask, jsonify, render_template_string
from datetime import datetime
from threading import Thread

# ------------ CONFIG --------------
INTERVAL = 60        # forum tarama aralığı (sn)
PORT     = 8082      # Flask portu
BOT_TOKEN = "7616505173:AAFQ9JAY2tdiylYBp0S9fLxG3UyPPsv2GNA"  # <-- bot token
CHAT_ID   = "649226694"    # <-- hedef chat id
# ----------------------------------

forums = {
    "https://0x00sec.org": "0x00sec",
    "https://alligator.cash": "alligator",
    "https://altenens.is": "altenen",
    "https://forum.antichat.com": "antichat",
    "https://ascarding.com": "carding",
    "https://blackhatprotools.info": "blackhat",
    "https://breachforums.st": "breach",
    "https://carder-forum.online": "carder",
    "https://cardingforum.cx": "carding",
    "https://cardingleaks.ws": "carding",
    "https://cardvilla.cc": "cardvilla",
    "https://chitachok.fun": "chitachok",
    "https://combolist.top": "combolist",
    "https://cracked.io": "cracked",
    "https://crackia.com": "crackia",
    "https://cracking.org": "cracking",
    "https://crackingall.com": "cracking",
    "https://crackinghits.to": "crackinghits",
    "https://crackingitaly.to": "crackingitaly",
    "https://crackingx.com": "crackingx",
    "https://crackingpro.com": "crackingpro",
    "https://crackingshare.com": "crackingshare",
    "https://crackx.to": "crackx",
    "https://crime.to": "crime",
    "https://crdcrew.cc": "crdcrew",
    "https://crdpro.cc": "crdpro",
    "https://cweb.ws": "cweb",
    "https://cyberleaks.to": "cyberleaks",
    "https://cybernulled.com": "cybernulled",
    "https://darkpro.net": "darkpro",
    "https://darkstash.com": "darkstash",
    "https://dark-time.life": "dark-time",
    "https://darkwebmafias.ws": "darkwebmafias",
    "https://demonforums.net": "demonforums",
    "https://directleaks.to": "directleaks",
    "https://drdark.ru": "drdark",
    "https://eleaks.to": "eleaks",
    "https://ezcarder.cc": "ezcarder",
    "https://leakforum.org": "leakforum",
    "https://leakzone.net": "leakzone",
    "https://leakedbb.com": "leakedbb",
    "https://leech.is": "leech",
    "https://legitcarder.ru": "legitcarder",
    "https://legitcarders.ws": "legitcarders",
    "https://lolz.guru": "lolz",
    "https://niflheim.top": "niflheim",
    "https://noirth.com": "noirth",
    "https://nullcrack.store": "nullcrack",
    "https://nulled.to": "nulled",
    "https://nulled.id": "nulledid",
    "https://psylab.cc": "psylab",
    "https://prologic.su": "prologic",
    "https://russiancarder.net": "russiancarder",
    "https://shieldforum.in": "shieldforum",
    "https://sinfulsite.com": "sinfulsite",
    "https://sinister.ly": "sinisterly",
    "https://trustedsellers.ws": "trustedsellers",
    "https://underworldmafias.net": "underworldmafias",
    "https://validmarket.io": "validmarket",
    "https://verifiedcarder.net": "verifiedcarder",
    "https://vlmi.ws": "vlmi",
    "https://xss.is": "xss",
    "https://youhack.ru": "youhack"
}

app             = Flask(__name__)
latest_statuses = {"last_update":"","statuses":{}}
up_times        = {u:datetime.utcnow() for u in forums}
prev_state      = {u:"INIT" for u in forums}

# -------- HTML (değişmedi) --------
HTML = """<!DOCTYPE html><html lang='en'><head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>Forum Status Live Tracker</title>
<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap' rel='stylesheet'>
<style>
 :root{--bg:#111418;--card:#1b1f24;--border:#2c3238;--green:#16c784;--red:#ff5555;--yellow:#eab308;--cyan:#3ab7ff}
 *{box-sizing:border-box;font-family:'Inter',sans-serif}
 body{background:var(--bg);color:#d1d5db;margin:0;padding:24px;display:flex;flex-direction:column;align-items:center;min-height:100vh}
 h1{color:var(--green);margin:0 0 16px;font-size:1.8rem;text-align:center}
 .wrapper{width:100%;max-width:1000px;background:var(--card);border:1px solid var(--border);border-radius:8px;padding:16px;box-shadow:0 0 12px rgba(0,0,0,.4)}
 table{width:100%;border-collapse:collapse;table-layout:fixed}
 th,td{padding:10px;border-bottom:1px solid var(--border);text-align:left;word-break:break-all}
 thead th{font-weight:600;color:#f3f4f6;font-size:.9rem}
 tbody tr:hover{background:#24292f}
 .online{color:var(--green)}
 .offline{color:var(--red)}
 .possible{color:var(--yellow)}
 .waf{color:var(--cyan)}
 a{color:#93c5fd;text-decoration:none}
</style></head><body>
<h1>🛡️ Forum Status Live Tracker</h1>
<div class='wrapper'><table id='statusTable'>
<thead><tr><th>Status</th><th>Forum URL</th><th>Uptime</th></tr></thead><tbody></tbody></table></div>
<script>
function pri(s){return s.includes('ONLINE')?3:s.includes('LIVE')?2:s.includes('POSSIBLY')?1:0}
async function fetchStatus(){
 const resp=await fetch('/status');const data=await resp.json();if(!data.statuses)return;
 const tb=document.querySelector('#statusTable tbody');tb.innerHTML='';
 Object.entries(data.statuses).sort((a,b)=>pri(b[1].status)-pri(a[1].status)).forEach(([url,info])=>{
  const cls=info.status.includes('ONLINE')?'online':info.status.includes('LIVE')?'waf':info.status.includes('OFFLINE')?'offline':'possible';
  tb.insertAdjacentHTML('beforeend',`<tr><td class='${cls}'>${info.status}</td><td><a href='${url}' target='_blank'>${url}</a></td><td>${info.uptime}</td></tr>`);
 });
}
setInterval(fetchStatus,1000);fetchStatus();
</script></body></html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/status')
def status():
    return jsonify(latest_statuses)

async def tg(msg):
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as s:
        await s.post(url,json={"chat_id":CHAT_ID,"text":msg})

async def check(session,url,kw):
    waf_kw=["access denied","attention required","checking your browser","forbidden","blocked","cloudflare"]
    try:
        async with session.get(url,timeout=10) as r:
            t=(await r.text()).lower()
            if any(w in t for w in waf_kw):
                return url,"LIVE (Protected by WAF) 🛡️"
            return (url,"ONLINE ✅") if kw.lower() in t else (url,"POSSIBLY OFFLINE ❓")
    except:
        return url,"OFFLINE ❌"

async def monitor():
    global latest_statuses
    while True:
        now = datetime.utcnow()
        async with aiohttp.ClientSession() as s:
            res = await asyncio.gather(*[check(s,u,k) for u,k in forums.items()])
        st_map = {}
        for u,st in res:
            # uptime tracking
            if st.startswith('ONLINE') or st.startswith('LIVE'):
                up_times.setdefault(u,now)
            else:
                up_times[u]=now

            # --- Telegram transition logic ---
            prev = prev_state.get(u,'INIT')
            if prev.startswith('OFFLINE') and (st.startswith('ONLINE') or st.startswith('LIVE')):
                await tg(f"✅ BACK ONLINE: {u} → {st}")
            elif not prev.startswith('OFFLINE') and st.startswith('OFFLINE'):
                await tg(f"⚠️ OFFLINE: {u}")
            # store state
            prev_state[u] = st

            st_map[u] = {"status": st, "uptime": fmt(now - up_times[u])}

        latest_statuses = {"last_update": now.strftime('%Y-%m-%d %H:%M:%S'), "statuses": st_map}
        await asyncio.sleep(INTERVAL)

# ---------------- util / main ----------------

def fmt(d):
    m=(d.seconds%3600)//60; h=d.seconds//3600
    return f"{d.days}d {h}h" if d.days else (f"{h}h {m}m" if h else f"{m}m")

if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.create_task(monitor())
    Thread(target=lambda:app.run(host='0.0.0.0',port=PORT)).start()
    loop.run_forever()
