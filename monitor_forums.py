# monitor.py
import asyncio, aiohttp
from flask import Flask, jsonify, render_template_string, Response
from datetime import datetime, timezone
from threading import Thread
from collections import defaultdict
import time
from flask import Flask, render_template
import json

INTERVAL = 5
PORT = 8082

forums = {
    "https://4cheat.ru/": "4cheat",
    "https://589forum.org/": "589forum",
    "https://alligator.cash/": "alligator",
    "https://altenens.is": "altenen",
    "https://forum.antichat.com": "antichat",
    "https://antimigalki.space": "antimigalki",
    "https://arbitraj-forum.ru": "arbitraj",
    "https://ascarding.com": "ascarding",
    "https://astropid.net": "astropid",
    "https://bdfclub.com": "bdf",
    "https://bhcforums.cc": "bhc",
    "https://bhf.ee": "bhf",
    "https://bhf.im": "bhf",
    "http://bitcoinfor.ru": "bitcoinfo.ru",
    "https://forum.bits.media": "bits.media",
    "https://blackbiz.top": "blackbiz",
    "https://blackbones.net": "blackbones",
    "https://blackforums.me": "blackforums",
    "https://blackforums.net": "blackforums",
    "https://blackforums.ru": "blackforums",
    "https://blackhacker.pw": "blackhacker",
    "https://blackhatpakistan.net": "blackhatpakistan",
    "https://www.blackhatprotools.info/": "blackhatprotools",
    "https://blackhatworld.com": "blackhatworld",
    "https://breached.ws": "breached",
    "http://breached.ws": "breach",
    "https://carders.biz": "carders.biz",
    "https://center-club.io": "center",
    "https://chitachok.ru": "chitachok",
    "https://comfybox.floofey.dog": "comfybox",
    "https://coockie.pro": "cookiepro",
    "https://cracked.sh": "cracked",
    "https://cracking.org": "cracking",
    "https://crackingmafia.is": "cracking",
    "https://www.crackingpro.com": "cracking",
    "https://crackingx.com": "cracking",
    "https://crdpro.cc": "crdpro",
    "http://crime.to": "crimenetwork",
    "http://crimenow.is": "crimenow",
    "https://crimestate.cc": "crimestate",
    "https://forum.cryptocurrency.tech": "cryptocurrency.tech",
    "https://forum.cryptoff.org": "cryptoff",
    "http://cryptogid.org": "cryptogid",
    "https://cvvbrd.info": "cvv_board",
    "https://cybhack.net": "cybhack",
    "https://d4rkforums.net": "d4rkforums",
    "https://dark2web.net": "dark2web",
    "https://darkclub.pw": "darkclub",
    "https://darkforum.in": "darkforum",
    "https://darkforum.net": "darkforum",
    "https://darkforums.st": "darkforums",
    "https://darkmoney.lc": "darkmoney",
    "https://darknet.ug": "darknet",
    "https://darkpid.com": "darkpid",
    "https://darkpro.net/": "darkpro",
    "https://darkzone.uk": "darkzone",
    "https://datacloud.space": "datacloud",
    "https://dataforums.co": "dataforums",
    "https://dedicatet.com": "dedicatet",
    "https://demonforums.net": "demonforums",
    "https://drdark.ru": "drdark",
    "https://at.dublikat.club": "dublikat.club",
    "https://dumped.to": "dumped",
    "https://dumpforums.to/": "dumpforums",
    "https://eleaks.to": "eleaks",
    "https://www.enclave.cc": "enclave",
    "https://endway.su": "endway",
    "https://eternia.to": "eternia",
    "https://evilarmy.in": "evilarmy",
    "https://evil-zone.org": "evilzone",
    "https://evilx.su/forum/": "evilx",
    "https://forum.exodusmarket.io": "exodus",
    "https://exploit.in": "exploit.in",
    "https://exploitforums.net": "exploit",
    "https://exploits.ws": "exploits.ws",
    "https://ezcarder.is/": "ezcarder",
    "https://forumteam.online": "forumteam.online",
    "https://forumteam.top": "forumteam.top",
    "https://fssquad.com": "fssquad",
    "https://getrekt.io": "getrekt",
    "https://hackforums.net/index.php": "hackforums",
    "https://hackingfather.com/": "hackingfather",
    "https://hackonology.com/forum/": "hackonology",
    "https://hacksnation.com/": "hacksnation",
    "http://hohekammer.cc": "hohekammer",
    "https://in4.bz": "in4bz",
    "https://incidious.se": "incidious",
    "https://infected-zone.com": "infected",
    "https://infinity.ink": "infinity",
    "http://kcc.cat": "kcc",
    "https://forum.kkksec.com": "kkksecforum",
    "http://korovka.cc": "korovka",
    "https://korovka.cc": "korovka",
    "https://lampeduza.la": "lampeduza",
    "https://leadlab.top": "lead",
    "https://leakbase.la": "leakbase",
    "https://leakbase.org": "leakbase",
    "https://leakforums.su": "leak",
    "https://leaks.so": "leaks.so",
    "https://leak.sx": "leaks.sx",
    "https://leaky.pro/": "leaky.pro",
    "https://leech.is": "leech",
    "https://level23hacktools.com/hackers": "level23hacktools",
    "https://linkpass.info": "linkpass",
    "https://lolz.guru": "lolz",
    "http://lowendtalk.com": "lowendtalk",
    "https://nulledbb.com": "nulledbb",
    "https://nulledx.to": "nulledx",
    "https://olvx.cc": "olvx",
    "https://omerta.cc": "omerta",
    "https://omerta.cx": "omerta",
    "https://omert.cc": "omerta",
    "https://onniforums.com": "onniforums",
    "https://openssource.org": "openssource",
    "https://patched.to": "patched.to",
    "https://payload.sh": "payload.sh",
    "https://phish.pw": "phish.pw",
    "https://phreaker.info": "phreaker",
    "https://s1.piratebuhta.net": "piratebuhta",
    "https://probiv.one": "probiv",
    "https://procrd.pw": "procrd",
    "https://prologic.su": "prologic",
    "https://proton.sc": "proton",
    "https://pshack.org": "pshack",
    "https://ramp4u.io": "ramp",
    "https://rebreached.vc": "rebreached",
    "https://reversing.center": "reversing",
    "https://www.rf-cheats.ru": "rf-cheat",
    "https://rootsploit.org": "rootsploit",
    "https://darknet.rutor.nl": "rutor",
    "http://rutor.info": "rutor",
    "http://rutor.is": "rutor",
    "https://seopirat.club": "seopirat",
    "https://sinfulsite.com": "sinful",
    "https://sinister.ly": "sinister",
    "https://skynetzone.biz": "skynetzone.biz",
    "https://skynetzone.pw": "skynetzone.pw",
    "http://forum.softxaker.ru": "softxaker",
    "https://spyhackerz.org": "spyhackerz",
    "https://sqli.cloud": "sqli",
    "https://stressedforums.pw": "stressed",
    "https://thegoodlife.to": "thegoodlife",
    "https://thejavasea.com": "thejavasea",
    "https://toolba.se": "toolbase",
    "https://trafa.net": "trafa",
    "https://www.turkhackteam.org": "turkhackteam",
    "https://vavilon.cc": "vavilon",
    "https://vedenet.online": "vedenet",
    "https://veryleaks.cz": "veryleaks",
    "https://v-h.guru": "v-h.guru",
    "https://vlmi.ws": "vlmi",
    "https://vsemmoney.com": "vsemmoney",
    "https://wwh-club.io": "wwhclub",
    "https://xforums.st": "xforums",
    "https://xreactor.org": "xreactor",
    "https://xss.is": "xss",
    "https://youhack.xyz": "youhack",
    "https://zdl.pw": "zdl",
    "https://kittyforums.to/": "kittyforums"
}

