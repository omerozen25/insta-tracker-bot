import requests
import json
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =================================================================
# --- AYARLAR: KULLANICI BİLGİLERİ İLE ENTEGRE EDİLMİŞTİR (LOKAL TEST İÇİN) ---
# =================================================================

# Takip edilecek kullanıcı listesi
TARGET_USERS = [
    # --- 👑 ZİRVE SPOR & MEDYA FENOMENLERİ (MUTLAK TAKİP) ---
    "cristiano", "leomessi", "therock", "selenagomez", "kyliejenner", 
    "arianagrande", "kimkardashian", "beyonce", "neymarjr", "virat.kohli", 
    "khloekardashian", "kendalljenner", "jlo", "taylorswift", "justinbieber", "kourtneykardash", "simeone", "mrancelotti"
    
    # --- ⚽ EK SPOR DÜNYASI ---
    "kingjames", "k.mbappe", "davidbeckham", "ronaldinho", "marcelotwelve",
    "karimbenzema", "garethbale11", "floydmayweather", "lewishamilton",
    "m_phelps00", "sergioramos", "zlatanibrahimovic", "neuer",
    "mesutozil", "hakancalhanoglu", "mb459", "virendersehwag",
    
    # --- 🎤 MÜZİK İKONLARI VE K-POP ---
    "mileycyrus", "katyperry", "badgalriri", "billieeilish", "shakira",
    "dualipa", "champagnepapi", "chrisbrownofficial", "adele", "nickiminaj",
    "rauwalejandro", "camila_cabello", "sza", "jbalvin", "snoopdogg",
    "usher", "jennierubyjane", "sooyaaa__", "roses_are_rosie", "uarmyhope",
    "thv", "jungkook.97", "bts.bighitofficial", "g_dragon",

    # --- 🎬 HOLLYWOOD VE SİNEMA ---
    "willsmith", "angelinajolie", "vancityreynolds", "chrishemsworth",
    "emmawatson", "tomholland2013", "robertdowneyjr", "gal_gadot",
    "vindiesel", "leodicaprio", "chrispratt", "tomcruise", "jasonstatham",
    "ana_d_armas", "margotrobbieofficial", "hrithikroshan", "aishwaryaraibachchan_arb",
    "deepikapadukone", "shraddhakapoor", "katrinakaif", "aliaabhatt",
    "akshaykumar", "ranveersingh",

    # --- 📺 TV VE KÜRESEL İÇERİK ÜRETİCİLERİ ---
    "mrbeast", "ellendegeneres", "jimmyfallon", "oprah", "parishilton",
    "gigihadid", "bellahadid", "haileybieber", "zacefron", "ashleygraham",
    "tyrabanks", "danbilzerian", "loganpaul", "jakepaul", "charlidamelio",
    "addisonrae", "khaby00", "theweeknd", "lisaandlena", "noahcentineo",

    # --- 💼 İŞ DÜNYASI VE DİĞER ETKİLİ İSİMLER ---
    "jeffbezos", "richardbranson", "elonmusk", "garyvee", "mariotestino",
    "barackobama", "michelleobama", "theellenshow", "ted", "nasa",

    # --- KURUMSAL HESAPLAR ---
    "nike", "natgeo", "realmadrid", "fcbarcelona", "championsleague",
    "nba", "premierleague", "victoriassecret", "adidasfootball",
    "marvel", "espn", "houseofhighlights"
] 

# API ve Token Bilgileri
API_URL = "https://jydgtalarwcfcailwvha.supabase.co/functions/v1/fetch-preview-following"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp5ZGd0YWxhcndjZmNhaWx3dmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5OTg0NTQsImV4cCI6MjA3MzU3NDQ1NH0.QWGE4HC5b-JyBTBCB2D3kTKAdoyQHBj11yhOO0ahzys"

# GMAIL BİLGİLERİNİZ
GMAIL_PASSWORD = "futbsmjwcbkgapib" 
GMAIL_USER = "omerozen336@gmail.com" 
RECEIVER_EMAIL = "omerozen336@gmail.com" 

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# =================================================================
# --- FONKSİYONLAR ---
# =================================================================

