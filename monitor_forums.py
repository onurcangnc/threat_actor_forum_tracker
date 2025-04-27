import threading
import time
import requests
from flask import Flask, request, redirect, url_for, session, jsonify
from datetime import datetime
import os

# Tüm forumlar (senin verdiğin tam liste)
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

# Telegram ve login için environment secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
USERNAME = os.getenv("TRACKER_USERNAME")
PASSWORD = os.getenv("TRACKER_PASSWORD")

# Flask secret key
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "defaultsecretkey")

# Interval (saniye cinsinden) - 5 dakika
INTERVAL = 300

# Forum statusları
forum_statuses = {}

# Flask uygulaması
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

@app.route('/')
def home():
    return 'Threat Actor Forum Tracker is Running!'

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for('status'))
        else:
            return "❌ Wrong username or password.", 401
    return '''
        <h2>Login</h2>
        <form method="post">
            Username: <input type="text" name="username" required><br><br>
            Password: <input type="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect(url_for('login'))

@app.route('/status')
def status():
    if not session.get("logged_in"):
        return redirect(url_for('login'))
    return jsonify(forum_statuses)

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        if chat_id.strip():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": chat_id.strip(),
                "text": message
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code != 200:
                    print(f"Telegram mesajı gönderilemedi: {response.text}")
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
    global forum_statuses
    while True:
        statuses = {}
        for url, keyword in forums.items():
            status = check_forum(url, keyword)
            print(f"[{status}] {url}")
            statuses[url] = status

        forum_statuses = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "forums": statuses
        }

        report = f"🛡️ Forum Status Report ({forum_statuses['last_update']})\n\n"
        for url, stat in statuses.items():
            report += f"[{stat}] {url}\n"

        send_telegram_message(report)

        time.sleep(INTERVAL)

def start_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=monitor_forums).start()
    threading.Thread(target=start_flask).start()
