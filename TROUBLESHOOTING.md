# Panduan Pemecahan Masalah (Troubleshooting)

## Masalah: AlreadyRegistered: Model sudah terdaftar di admin

Jika Anda mendapatkan error seperti ini:
```
django.contrib.admin.exceptions.AlreadyRegistered: The model Currency is already registered with 'expenses.CurrencyAdmin'.
```

Penyebabnya adalah model tersebut didaftarkan dua kali di file `admin.py`. Solusinya adalah menghapus pendaftaran yang duplikat tersebut.

## Masalah: No such table

Jika Anda mendapatkan error "no such table" saat mengakses aplikasi, pastikan Anda sudah menjalankan migrasi:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Masalah: Migration history mismatch

Jika terjadi masalah dengan migrasi database, coba reset migrasi dengan:

```bash
python manage.py migrate expenses zero
python manage.py makemigrations expenses
python manage.py migrate expenses
```

## Masalah: Data awal tidak terload

Jika data awal (initial data) tidak terload, pastikan Anda sudah menjalankan:

```bash
python manage.py loaddata expenses/fixtures/initial_data.json
```

Setelah semua migrasi selesai.

## Masalah: Tidak bisa login ke admin

Pastikan Anda sudah membuat superuser dengan:

```bash
python manage.py createsuperuser
```

## Masalah: Template tidak ditemukan

Jika ada template yang tidak ditemukan, pastikan struktur folder templates sudah benar dan setting `TEMPLATES` di `settings.py` sudah dikonfigurasi dengan benar.

## Masalah: Static files tidak terload

Jalankan perintah berikut untuk mengumpulkan static files:

```bash
python manage.py collectstatic
```

Pastikan setting `STATIC_URL` dan `STATICFILES_DIRS` di `settings.py` sudah benar.
