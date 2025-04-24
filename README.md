# Fire Detection System with Telegram Integration

Prototipe sistem deteksi kebakaran untuk memonitor umpan video dan mengirimkan peringatan langsung melalui Telegram ketika kebakaran terdeteksi.

## Fitur

- Deteksi api menggunakan computer vision
- Pilihan beberapa sumber video (webcam atau MJPEG stream)
- Peringatan instan melalui pesan Telegram
- Pengambilan screenshot ketika api terdeteksi 
- Indikasi visual api dengan kotak pembatas pada tampilan video

## Requirements

- Python 3.6 atau lebih tinggi
- Webcam (jika menggunakan sumber video lokal)
- Koneksi internet untuk notifikasi Telegram

## Instalasi

1. Clone repository ini:
   ```bash
   git clone https://github.com/yourusername/fire-detection-integrated-with-telegram.git
   cd fire-detection-integrated-with-telegram
   ```

2. Install dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

## Konfigurasi

Sebelum menjalankan aplikasi, Anda perlu mengatur kredensial API Bot Telegram:

1. Buka `main.py` di editor teks
2. Temukan baris berikut:
   ```python
   TELEGRAM_BOT_TOKEN = '#'
   TELEGRAM_CHAT_ID = '#'
   ```
3. Ganti placeholder `#` dengan Token Bot Telegram dan Chat ID Anda yang sebenarnya

### Cara mendapatkan Token Bot Telegram dan Chat ID

1. Buat bot baru dengan mengirim pesan ke [@BotFather](https://t.me/botfather) di Telegram
2. Ikuti instruksi untuk membuat bot baru dan dapatkan token bot
3. Mulai percakapan dengan bot Anda
4. Untuk mendapatkan Chat ID Anda, gunakan [@userinfobot](https://t.me/userinfobot) atau kunjungi `https://api.telegram.org/bot<YourBOTToken>/getUpdates` setelah mengirim pesan ke bot Anda

## Cara Penggunaan

1. Jalankan aplikasi:
   ```bash
   python main.py
   ```
   atau
   ```bash
   py main.py
   ```

2. Saat diminta, pilih sumber video:
   - Masukkan `1` untuk menggunakan webcam Anda
   - Masukkan `2` untuk menggunakan URL streaming MJPEG

3. Aplikasi akan mulai memantau sumber video yang dipilih untuk deteksi api
   - Tekan tombol `q` untuk keluar dari aplikasi

## Cara Kerja

Sistem menggunakan cascade classifier yang dilatih untuk mendeteksi pola api dalam frame video. Ketika api terdeteksi:
1. Screenshot diambil dan disimpan sementara
2. Pesan peringatan dikirim ke chat Telegram yang ditentukan
3. Screenshot dikirim ke chat sebagai bukti
4. Screenshot dihapus dari penyimpanan lokal setelah dikirim

## Customization

Anda dapat menyesuaikan pesan peringatan dengan memodifikasi variabel `pesan_teks` di `main.py`:

```python
pesan_teks = '[Peringatan] \n Api terdeteksi \n Periksa Dapur Anda Sekarang Juga!!!'
```
