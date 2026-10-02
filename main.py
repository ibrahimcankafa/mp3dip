import yt_dlp
import time
import os
import glob

def okubol(pat = "sarkilar.txt"):
    with open(pat, "r", encoding="utf-8") as f:
        liste = f.read().splitlines()
        return liste


# İndirilmesini istediğin şarkıların listesi
tum_satirlar = okubol()  # Orijinal satırları sakla (dosyayı güncellemek için)

# Boş satırları filtrele, zaten indirilmişleri ayır
sarki_listesi = []       # İndirilecek şarkılar
zaten_indirilen = {}     # {arama_terimi: dosya_adi} — daha önce indirilmiş

for satir in tum_satirlar:
    satir = satir.strip()
    if not satir:
        continue
    if " | " in satir:
        # Daha önce indirilmiş: "mokali | Organize x Lvbel... .mp3"
        parcalar = satir.split(" | ", 1)
        arama = parcalar[0].strip()
        dosya = parcalar[1].strip()
        zaten_indirilen[arama] = dosya
    else:
        sarki_listesi.append(satir)

# İndirilen MP3'ler için klasör oluştur (Eğer yoksa)
hedef_klasor = 'mp3'
if not os.path.exists(hedef_klasor):
    os.makedirs(hedef_klasor)

# Sonuç takibi
basarili = []
basarisiz = []  # (sarki_adi, sebep) tuple'ları

def mp3_indir(sarki_adi):
    """Şarkıyı YouTube'dan arar ve MP3 olarak indirir. Sonucu döndürür."""

    # İndirmeden önce mevcut dosyaları kaydet (sonra karşılaştırmak için)
    onceki_dosyalar = set(glob.glob(os.path.join(hedef_klasor, "*.mp3")))

    # Arama ayarları (sadece URL bulmak için, indirmek için değil)
    arama_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': 'in_playlist',  # Sadece URL'leri al, video detaylarını çözme
        'playlistend': 1,               # Sadece 1 sonuç
    }

    # İndirme ayarları
    indirme_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{hedef_klasor}/%(title)s.%(ext)s', # Dosya adı ve yolu
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Ses kalitesi (192 veya 320 yapabilirsin)
        }],
        'noplaylist': True,
        'quiet': True, # Ekrana gereksiz log basmasını engeller, sadece kendi printlerimizi görürüz
        'no_warnings': True,
        'playlistend': 1,  # Güvenlik: asla birden fazla video indirme
    }

    try:
        # ADIM 1: Önce arama yapıp sadece 1 video URL'si bul
        print(f"▶ Aranıyor: {sarki_adi}...")
        with yt_dlp.YoutubeDL(arama_opts) as ydl_arama:
            info = ydl_arama.extract_info(f"ytsearch1:{sarki_adi}", download=False)

            # ytsearch sonucu 'entries' listesi döner
            entries = info.get('entries', []) if info else []
            # Lazy iterator ise listeye çevir ve sadece ilkini al
            entries = list(entries)[:1] if entries else []

            if not entries:
                sebep = "YouTube aramasında sonuç bulunamadı"
                print(f"✖ {sarki_adi}: {sebep}")
                basarisiz.append((sarki_adi, sebep))
                return

            video = entries[0]
            video_baslik = video.get('title', 'Bilinmeyen')
            video_url = video.get('webpage_url') or video.get('url', '')

            if not video_url:
                sebep = "Video URL'si alınamadı"
                print(f"✖ {sarki_adi}: {sebep}")
                basarisiz.append((sarki_adi, sebep))
                return

            # URL'nin tam YouTube linki olduğundan emin ol
            if not video_url.startswith('http'):
                video_id = video.get('id', video_url)
                video_url = f"https://www.youtube.com/watch?v={video_id}"

        # ADIM 2: Bulunan TEK videoyu indir (ayrı YoutubeDL instance'ı ile)
        print(f"  ↳ Bulunan video: {video_baslik}")
        print(f"  ↳ İndiriliyor...")
        with yt_dlp.YoutubeDL(indirme_opts) as ydl_indir:
            ret = ydl_indir.download([video_url])

        # İndirme sonrası yeni dosya oluştu mu kontrol et
        sonraki_dosyalar = set(glob.glob(os.path.join(hedef_klasor, "*.mp3")))
        yeni_dosyalar = sonraki_dosyalar - onceki_dosyalar

        if ret != 0:
            sebep = f"yt-dlp indirme hatası (kod: {ret})"
            print(f"✖ {sarki_adi}: {sebep}")
            basarisiz.append((sarki_adi, sebep))
            return

        if not yeni_dosyalar:
            sebep = "İndirme tamamlandı gibi görünüyor ama MP3 dosyası oluşmadı (FFmpeg sorunu olabilir)"
            print(f"⚠ {sarki_adi}: {sebep}")
            basarisiz.append((sarki_adi, sebep))
            return

        dosya_adi = os.path.basename(list(yeni_dosyalar)[0])
        print(f"✔ Başarıyla indirildi: {sarki_adi} → {dosya_adi}")
        basarili.append((sarki_adi, dosya_adi))

    except yt_dlp.utils.DownloadError as e:
        hata_mesaji = str(e)
        if "No video results" in hata_mesaji or "no results" in hata_mesaji.lower():
            sebep = "YouTube aramasında sonuç bulunamadı"
        elif "unavailable" in hata_mesaji.lower():
            sebep = "Video kullanılamıyor (kaldırılmış veya bölge kısıtlaması)"
        elif "private" in hata_mesaji.lower():
            sebep = "Video gizli (private)"
        elif "age" in hata_mesaji.lower():
            sebep = "Yaş kısıtlamalı video (giriş yapılması gerekiyor)"
        else:
            sebep = f"İndirme hatası: {hata_mesaji}"
        print(f"✖ {sarki_adi}: {sebep}")
        basarisiz.append((sarki_adi, sebep))
    except Exception as e:
        sebep = f"Beklenmeyen hata: {e}"
        print(f"✖ {sarki_adi}: {sebep}")
        basarisiz.append((sarki_adi, sebep))


