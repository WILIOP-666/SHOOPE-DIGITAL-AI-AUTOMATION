# AUTO - Pasar Digital Canggih dengan Kekuatan AI

Solusi pasar digital lengkap yang didukung otomatisasi berbasis AI, terintegrasi dengan Shopee, dan pengiriman produk otomatis secepat kilat!

## Sekilas tentang AUTO

AUTO adalah platform revolusioner untuk menjual dan mengirimkan produk digital dengan sentuhan ajaib otomatisasi AI. Dibangun dengan tiga pilar utama yang saling melengkapi:

1. **Backend (FastAPI)**: Otak di balik layar yang mengelola permintaan API, operasi database, pemrosesan AI, dan pengiriman produk.
2. **Frontend (Next.js)**: Antarmuka pengguna yang elegan untuk mengatur produk, pesanan, dan pengaturan AI dengan mudah.
3. **Ekstensi Browser (Plasmo)**: Jembatan cerdas yang terhubung dengan Shopee untuk memantau pesanan dan mengirimkan produk secara instan.

## Fitur Unggulan

### Fitur Inti
- Sistem autentikasi dan otorisasi pengguna yang aman.
- Manajemen produk super fleksibel (template, akun, tautan, voucher).
- Pemrosesan dan pelacakan pesanan yang mulus.
- Otomatisasi pengiriman produk digital tanpa repot.
- Integrasi langsung dengan pasar Shopee.

### Keajaiban AI
- Respons obrolan cerdas berbasis AI untuk menjawab pertanyaan pelanggan.
- Database vektor (Pinecone) untuk jawaban FAQ yang tepat sasaran.
- Database graf (Neo4j) sebagai memori jangka panjang yang andal.
- Pengaturan AI yang bisa disesuaikan untuk toko, produk, dan pengguna.

## Struktur Proyek

- `backend/`: Jantung Python FastAPI yang bertenaga.
- `frontend/`: Tampilan Next.js yang memukau.
- `extension/`: Ekstensi browser Plasmo yang inovatif.
- `docs/`: Panduan lengkap untuk menyelami proyek.

## Dokumentasi

- [Sekilas Proyek](docs/index.md)
- [Arsitektur Sistem](docs/architecture.md)
- [Dokumentasi API](docs/api.md)
- [Panduan Integrasi AI](docs/ai-integration.md)
- [Struktur Proyek](docs/project-structure.md)
- [Ringkasan Proyek](docs/summary.md)

## Cara Memulai

### Menyiapkan Backend

1. Masuk ke direktori backend:
```
cd backend
```

2. Buat lingkungan virtual:
```
python -m venv venv
```

3. Aktifkan lingkungan virtual:
```
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Pasang dependensi:
```
pip install -r requirements.txt
```

5. Buat file `.env` dengan variabel yang dibutuhkan (lihat `backend/README.md` untuk detailnya).

6. Inisialisasi database:
```
python init_db.py
```

7. Jalankan server:
```
uvicorn app.main:app --reload
```

### Menyiapkan Frontend

1. Masuk ke direktori frontend:
```
cd frontend
```

2. Pasang dependensi:
```
npm install
```

3. Buat file `.env.local` dengan variabel yang diperlukan (lihat `frontend/README.md` untuk detailnya).

4. Jalankan server pengembangan:
```
npm run dev
```

### Menyiapkan Ekstensi Browser

1. Masuk ke direktori ekstensi:
```
cd extension/auto-extension
```

2. Pasang dependensi:
```
npm install
```

3. Jalankan server pengembangan:
```
npm run dev
```

4. Muat ekstensi di browser Anda (lihat `extension/auto-extension/README.md` untuk panduan).

## Teknologi yang Digunakan

### Backend
- Python 3.9+: Bahasa yang kuat dan fleksibel.
- FastAPI: API cepat dan modern.
- SQLAlchemy: Pengelolaan database yang tangguh.
- Pinecone: Database vektor untuk pencarian cerdas.
- Neo4j: Database graf untuk memori kontekstual.
- OpenAI API: Kekuatan AI generatif.

### Frontend
- Next.js 14: Framework React tercanggih.
- React 19: UI yang responsif dan dinamis.
- TypeScript: Kode yang rapi dan aman.
- Tailwind CSS: Desain stylish dalam sekejap.

### Ekstensi Browser
- Plasmo: Fondasi ekstensi yang solid.
- React: Komponen yang interaktif.
- TypeScript: Keandalan dalam setiap baris kode.

## Lisensi

Proyek ini dilisensikan di bawah MIT License—lihat file LICENSE untuk detailnya.
