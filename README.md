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

### 1. Şarkı listeni hazırla

`sarkilar.txt` dosyasına indirmek istediğin şarkıları her satıra bir tane olacak şekilde yaz:

```
karabiberim
havhavhav
cybersex doja cat
numb linkin park
```

### 2. Çalıştır

```bash
python main.py
```

### 3. Sonuçları gör

İndirme tamamlandığında `sarkilar.txt` otomatik güncellenir:

```
karabiberim | Serdar Ortaç - Karabiberim (Official Video).mp3
havhavhav | LVBEL C5 - HAVHAVHAV.mp3
cybersex doja cat | Doja Cat - Cyber Sex (Official Video).mp3
numb linkin park | Numb (Official Music Video) - Linkin Park.mp3
```

Böylece hangi şarkının hangi dosya adıyla indiğini görebilirsin. Tekrar çalıştırdığında bu şarkılar atlanır.

**Yeni şarkı eklemek için** `sarkilar.txt`'ye yeni bir satır ekle ve tekrar çalıştır. Eski indirilenler tekrar indirilmez.

## Dosya Yapısı

```
mp3dip/
├── main.py              # Ana script
├── sarkilar.txt         # Şarkı listesi (arama terimi | indirilen dosya adı)
├── mp3/                 # İndirilen MP3 dosyaları
├── indirilemeyenler.txt # Başarısız indirmeler ve sebepleri (otomatik oluşur)
└── README.md
```

## Çıktı Örneği

```
⏭ 2 şarkı zaten indirilmiş, atlanıyor:
   • karabiberim → Serdar Ortaç - Karabiberim (Official Video).mp3
   • havhavhav → LVBEL C5 - HAVHAVHAV.mp3

🎵 Toplam 1 şarkı indirilecek...

[1/1] ▶ Aranıyor: mokali...
  ↳ Bulunan video: Organize x Lvbel C5 x Ezhel - CADDE BOSTAN 2.0 (Mokali Mix)
  ↳ İndiriliyor...
✔ Başarıyla indirildi: mokali → Organize x Lvbel C5 x Ezhel - CADDE BOSTAN 2.0 (Mokali Mix).mp3

══════════════════════════════════════════════════
  📊 İNDİRME RAPORU
══════════════════════════════════════════════════
  ✔ Başarılı: 1/1
  ⏭ Zaten indirilmiş: 2
  ✖ Başarısız: 0/1
══════════════════════════════════════════════════

🎉 Tüm şarkılar başarıyla indirildi!
```

## Notlar

- Ses kalitesini değiştirmek için `main.py` içindeki `preferredquality` değerini `320` yapabilirsin
- Her şarkı arasında 3 saniye bekleme süresi var (YouTube'un rate limit'ine takılmamak için)
- `sarkilar.txt`'deki bir şarkıyı tekrar indirmek istersen, yanındaki `| dosya_adi.mp3` kısmını silmen yeterli

## Lisans

MIT
