# 🎵 mp3dip

YouTube'dan toplu şarkı indirme aracı. Şarkı isimlerini bir txt dosyasına yaz, çalıştır, gerisini o halleder.

## Özellikler

- 🔍 **YouTube arama** — Şarkı adını yaz, YouTube'da aratıp en üstteki sonucu indirir
- 🎧 **MP3 dönüştürme** — İndirilen ses dosyalarını otomatik olarak 192kbps MP3'e çevirir
- 📝 **Akıllı takip** — İndirilen şarkıların dosya adını `sarkilar.txt`'ye kaydeder
- ⏭ **Tekrar indirmez** — Daha önce indirilmiş şarkıları otomatik atlar
- 📊 **Detaylı rapor** — Her çalıştırmada başarılı/başarısız indirme özeti gösterir
- ❌ **Hata kaydı** — İndirilemeyen şarkılar sebebiyle birlikte `indirilemeyenler.txt`'ye kaydedilir

## Gereksinimler

- **Python 3.7+**
- **FFmpeg** — ses dönüştürme için gerekli ([ffmpeg.org](https://ffmpeg.org/download.html))
- **yt-dlp** — YouTube indirme kütüphanesi

## Kurulum

```bash
# Repoyu klonla
git clone https://github.com/kullanici/mp3dip.git
cd mp3dip

# Sanal ortam oluştur (opsiyonel ama önerilir)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Bağımlılıkları kur
pip install yt-dlp
```

> **Not:** FFmpeg'in sistem PATH'inde olması gerekiyor. Windows'ta `winget install ffmpeg` veya [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) üzerinden kurabilirsin.

## Kullanım

### 1. Şarkı listeni oluştur

Proje klasöründe `sarkilar.txt` adında bir dosya oluştur ve indirmek istediğin şarkıları her satıra bir tane olacak şekilde yaz:

```bash
# Dosyayı oluştur (Windows)
notepad sarkilar.txt
```

```
stairway to heaven
bohemian rhapsody
şımarık tarkan
```

> **İpucu:** Şarkının yanına sanatçı adını da yazarsan daha doğru sonuç bulur (ör. `numb linkin park`).

### 2. Çalıştır

```bash
python main.py
```

### 3. Sonuçları gör

İndirme tamamlandığında `sarkilar.txt` otomatik güncellenir:

```
stairway to heaven | Led Zeppelin - Stairway To Heaven (Official Audio).mp3
bohemian rhapsody | Queen – Bohemian Rhapsody (Official Video Remastered).mp3
şımarık tarkan | Tarkan - Şımarık (Official Video).mp3
```

Böylece hangi şarkının hangi dosya adıyla indiğini görebilirsin. Tekrar çalıştırdığında bu şarkılar atlanır.

**Yeni şarkı eklemek için** `sarkilar.txt`'ye yeni bir satır ekle ve tekrar çalıştır. Eski indirilenler tekrar indirilmez.

## Dosya Yapısı

```
mp3dip/
├── main.py                # Ana script
├── README.md
├── .gitignore
├── sarkilar.txt           # ⚠ Kendin oluşturmalısın (repoya dahil değil)
├── mp3/                   # İndirilen MP3 dosyaları (repoya dahil değil)
└── indirilemeyenler.txt   # Başarısız indirmeler (otomatik oluşur, repoya dahil değil)
```

## Çıktı Örneği

```
🎵 Toplam 3 şarkı indirilecek...

[1/3] ▶ Aranıyor: stairway to heaven...
  ↳ Bulunan video: Led Zeppelin - Stairway To Heaven (Official Audio)
  ↳ İndiriliyor...
✔ Başarıyla indirildi: stairway to heaven → Led Zeppelin - Stairway To Heaven (Official Audio).mp3
⏳ Sıradaki şarkıya geçmeden önce 3 saniye bekleniyor...

[2/3] ▶ Aranıyor: bohemian rhapsody...
  ↳ Bulunan video: Queen – Bohemian Rhapsody (Official Video Remastered)
  ↳ İndiriliyor...
✔ Başarıyla indirildi: bohemian rhapsody → Queen – Bohemian Rhapsody (Official Video Remastered).mp3
⏳ Sıradaki şarkıya geçmeden önce 3 saniye bekleniyor...

[3/3] ▶ Aranıyor: şımarık tarkan...
  ↳ Bulunan video: Tarkan - Şımarık (Official Video)
  ↳ İndiriliyor...
✔ Başarıyla indirildi: şımarık tarkan → Tarkan - Şımarık (Official Video).mp3

══════════════════════════════════════════════════
  📊 İNDİRME RAPORU
══════════════════════════════════════════════════
  ✔ Başarılı: 3/3
  ⏭ Zaten indirilmiş: 0
  ✖ Başarısız: 0/3
══════════════════════════════════════════════════

🎉 Tüm şarkılar başarıyla indirildi!
```

## Notlar

- Ses kalitesini değiştirmek için `main.py` içindeki `preferredquality` değerini `320` yapabilirsin
- Her şarkı arasında 3 saniye bekleme süresi var (YouTube'un rate limit'ine takılmamak için)
- `sarkilar.txt`'deki bir şarkıyı tekrar indirmek istersen, yanındaki `| dosya_adi.mp3` kısmını silmen yeterli

## Lisans

MIT
