# Panduan Setup Database PostgreSQL

## Pastikan PostgreSQL sudah terinstall

1. Download dan install PostgreSQL dari [situs resmi PostgreSQL](https://www.postgresql.org/download/)
2. Selama instalasi, catat password untuk user postgres

## Buat database dan user

1. Buka pgAdmin atau PostgreSQL command prompt
2. Buat database baru dengan nama `expense_tracker_db`:
   ```sql
   CREATE DATABASE expense_tracker_db;
   ```

3. Pastikan user postgres memiliki akses ke database ini

## Konfirmasi konfigurasi database

1. Pastikan file `.env` di root project berisi konfigurasi yang benar:
   ```
   DB_NAME=expense_tracker_db
   DB_USER=postgres
   DB_PASSWORD=12345  # Ganti dengan password PostgreSQL Anda
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. Jika Anda mengubah password di file `.env`, pastikan bahwa itu sesuai dengan password PostgreSQL Anda

## Jalankan migrasi database

```bash
python manage.py migrate
```

## Troubleshooting

- Jika masih mendapatkan error koneksi, pastikan server PostgreSQL berjalan
- Periksa apakah port 5432 tidak diblokir oleh firewall
- Pastikan username dan password benar
