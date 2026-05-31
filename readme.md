# 💳 PayGate — Payment Gateway dengan Python Flask

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?logo=flask)
![Midtrans](https://img.shields.io/badge/Midtrans-Sandbox-blue)
![License](https://img.shields.io/badge/License-MIT-green)

PayGate adalah aplikasi payment gateway berbasis **Python Flask** yang terintegrasi dengan **Midtrans** sebagai penyedia pembayaran. Project ini mendukung berbagai metode pembayaran populer di Indonesia dan cocok digunakan sebagai portofolio maupun fondasi aplikasi e-commerce.

---

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Metode Pembayaran](#-metode-pembayaran)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Struktur Folder](#-struktur-folder)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [API Endpoints](#-api-endpoints)
- [Testing dengan Simulator Midtrans](#-testing-dengan-simulator-midtrans)
- [Cara Upgrade ke Production](#-cara-upgrade-ke-production)
- [Tangkapan Layar](#-tangkapan-layar)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## ✨ Fitur

- ✅ Integrasi penuh dengan **Midtrans Snap** dan **Core API**
- ✅ Mendukung **7 metode pembayaran** populer Indonesia
- ✅ Dashboard pembayaran dengan tampilan modern (Tailwind CSS)
- ✅ Riwayat transaksi dengan filter dan pencarian
- ✅ Statistik transaksi real-time (total, berhasil, pending, nominal)
- ✅ Webhook handler untuk notifikasi status pembayaran otomatis
- ✅ Database SQLite (mudah di-upgrade ke PostgreSQL/MySQL)
- ✅ Mode Sandbox untuk testing tanpa uang nyata
- ✅ Link simulator otomatis untuk setiap metode pembayaran
- ✅ Siap di-deploy ke Railway, Render, atau VPS

---

## 💰 Metode Pembayaran

| Metode | Tipe | Simulator |
|--------|------|-----------|
| Semua Metode (Snap) | Popup terintegrasi | Via popup Midtrans |
| GoPay | E-wallet | ✅ Simulator tersedia |
| ShopeePay | E-wallet | ✅ Simulator tersedia |
| QRIS | QR Code | ✅ Simulator tersedia |
| Virtual Account BCA | Transfer bank | ✅ Simulator tersedia |
| Virtual Account BNI | Transfer bank | ✅ Simulator tersedia |
| Virtual Account BRI | Transfer bank | ✅ Simulator tersedia |
| Virtual Account Mandiri | Transfer bank | ✅ Simulator tersedia |
| Virtual Account Permata | Transfer bank | ✅ Simulator tersedia |
| Alfamart | Minimarket | ✅ Simulator tersedia |
| Indomaret | Minimarket | ✅ Simulator tersedia |

---

## 🛠 Teknologi yang Digunakan

### Backend
| Package | Versi | Fungsi |
|---------|-------|--------|
| `Flask` | 3.0.0 | Web framework utama |
| `Flask-SQLAlchemy` | 3.1.1 | ORM untuk database |
| `Flask-Migrate` | 4.0.5 | Migrasi skema database |
| `midtransclient` | 1.4.2 | SDK resmi Midtrans |
| `python-dotenv` | 1.0.0 | Manajemen environment variable |
| `requests` | 2.31.0 | HTTP client |

### Frontend
| Teknologi | Fungsi |
|-----------|--------|
| Tailwind CSS (CDN) | Styling dan UI |
| Vanilla JavaScript | Interaksi dan fetch API |
| Midtrans Snap.js | Popup pembayaran |
| Google Fonts (Inter) | Tipografi |

### Database
- **Development**: SQLite (file lokal `payments.db`)
- **Production**: PostgreSQL / MySQL (konfigurasi via `DATABASE_URL`)

---

## 📁 Struktur Folder

```
payment_gateway/
├── app/
│   ├── __init__.py              # Inisialisasi Flask app & ekstensi
│   ├── models.py                # Model database (Transaction)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── payment_routes.py    # Endpoint pembayaran & halaman HTML
│   │   ├── auth_routes.py       # Endpoint autentikasi
│   │   └── webhook_routes.py    # Handler notifikasi Midtrans
│   ├── services/
│   │   ├── __init__.py
│   │   └── midtrans_service.py  # Logika integrasi Midtrans
│   └── templates/
│       ├── base.html            # Template dasar (navbar, footer)
│       ├── index.html           # Halaman buat pembayaran
│       └── transaksi.html       # Halaman riwayat transaksi
├── config/
│   ├── __init__.py
│   └── config.py                # Konfigurasi aplikasi
├── migrations/                  # File migrasi database (auto-generated)
├── .env                         # Environment variable (jangan di-commit!)
├── .gitignore
├── requirements.txt
└── run.py                       # Entry point aplikasi
```

---

## 📦 Prasyarat

Pastikan sudah terinstal:

- **Python** 3.10 atau lebih baru → [Download](https://www.python.org/downloads/)
- **pip** (sudah termasuk dalam instalasi Python)
- **Git** → [Download](https://git-scm.com/)
- Akun **Midtrans Sandbox** (gratis) → [Daftar](https://dashboard.sandbox.midtrans.com/register)

---

## 🚀 Instalasi

### 1. Clone repository

```bash
git clone https://github.com/username/payment_gateway.git
cd payment_gateway
```

### 2. Buat virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfigurasi

### 1. Buat file `.env`

Salin contoh konfigurasi berikut dan simpan sebagai `.env` di root project:

```env
# Flask
SECRET_KEY=ganti-dengan-string-acak-yang-panjang
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///payments.db

# Midtrans Sandbox
MIDTRANS_SERVER_KEY=Mid-server-xxxxxxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=Mid-client-xxxxxxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=False
```

> 💡 **Cara generate SECRET_KEY yang aman:**
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 2. Dapatkan API Key Midtrans

1. Login ke [Midtrans Sandbox Dashboard](https://dashboard.sandbox.midtrans.com)
2. Buka **Settings → Access Keys**
3. Copy **Server Key** dan **Client Key**
4. Paste ke file `.env`

---

## ▶️ Menjalankan Aplikasi

### 1. Inisialisasi database

```bash
# Set environment variable (Windows PowerShell)
$env:FLASK_APP = "run.py"

# Inisialisasi migrasi
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 2. Jalankan server

```bash
python run.py
```

### 3. Buka browser

```
http://127.0.0.1:5000
```

Aplikasi siap digunakan! 🎉

---

## 📡 API Endpoints

### Halaman Web

| Method | URL | Deskripsi |
|--------|-----|-----------|
| `GET` | `/` | Halaman buat pembayaran |
| `GET` | `/transaksi` | Halaman riwayat transaksi |

### Payment API

| Method | URL | Deskripsi |
|--------|-----|-----------|
| `GET` | `/api/payment/list` | Daftar semua transaksi |
| `GET` | `/api/payment/status/<order_id>` | Status transaksi |
| `POST` | `/api/payment/create` | Buat transaksi via Snap |
| `POST` | `/api/payment/gopay` | Buat transaksi GoPay |
| `POST` | `/api/payment/shopeepay` | Buat transaksi ShopeePay |
| `POST` | `/api/payment/qris` | Buat transaksi QRIS |
| `POST` | `/api/payment/va` | Buat Virtual Account |
| `POST` | `/api/payment/alfamart` | Buat kode Alfamart |
| `POST` | `/api/payment/indomaret` | Buat kode Indomaret |

### Webhook

| Method | URL | Deskripsi |
|--------|-----|-----------|
| `POST` | `/api/webhook/midtrans` | Handler notifikasi Midtrans |

### Contoh Request

**Buat transaksi GoPay:**
```bash
curl -X POST http://localhost:5000/api/payment/gopay \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150000,
    "customer": {
      "name": "Budi Santoso",
      "email": "budi@email.com",
      "phone": "08123456789"
    }
  }'
```

**Response:**
```json
{
  "order_id": "ORDER-4B3ABC72",
  "transaction_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "deeplink_url": "https://simulator.sandbox.midtrans.com/...",
  "simulator_url": "https://simulator.sandbox.midtrans.com/gopay/ui/index?..."
}
```

**Buat Virtual Account:**
```bash
curl -X POST http://localhost:5000/api/payment/va \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 75000,
    "bank": "bca",
    "customer": {
      "name": "Siti Rahayu",
      "email": "siti@email.com"
    }
  }'
```

---

## 🧪 Testing dengan Simulator Midtrans

Semua metode pembayaran bisa ditest **tanpa uang nyata** menggunakan simulator Midtrans.

### Kartu Kredit (via Snap)

| Field | Nilai |
|-------|-------|
| Nomor Kartu | `4811 1111 1111 1114` |
| Expiry | `0139` |
| CVV | `123` |
| OTP | `112233` |

### E-wallet & QRIS

Setelah transaksi dibuat, klik **"Buka Simulator Midtrans"** yang muncul otomatis di halaman, lalu klik **"Pay"** di halaman simulator.

### Virtual Account

Nomor VA akan tampil setelah transaksi dibuat. Klik link simulator → masukkan nomor VA → klik **"Pay"**.

### Mandiri (Echannel)

Gunakan **Biller Code** dan **Bill Key** yang tampil setelah transaksi dibuat di simulator Mandiri.

### Alfamart & Indomaret

Gunakan **kode pembayaran** yang tampil di link simulator minimarket.

---

## 🔄 Status Transaksi

| Status | Keterangan |
|--------|------------|
| `pending` | Transaksi dibuat, menunggu pembayaran |
| `success` | Pembayaran berhasil dikonfirmasi |
| `failed` | Pembayaran gagal atau ditolak |
| `cancel` | Transaksi dibatalkan |
| `expire` | Transaksi kedaluwarsa |

---

## 🌐 Cara Upgrade ke Production

### 1. Verifikasi akun Midtrans

Lengkapi dokumen di [dashboard.midtrans.com](https://dashboard.midtrans.com):
- KTP pemilik
- NPWP (opsional untuk UMKM)
- Nomor rekening bank aktif

### 2. Update konfigurasi `.env`

```env
MIDTRANS_SERVER_KEY=Mid-server-PRODUCTION-KEY
MIDTRANS_CLIENT_KEY=Mid-client-PRODUCTION-KEY
MIDTRANS_IS_PRODUCTION=True
DATABASE_URL=postgresql://user:password@host/dbname
```

### 3. Update Snap.js di `base.html`

```html
<!-- Ganti dari: -->
<script src="https://app.sandbox.midtrans.com/snap/snap.js">

<!-- Menjadi: -->
<script src="https://app.midtrans.com/snap/snap.js">
```

### 4. Deploy ke hosting

```bash
# Contoh deploy ke Railway
railway login
railway init
railway up
```

---

## 🔒 Keamanan

- Jangan pernah meng-commit file `.env` ke repository publik
- Tambahkan `.env` ke `.gitignore`
- Gunakan HTTPS di production
- Validasi signature webhook dari Midtrans di production
- Ganti `SECRET_KEY` dengan string acak yang panjang dan unik

### `.gitignore` yang disarankan

```gitignore
# Environment
.env
*.env

# Virtual Environment
venv/
env/
.venv/

# Database
*.db
*.sqlite3

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp

# Migrations (opsional, bisa di-include)
# migrations/
```

---

## 🤝 Kontribusi

Pull request sangat disambut! Untuk perubahan besar, buka issue terlebih dahulu untuk mendiskusikan apa yang ingin diubah.

1. Fork repository ini
2. Buat branch fitur: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m 'feat: tambah fitur X'`
4. Push ke branch: `git push origin fitur/nama-fitur`
5. Buat Pull Request

---

## 📄 Lisensi

Didistribusikan di bawah lisensi **MIT**. Lihat `LICENSE` untuk informasi lebih lanjut.

---

## 👨‍💻 Developer

**Muhamad Farhanudin**
- GitHub: [@farhanudin26](https://github.com/farhanudin26)
- Email: udilspicy13@gmail.com

---

> ⚠️ **Disclaimer**: Project ini dibuat untuk tujuan pembelajaran dan portofolio. Pastikan memahami kebijakan Midtrans sebelum menggunakannya di lingkungan production.