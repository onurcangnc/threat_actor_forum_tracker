import requests
import time
from datetime import datetime

# Tehdit aktörü forumları ve anahtar kelimeleri
forums = {
    "https://altenens.is": "altenen",
    "https://forum.antichat.com": "antichat",
    "https://ascarding.com": "carding",
    "https://blackhatprotools.info": "blackhat",
    "https://breachforums.st": "breach",
    "https://carder-forum.online": "carder",
    "https://cardingforum.cx": "carding",
    "https://cardingleaks.ws": "carding",
    "https://cardvilla.cc": "cardvilla",
    "https://cracked.io": "cracked",
    "https://crackia.com": "crackia",
    "https://cracking.org": "cracking",
    "https://crackingall.com": "cracking",
    "https://crackinghits.to": "cracking",
    "https://crackingitaly.to": "cracking",
    "https://crackingx.com": "cracking",
    "https://crackingpro.com": "cracking",
    "https://crackingshare.com": "cracking",
    "https://crackx.to": "crackx",
    "https://crime.to": "crime",
    "https://crdcrew.cc": "crdcrew",
    "https://crdpro.cc": "crdpro",
    "https://cweb.ws": "carding",
    "https://cyberleaks.to": "leaks",
    "https://cybernulled.com": "nulled",
    "https://darkpro.net": "darkpro",
    "https://darkstash.com": "darkstash",
    "https://dark-time.life": "dark-time",
    "https://darkwebmafias.ws": "darkweb",
    "https://demonforums.net": "demon",
    "https://directleaks.to": "leaks",
    "https://drdark.ru": "drdark",
    "https://eleaks.to": "leaks",
    "https://ezcarder.cc": "carder",
    "https://leakforum.org": "leakforum",
    "https://leakzone.net": "leakzone",
    "https://leakedbb.com": "leaked",
    "https://leech.is": "leech",
    "https://legitcarder.ru": "carder",
    "https://legitcarders.ws": "carder",
    "https://lolz.guru": "lolz",
    "https://niflheim.top": "niflheim",
    "https://noirth.com": "noirth",
    "https://nullcrack.store": "crack",
    "https://nulled.to": "nulled",
    "https://nulled.id": "nulled",
    "https://psylab.cc": "psylab",
    "https://prologic.su": "prologic",
    "https://russiancarder.net": "carder",
    "https://shieldforum.in": "shield",
    "https://sinfulsite.com": "sinful",
    "https://sinister.ly": "sinister",
    "https://trustedsellers.ws": "trusted",
    "https://underworldmafias.net": "mafias",
    "https://validmarket.io": "market",
    "https://verifiedcarder.net": "carder",
    "https://vlmi.ws": "vlmi",
    "https://xss.is": "xss",
    "https://youhack.ru": "youhack"
}

# Telegram Bot Bilgileri
BOT_TOKEN = "BURAYA_BOT_TOKEN"
CHAT_IDS = ["BURAYA_CHAT_IDLER"]

# Her 5 dakikada bir çalışacak
INTERVAL = 300  # saniye

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"Telegram mesajı gönderilemedi: {response.text}")
        except Exception as e:
            print(f"Telegram hatası: {e}")

def check_forum(url, keyword):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if keyword.lower() in response.text.lower():
                return f"[ONLINE ✅] {url}"
            else:
                return f"[POSSIBLY OFFLINE ❓] {url} (Keyword '{keyword}' not found)"
        else:
            return f"[OFFLINE ❌] {url} - Status Code: {response.status_code}"
    except requests.exceptions.RequestException:
        return f"[OFFLINE ❌] {url} - Connection Error"

def monitor_forums():
    while True:
        print(f"\n--- Checking forums at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        status_list = []
        for url, keyword in forums.items():
            status = check_forum(url, keyword)
            print(status)
            status_list.append(status)
        
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_report = f"🛡️ Forum Status Report ({report_time})\n\n" + "\n".join(status_list)
        
        send_telegram_message(full_report)
        
        print(f"--- Report sent. Waiting {INTERVAL/60:.0f} minutes ---\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor_forums()
