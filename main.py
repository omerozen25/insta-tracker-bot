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
    "cristiano",
    "leomessi",
    "therock",
    "selenagomez",
    "kyliejenner",
    "arianagrande",
    "kimkardashian",
    "beyonce",
    "neymarjr",
    "virat.kohli",
    "khloekardashian",
    "kendalljenner",
    "jlo",
    "taylorswift",
    "kourtneykardash",
    "simeone",
    "mrancelotti",

    "kingjames",
    "k.mbappe",
    "davidbeckham",
    "ronaldinho",
    "marcelotwelve",
    "karimbenzema",
    "garethbale11",
    "floydmayweather",
    "lewishamilton",
    "m_phelps00",
    "sergioramos",
    "hakancalhanoglu",
    "mb459",
    "virendersehwag",

    "katyperry",
    "badgalriri",
    "shakira",
    "dualipa",
    "champagnepapi",
    "chrisbrownofficial",
    "adele",
    "rauwalejandro",
    "camila_cabello",
    "sza",
    "jbalvin",
    "snoopdogg",
    "usher",
    "jennierubyjane",
    "roses_are_rosie",
    "uarmyhope",
    "thv",
    "jungkook.97",
    "bts.bighitofficial",
    "g_dragon",

    "willsmith",
    "angelinajolie",
    "vancityreynolds",
    "chrishemsworth",
    "emmawatson",
    "tomholland2013",
    "robertdowneyjr",
    "gal_gadot",
    "vindiesel",
    "leodicaprio",
    "tomcruise",
    "ana_d_armas",
    "margotrobbieofficial",
    "hrithikroshan",
    "aishwaryaraibachchan_arb",
    "deepikapadukone",
    "shraddhakapoor",
    "katrinakaif",
    "aliaabhatt",
    "akshaykumar",
    "ranveersingh",

    "mrbeast",
    "ellendegeneres",
    "jimmyfallon",
    "oprah",
    "parishilton",
    "gigihadid",
    "bellahadid",
    "haileybieber",
    "zacefron",
    "ashleygraham",
    "tyrabanks",
    "danbilzerian",
    "loganpaul",
    "jakepaul",
    "charlidamelio",
    "addisonrae",
    "khaby00",
    "lisaandlena",
    "noahcentineo",

    "jeffbezos",
    "richardbranson",
    "garyvee",
    "mariotestino",
    "barackobama",
    "michelleobama",
    "theellenshow",
    "ted",
    "nasa",

    "nike",
    "natgeo",
    "realmadrid",
    "fcbarcelona",
    "championsleague",
    "nba",
    "premierleague",
    "victoriassecret",
    "adidasfootball",
    "marvel",
    "espn",
    "houseofhighlights",

    # --- Real Madrid oyuncuları ---
    "thibautcourtois",
    "dani.carvajal.2",
    "edermilitao",
    "davidalaba",
    "trent",
    "toniruediger",
    "ferland_mendy",
    "deanhuijsen",
    "judebellingham",
    "camavinga",
    "fedevalverde",
    "aurelientchm",
    "ardaguler",
    "daniceballos4",
    "vinijr",
    "endrick",
    "rodrygogoes",
    "gonzalogarcia7_",
    "brahim",
    "franco.mastantuono",

    # --- Barcelona oyuncuları ---
    "materstegen",
    "__joangarcia",
    "wojciech.szczesny1",
    "alejandrobalde",
    "ronaldaraujo_4",
    "paucubarsi",
    "andreaschristensen3",
    "jkeey4",
    "ericgm3",
    "pablogavi",
    "pedri",
    "daniolmo",
    "frenkiedejong",
    "marcbernal_",
    "ferrantorres",
    "_rl9",
    "lamineyamal",
    "raphinha",
    "marcusrashford",
    "roony",

    # --- PSG / Diğer büyük kulüp oyuncuları ---
    "achrafhakimi",
    "marquinhosm5",
    "vitinha",
    "goncaloramos88",
    "kvara7",
    "kanginleeoficial",
    "lucashernandez21",
    "nunomendes_5",
    "fabianruiz52",
    "_lc30_",
    "illiazabarnyi",

    # --- Manchester City ---
    "donnarumma",
    "rubendias",
    "johnstones5",
    "nathanake",
    "josko_gvardiol",
    "philfoden",
    "jackgrealish",
    "erling",
    "bernardocarvalhosilva",

    # --- Liverpool / Premier Lig karması ---
    "mosalah",
    "virgilvandijk",
    "alissonbecker",
    "darwin_n9",
    "alex_isak",
    "fedexchiesa",
    "codymathesgakpo",
    "alemacallister",
    "szoboszlaidominik",

    # --- Bayern Münih vs. ---
    "harrykane",
    "joshua.kimmich",
    "leon_goretzka",
    "jamalmusiala10",
    "alphonsodavies",
    "sergegnabry",
    "upamecano",
    "m.olise",

    # --- Juventus ---
    "locamanuel73",
    "kenanyildiz_official",

    # --- Milan ---
    "iamrafaeleao93",
    "magicmikemaignan",
    "cmpulisic",
    "theo3hernandez",
    "adrienrabiot_25",

    # --- Inter ---
    "lautaromartinez",
    "nicolo_barella",
    "yannsommer",
    "alessandrobastoni",
    "thuram",

    # --- Arsenal ---
    "bukayosaka87",
    "odegaard.98",
    "dejesusoficial",
    "gabriel.martinelli",
    "declanrice",

    # --- 🌍 EKLENEN DÜNYA ÇAPINDA MEGA ÜNLÜLER ---
    "lilbieber",
    "nickiminaj",
    "mileycyrus",
    "billieeilish",
    "iamcardib",
    "badbunnypr",
    "ladygaga",
    "zendaya",
    "kevinhart4real",
    "ddlovato",
    "lalalalisa_m",
    "sooyaaa__",
    "stephencurry30",
    "thenotoriousmma",
    "narendramodi",
    "priyankachopra",
    "maluma",
    "karolg",
    "dojacat",
    "travisscott",
    "shawnmendes",
    "zayn",
    "anitta",
    "paulpogba",
    "jenniferaniston",
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
    """API'den kullanıcının takip ettiklerini çeker. 401/403 hatalarında mail gönderir."""
    payload = {"username": username, "amount": 100}
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        
        if response.status_code != 200:
            error_message = f"API Hatası ({username}): Status Code {response.status_code}"
            print(f"⚠️ {error_message}")

            # SADECE 401 (Unauthorized) veya 403 (Forbidden) ise mail gönder!
            if response.status_code in [401, 403]: 
                subject = f"🚨 KRİTİK HATA: TOKEN SORUNU ({response.status_code})"
                body = (
                    f"Takip botu çalışırken kritik bir hata oluştu:\n\n"
                    f"Kullanıcı: {username}\n"
                    f"Hata Kodu: {response.status_code}\n"
                    f"Açıklama: Bearer Token'ın süresi dolmuş veya geçersiz olmuş olabilir.\n"
                    f"Lütfen GitHub Secrets'taki SUPABASE_TOKEN'ı güncelleyin."
                )
                # Hata mailini gönder
                send_email(subject, body)
                
            return None # Diğer tüm hatalarda (500, 502, vb.) mail atmadan devam eder.

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
        # Bağlantı hatasında mail göndermez, sadece konsola yazar
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
