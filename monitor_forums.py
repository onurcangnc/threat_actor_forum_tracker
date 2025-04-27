import threading
import time
import requests
from flask import Flask
from datetime import datetime
import os

# Tüm Forumlar Listesi
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

# Telegram bilgileri
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
<<<<<<< HEAD

# HTML dosyasını kaydedeceğimiz dosya adı
HTML_FILE = "status.html"

# Kontrol aralığı
INTERVAL = 300  # 5 dakika

# Flask uygulaması
app = Flask(__name__)

@app.route('/')
def home():
    return 'Forum Tracker is Running!'
=======

# HTML dosyasını kaydedeceğimiz dosya adı
HTML_FILE = "status.html"

# Kontrol aralığı
INTERVAL = 300  # 5 dakika

# Flask uygulaması
app = Flask(__name__)


@app.route('/')
def home():
    return 'Forum Tracker is Running!'

>>>>>>> 49a996d (changed)

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        if chat_id.strip():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
<<<<<<< HEAD
            payload = {
                "chat_id": chat_id.strip(),
                "text": message
            }
=======
            payload = {"chat_id": chat_id.strip(), "text": message}
>>>>>>> 49a996d (changed)
            try:
                response = requests.post(url, json=payload)
                if response.status_code != 200:
                    print(f"Telegram mesajı gönderilemedi: {response.text}")
            except Exception as e:
                print(f"Telegram gönderim hatası: {e}")
<<<<<<< HEAD
=======

>>>>>>> 49a996d (changed)

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

<<<<<<< HEAD
=======

>>>>>>> 49a996d (changed)
def generate_html(statuses, last_update):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Forum Status Report</title>
</head>
<body>
    <h1>🛡️ Forum Status Report ({last_update})</h1>
    <ul>
"""
    for url, status in statuses.items():
        html_content += f"<li>[{status}] {url}</li>\n"

    html_content += """
    </ul>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
<<<<<<< HEAD
=======

>>>>>>> 49a996d (changed)

def monitor_forums():
    while True:
        statuses = {}
        for url, keyword in forums.items():
            status = check_forum(url, keyword)
            print(f"[{status}] {url}")
            statuses[url] = status

        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # HTML dosyasını oluştur
        generate_html(statuses, last_update)

        # 🚀 BURAYA BUNU EKLE:
        git_push()

        # Telegram raporu gönder
        report = f"🛡️ Forum Status Report ({last_update})\n\n"
        for url, stat in statuses.items():
            report += f"[{stat}] {url}\n"
        send_telegram_message(report)

        time.sleep(INTERVAL)


def git_push():
    try:
<<<<<<< HEAD
        os.system("git config --global user.email 'onurcan.genc@ug.bilkent.edu.tr'")
        os.system("git config --global user.name 'onurcangnc'")          
        os.system("git add status.html")
        os.system('git commit -m "Auto update status page" || echo "Nothing to commit"')
        os.system("git push https://{}@github.com/onurcangnc/threat_actor_forum_tracker.git main".format(os.getenv("GITHUB_TOKEN")))
=======
        os.system(
            "git config --global user.email 'onurcan.genc@ug.bilkent.edu.tr'")
        os.system("git config --global user.name 'onurcangnc'")
        os.system("git pull origin main --rebase")  # ⭐ YENİ EKLİYORUZ!
        os.system("git add status.html")
        os.system(
            'git commit -m "Auto update status page" || echo "Nothing to commit"'
        )
        os.system(
            "git push https://{}@github.com/onurcangnc/threat_actor_forum_tracker.git main"
            .format(os.getenv("GITHUB_TOKEN")))
>>>>>>> 49a996d (changed)
        print("✅ GitHub Pages güncellendi!")
    except Exception as e:
        print(f"Git push hatası: {e}")

<<<<<<< HEAD
def start_flask():
    app.run(host="0.0.0.0", port=8080)

=======

def start_flask():
    app.run(host="0.0.0.0", port=8080)


>>>>>>> 49a996d (changed)
if __name__ == "__main__":
    threading.Thread(target=monitor_forums).start()
    threading.Thread(target=start_flask).start()
import threading
import time
import requests
from flask import Flask
from datetime import datetime
import os

# Tüm Forumlar Listesi
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

# Telegram bilgileri
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

# HTML dosyası
HTML_FILE = "status.html"
INTERVAL = 300  # 5 dakika

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Forum Tracker is Running!'

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        if chat_id.strip():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id.strip(), "text": message}
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

def generate_html(statuses, last_update):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Forum Status Report</title>
</head>
<body>
    <h1>🛡️ Forum Status Report ({last_update})</h1>
    <ul>
"""
    for url, status in statuses.items():
        html_content += f"<li>[{status}] {url}</li>\n"
    html_content += """
    </ul>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

def git_push():
    try:
        os.system("git config --global user.email 'onurcan.genc@ug.bilkent.edu.tr'")
        os.system("git config --global user.name 'onurcangnc'")
        os.system("git add status.html")
        os.system('git commit -m "Auto update status page" || echo "Nothing to commit"')
        os.system("git pull origin main --rebase")
        os.system("git push https://{}@github.com/onurcangnc/threat_actor_forum_tracker.git main".format(os.getenv("GITHUB_TOKEN")))
        print("✅ GitHub Pages güncellendi!")
    except Exception as e:
        print(f"Git push hatası: {e}")

def monitor_forums():
    while True:
        statuses = {}
        for url, keyword in forums.items():
            status = check_forum(url, keyword)
            print(f"[{status}] {url}")
            statuses[url] = status

        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generate_html(statuses, last_update)
        git_push()

        report = f"🛡️ Forum Status Report ({last_update})\n\n"
        for url, stat in statuses.items():
            report += f"[{stat}] {url}\n"
        send_telegram_message(report)

        time.sleep(INTERVAL)

def start_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=monitor_forums).start()
    threading.Thread(target=start_flask).start()
