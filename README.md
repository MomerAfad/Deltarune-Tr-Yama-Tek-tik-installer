# Can sıkıntısından yaptığım Deltarune Bluesoul Chapter 3-4 Tek tık Türkçe Yama Kurulum aracı!

Deltarune için Bluesoul ekibinin Türkçe yamasını tek tıkla kuran basit bir installer.

## Özellikler

✅ **Modern Karanlık Tema**: Profesyonel görünümlü arayüz  
✅ **Özel İkon**: Mavi piksel kalp logosu  
✅ **Otomatik Tespit**: Deltarune kurulum klasörünü otomatik olarak bulur (Steam vs.)  
✅ Eğer isterseniz manuel seçim dahildir  
✅ **Oto Yedekleme**: Orijinal dosyalarınız `backup_original` klasöründe yedeklenir  
✅ **Kolay Kullanım**: Tek tıkla yama kurulumu  
✅ **Yama Kaldırma**: Tek tıkla orijinal dosyalara geri dönme  
✅ **Çapraz Platform**: Windows ve Linux desteği

### Gereksinimler

- **Python 3.6+** yüklü olmalı
- **Windows**: Python dışında ekstra gereksinim yok
- **Linux**: Tkinter kurulumu gerekebilir:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # Fedora
  sudo dnf install python3-tkinter
  
  # Arch Linux
  sudo pacman -S tk
  ```

### Çalıştırma
Sadece 'RUN_INSTALLER.bat(linux ise .sh)'ı çalıştırın

```bash
python installer.py
```

## Kullanım

### Yamayı Kurmak
1. Programı çalıştırın
2. Program Deltarune kurulum klasörünü otomatik olarak bulmaya çalışacak
3. Bulamazsa *"Oyun Konumunu Seç"* butonuna tıklayarak manuel olarak seçin
4. *"Yamayı İndir"* butonuna tıklayın
5. Kurulum tamamlandığında oyunu Türkçe oynayabilirsiniz!

### Yamayı Kaldırmak (Orijinale Dönmek)
1. Programı çalıştırın
2. Oyun konumu seçiliyse **"Yamayı Kaldır (Orijinale Dön)"** butonuna tıklayın
3. Onay penceresinde **"Evet"** seçin
4. Orijinal dosyalar otomatik olarak geri yüklenecektir!

## Yama İçeriği

Bu yama şunları içerir:
- **data.win**: Oyun verilerinin Türkçeleştirilmiş versiyonu
- **chapter3_windows/** ve **chapter4_windows/**: Bölüm dosyaları
- **mus/**: Müzik dosyaları (gerekirse)

## Sorun Giderme

**Program Deltarune'u bulamıyor:**
- "Gözat..." butonunu kullanarak manuel olarak seçin
- Deltarune'un kurulu olduğu klasörde `DELTARUNE.exe` veya `SURVEY_PROGRAM.exe` dosyası olmalı

**Yama kurulmuyor:**
- Deltarune'un kapalı olduğundan emin olun
- Yönetici olarak çalıştırmayı deneyin

               İngilizce/Orjinal haline dönmek istiyorum:

- **"Yamayı Kaldır (Orijinale Dön)"** butonuna tıklayın
- Veya manuel olarak: `backup_original` klasöründeki dosyaları ana klasöre geri kopyalayın

## Lisans ve Teşekkürler

Bu araç, Bluesoul ekibinin "Deltarune Türkçe" yamasını kolayca kurmak için hazırlanmıştır.
Blue soul ekibine yaptıkları için teşekkürler! (`Yamanın var olmasını mümkün kılanlar.txt` dosyasına bakın)
