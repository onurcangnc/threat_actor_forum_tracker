import threading
import time
import requests
from flask import Flask, jsonify, render_template_string
from datetime import datetime
import os

# Forum listesi - TAM HALİ
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

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
INTERVAL = 300

app = Flask(__name__)
latest_statuses = {}

@app.route('/')
def home():
    html_page = """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Forum Status Live Tracker</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f0f0f; color: #e0e0e0; margin: 0; padding: 20px; }
            h1 { text-align: center; color: #00ff99; }
            .status { max-width: 900px; margin: 20px auto; padding: 20px; background: #1f1f1f; border-radius: 8px; box-shadow: 0 0 10px rgba(0,255,153,0.5); overflow-x: auto; }
            .online { color: #00ff00; }
            .offline { color: #ff4040; }
            .possible { color: #ffd700; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #333; }
            .highlight { animation: highlightAnim 1.5s ease; }
            @keyframes highlightAnim { from { background-color: #004d00; } to { background-color: transparent; } }
            @media (max-width: 600px) { body { padding: 10px; } .status { padding: 10px; } th, td { padding: 8px; } }
        </style>
    </head>
    <body>
        <h1>🛡️ Forum Status Live Tracker</h1>
        <div class=\"status\">
            <table id=\"statusTable\">
                <thead>
                    <tr><th>Status</th><th>Forum URL</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        <script>
            let previousData = {};
            async function fetchStatus() {
                try {
                    const response = await fetch('/status');
                    const data = await response.json();
                    const tbody = document.querySelector('#statusTable tbody');
                    tbody.innerHTML = '';
                    let sortedEntries = Object.entries(data.statuses).sort((a, b) => {
                        return (b[1].includes('ONLINE') ? 1 : 0) - (a[1].includes('ONLINE') ? 1 : 0);
                    });
                    for (const [url, status] of sortedEntries) {
                        let cssClass = status.includes('ONLINE') ? 'online' : (status.includes('OFFLINE') ? 'offline' : 'possible');
                        let highlight = previousData[url] && previousData[url] !== status ? 'highlight' : '';
                        tbody.innerHTML += `<tr class="${highlight}"><td class="${cssClass}">${status}</td><td><a href="${url}" target="_blank">${url}</a></td></tr>`;
                        previousData[url] = status;
                    }
                } catch (error) {
                    console.error('Status fetch error:', error);
                }
            }
            setInterval(fetchStatus, 5000);
            fetchStatus();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_page)

@app.route('/status')
def status():
    return jsonify(latest_statuses)

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        if chat_id.strip():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id.strip(), "text": message}
            try:
                requests.post(url, json=payload)
            except Exception as e:
                print(f"Telegram gönderim hatası: {e}")

def check_forum(url, keyword):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if keyword.lower() in response.text.lower():
                return "ONLINE ✅"
            else:
                return "POSSIBLY OFFLINE ❓ (Keyword not found)"
        else:
            return f"OFFLINE ❌ (Status {response.status_code})"
    except requests.exceptions.RequestException:
        return "OFFLINE ❌ (Connection Error)"

def monitor_forums():
    global latest_statuses
    while True:
        statuses = {}
        for url, keyword in forums.items():
            status = check_forum(url, keyword)
            statuses[url] = status

        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_statuses = {"last_update": last_update, "statuses": statuses}

        report = f"🛡️ Forum Status Report ({last_update})\n\n" + "\n".join(f"[{status}] {url}" for url, status in statuses.items())
        send_telegram_message(report)

        time.sleep(INTERVAL)

def start_flask():
    app.run(host="0.0.0.0", port=8081)

if __name__ == "__main__":
    threading.Thread(target=monitor_forums).start()
    threading.Thread(target=start_flask).start()
