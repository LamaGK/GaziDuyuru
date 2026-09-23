import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

MYO_URL = "https://kazanmyo.gazi.edu.tr/view/announcements"
BOLUM_URL = "https://kazanmyo-elk.gazi.edu.tr/" # Kendi bölüm URL'in

HEADERS = {"User-Agent": "Mozilla/5.0"}

def duyuru_cek(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        duyurular = []
        
        # Sayfadaki duyuru linklerini yakala
        for item in soup.select(".announcement-item a, .post-title a, .duyuru-listesi a"):
            baslik = item.text.strip()
            link = item.get("href")
            if link and not link.startswith("http"):
                link = "https://kazanmyo.gazi.edu.tr" + link
            
            if baslik and link and {"baslik": baslik, "link": link} not in duyurular:
                duyurular.append({"baslik": baslik, "link": link})
                
        return duyurular[:15] # Son 15 duyuruyu al
    except Exception as e:
        print(f"Hata ({url}): {e}")
        return []

if __name__ == "__main__":
    veri = {
        "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "myo": duyuru_cek(MYO_URL),
        "bolum": duyuru_cek(BOLUM_URL)
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)