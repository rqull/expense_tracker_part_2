# Petunjuk Setup Aplikasi Expense Tracker

## Langkah 1: Setup Lingkungan Virtual (jika belum)

```bash
python -m venv .venv
```

### Aktivasi lingkungan virtual:

- Windows:
  ```bash
  .venv\Scripts\activate
  ```

- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

## Langkah 2: Instal Dependensi

```bash
pip install -r requirements.txt
```

## Langkah 3: Melakukan Migrasi Database

```bash
python manage.py makemigrations expenses
python manage.py migrate
```

## Langkah 4: Membuat Superuser (Admin)

```bash
python manage.py createsuperuser
```

Ikuti petunjuk untuk membuat akun admin dengan username, email, dan password.

## Langkah 5: Mengisi Data Awal (Opsional)

Jika tersedia fixture data, Anda dapat mengisinya dengan perintah:

```bash
python manage.py loaddata expenses/fixtures/initial_data.json
```

## Langkah 6: Menjalankan Server Pengembangan

```bash
python manage.py runserver
```

Aplikasi sekarang dapat diakses di http://127.0.0.1:8000

Halaman admin dapat diakses di http://127.0.0.1:8000/admin

## Catatan Tambahan

- Database default menggunakan SQLite yang sudah termasuk dalam Django
- Jika ingin menggunakan PostgreSQL, pastikan sudah menginstal `psycopg2-binary` (sudah termasuk dalam requirements.txt)
- Untuk menjalankan di lingkungan produksi, pastikan untuk mengubah pengaturan `DEBUG=False` dan mengkonfigurasi `ALLOWED_HOSTS` di file settings.py

## Troubleshooting

Jika Anda mengalami masalah selama setup atau menjalankan aplikasi, silakan lihat file `TROUBLESHOOTING.md` untuk panduan pemecahan masalah umum.

Jika masalah berlanjut, pastikan untuk memeriksa:
1. Versi Python (direkomendasikan Python 3.8+)
2. Versi Django (sesuai requirements.txt)
3. Struktur proyek dan file sudah benar
4. Migrasi database sudah dijalankan dengan benar