def send_email(subject, body):
    """Mail gönderme fonksiyonu"""
    if not GMAIL_USER or not GMAIL_PASSWORD or not RECEIVER_EMAIL:
        print("Mail ayarları eksik. Mail gönderilemedi.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, RECEIVER_EMAIL, text)
        server.quit()
        print("📧 Mail başarıyla gönderildi!")
    except Exception as e:
        print(f"❌ Mail gönderme hatası: {e}. Uygulama şifrenizi kontrol edin.")

def get_current_following(username):
    """API'den kullanıcının takip ettiklerini çeker. API hatası durumunda mail gönderir."""
    payload = {"username": username, "amount": 100}
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        
        if response.status_code != 200:
            error_message = f"API Hatası ({username}): Status Code {response.status_code}"
            print(f"⚠️ {error_message}")

            # Kritik API Hatası Kontrolü (401/403 Token sorunu veya 5xx Sunucu sorunu)
            if response.status_code in [401, 403, 500, 502]: 
                subject = f"🚨 KRİTİK HATA: TOKEN VEYA API BAĞLANTI SORUNU ({response.status_code})"
                body = (
                    f"Takip botu çalışırken kritik bir hata oluştu:\n\n"
                    f"Kullanıcı: {username}\n"
                    f"Hata Kodu: {response.status_code}\n"
                    f"Açıklama: API isteği başarısız oldu. Eğer hata kodu 401 veya 403 ise, Bearer Token'ın süresi dolmuş olabilir. Lütfen token'ı güncelleyin."
                )
                # Hata mailini gönder
                send_email(subject, body)
                
            return None

        data = response.json()
        following_list = []
        
        if "data" in data and "items" in data["data"]:
            for item in data["data"]["items"]:
                if "username" in item:
                    following_list.append(item["username"])
            return following_list
        else:
            print(f"⚠️ Veri yapısı beklenildiği gibi değil ({username}).")
            return []

    except requests.exceptions.RequestException as e:
        print(f"❌ Bağlantı hatası ({username}): {e}")
        
        # Bağlantı kesintilerinde de mail gönder (API URL yanlış olabilir)
        subject = f"🚨 KRİTİK HATA: İNTERNET VEYA ADRES SORUNU"
        body = f"Takip botu çalışırken bir bağlantı hatası oluştu:\n\nHata: {e}\n\nLütfen API URL'sini kontrol edin."
        send_email(subject, body)

        return None

def run_tracker():
    """Takip listesini kontrol eder ve değişiklikleri kaydeder/bildirir."""
    
    if not os.path.exists("data"):
        os.makedirs("data")

    print(f"--- Instagram Takip Botu Çalışıyor ({len(TARGET_USERS)} Hedef) ---")

    for user in TARGET_USERS:
        current_list = get_current_following(user)
        
        if current_list is None:
            continue # Hata varsa veya veri alınamadıysa bu kullanıcıyı geç

        file_path = f"data/{user}_history.json"
        
        old_list = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    old_list = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Hata: {user} history dosyası bozuk. Yeniden oluşturulacak.")

        old_set = set(old_list)
        new_set = set(current_list)

        added = new_set - old_set
        removed = old_set - new_set
        
        # --- Mail Gönder (Takip Değişikliği Durumunda) ---
        if added or removed:
            mail_subject = f"🚨 Instagram Alarm: {user} Hareketlilik Var!"
            mail_body = f"Kullanıcı: {user}\n\n"
            
            if added:
                mail_body += "➕ YENİ TAKİP EDİLENLER:\n"
                for person in added:
                    mail_body += f"- {person}\n"
                print(f"🚨 {user} yeni takip: {added}")
            
            if removed:
                mail_body += "\n➖ TAKİPTEN ÇIKARILANLAR:\n"
                for person in removed:
                    mail_body += f"- {person}\n"
                print(f"❌ {user} takipten çıkma: {removed}")
            
            send_email(mail_subject, mail_body)
        else:
            print(f"✅ {user} için değişiklik yok.")

        # Dosyayı güncelle
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(current_list, f, indent=4)
        
        time.sleep(15)

if __name__ == "__main__":
    run_tracker()