# Zaten indirilmiş şarkıları göster
if zaten_indirilen:
    print(f"⏭ {len(zaten_indirilen)} şarkı zaten indirilmiş, atlanıyor:")
    for arama, dosya in zaten_indirilen.items():
        print(f"   • {arama} → {dosya}")
    print()

# Listeyi sırayla döngüye sok ve indir
if sarki_listesi:
    print(f"🎵 Toplam {len(sarki_listesi)} şarkı indirilecek...\n")

    for index, sarki in enumerate(sarki_listesi):
        print(f"[{index + 1}/{len(sarki_listesi)}]", end=" ")
        mp3_indir(sarki)
        
        # Listenin son şarkısına gelinmediyse 3 saniye bekle
        if index < len(sarki_listesi) - 1:
            print("⏳ Sıradaki şarkıya geçmeden önce 3 saniye bekleniyor...\n")
            time.sleep(3)
else:
    print("ℹ İndirilecek yeni şarkı yok.")

# ═══════════════════════════════════════════
#  sarkilar.txt'yi güncelle
# ═══════════════════════════════════════════
# Başarılı indirmeleri dict'e çevir: {arama_terimi: dosya_adi}
basarili_dict = {sarki: dosya for sarki, dosya in basarili}

# Tüm satırları yeniden yaz
with open("sarkilar.txt", "w", encoding="utf-8") as f:
    for satir in tum_satirlar:
        satir_temiz = satir.strip()
        if not satir_temiz:
            f.write("\n")
            continue
        if " | " in satir_temiz:
            # Zaten eşlenmiş satır, olduğu gibi bırak
            f.write(satir_temiz + "\n")
        elif satir_temiz in basarili_dict:
            # Yeni indirilen — dosya adını yanına ekle
            f.write(f"{satir_temiz} | {basarili_dict[satir_temiz]}\n")
        else:
            # İndirilemedi, olduğu gibi bırak (bir sonraki çalıştırmada tekrar denenecek)
            f.write(satir_temiz + "\n")

print("\n📝 sarkilar.txt güncellendi.")

# ═══════════════════════════════════════════
#  SONUÇ RAPORU
# ═══════════════════════════════════════════
print("\n" + "═" * 50)
print("  📊 İNDİRME RAPORU")
print("═" * 50)
toplam = len(sarki_listesi) + len(zaten_indirilen)
print(f"  ✔ Başarılı: {len(basarili)}/{len(sarki_listesi)}")
print(f"  ⏭ Zaten indirilmiş: {len(zaten_indirilen)}")
print(f"  ✖ Başarısız: {len(basarisiz)}/{len(sarki_listesi)}")
print("═" * 50)

if basarili:
    print("\n✔ İndirilen şarkılar:")
    for sarki, dosya in basarili:
        print(f"   • {sarki} → {dosya}")

if basarisiz:
    print("\n✖ İndirilemeyen şarkılar:")
    for sarki, sebep in basarisiz:
        print(f"   • {sarki}")
        print(f"     Sebep: {sebep}")

    # Başarısız olanları dosyaya kaydet
    with open("indirilemeyenler.txt", "w", encoding="utf-8") as f:
        f.write("# İndirilemeyen Şarkılar\n")
        f.write(f"# Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for sarki, sebep in basarisiz:
            f.write(f"{sarki} | Sebep: {sebep}\n")
    print("\n📝 Başarısız liste 'indirilemeyenler.txt' dosyasına kaydedildi.")

if not basarisiz:
    print("\n🎉 Tüm şarkılar başarıyla indirildi!")
else:
    print(f"\n🎉 İndirme işlemleri tamamlandı! ({len(basarisiz)} şarkı indirilemedi)")