status_data = defaultdict(lambda: {
    "status": "UNKNOWN",
    "since": None,
    "uptime": "NOT ACCESSIBLE"
})

async def check_status(url):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, allow_redirects=True) as resp:
                if resp.status == 200:
                    return "ONLINE"
                elif resp.status in [403, 406]:
                    return "WAF"
                else:
                    return "POSSIBLE"
    except Exception:
        return "OFFLINE"

def format_duration(iso_since):
    since = datetime.fromisoformat(iso_since)
    diff = datetime.now(timezone.utc) - since
    total = int(diff.total_seconds())
    s = total % 60
    m = (total // 60) % 60
    h = (total // 3600) % 24
    d = (total // 86400) % 30
    mo = (total // 2592000)
    parts = []
    if mo: parts.append(f"{mo}ay")
    if d: parts.append(f"{d}g")
    if h: parts.append(f"{h}s")
    if m: parts.append(f"{m}d")
    if parts == [] or s: parts.append(f"{s}s")
    return "⏱ " + " ".join(parts)

async def check_forums():
    while True:
        for url in forums:
            new_status = await check_status(url)
            current = status_data[url]

            if new_status == "OFFLINE":
                current["status"] = "OFFLINE"
                current["since"] = None
                current["uptime"] = "NOT ACCESSIBLE"
                continue

            # ONLINE'e geçtiyse sayaç başlat
            if new_status == "ONLINE" and current["status"] != "ONLINE":
                current["since"] = datetime.now(timezone.utc).isoformat()

            # since varsa uptime güncelle
            if current["since"]:
                current["uptime"] = format_duration(current["since"])
            else:
                current["uptime"] = "NOT ACCESSIBLE"

            current["status"] = new_status
        await asyncio.sleep(INTERVAL)

app = Flask(__name__)

def sse_stream():
    while True:
        import json
        yield f"data: {json.dumps(status_data)}\n\n"
        time.sleep(2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream")
def stream():
    return Response(sse_stream(), mimetype="text/event-stream")

def start_loop():
    asyncio.run(check_forums())

if __name__ == "__main__":
    Thread(target=start_loop).start()
    app.run(host="0.0.0.0", port=PORT)