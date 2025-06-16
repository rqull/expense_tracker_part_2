// Script untuk menerapkan tema gelap
document.addEventListener('DOMContentLoaded', function() {
    // Pastikan tema gelap selalu diaktifkan
    document.documentElement.classList.add('dark');

    // Konfigurasi Chart.js untuk tema gelap
    if (window.Chart) {
        Chart.defaults.color = '#e4e6eb';
        Chart.defaults.borderColor = '#374151';
        Chart.defaults.backgroundColor = '#2d2d2d';
    }

    // Menyesuaikan warna text pada elemen yang tidak terpengaruh oleh CSS
    const fixTextColors = () => {
        // Mengubah warna teks pada elemen dengan class tertentu
        document.querySelectorAll('.text-gray-700, .text-gray-800, .text-gray-900').forEach(el => {
            el.classList.remove('text-gray-700', 'text-gray-800', 'text-gray-900');
            el.classList.add('text-gray-100');
        });

        document.querySelectorAll('.text-gray-500, .text-gray-600').forEach(el => {
            el.classList.remove('text-gray-500', 'text-gray-600');
            el.classList.add('text-gray-400');
        });
    };

    // Jalankan fungsi saat halaman dimuat
    fixTextColors();

    // Pantau perubahan DOM dan jalankan fungsi kembali jika ada perubahan
    // Berguna untuk konten yang dimuat secara dinamis
    const observer = new MutationObserver(fixTextColors);
    observer.observe(document.body, { childList: true, subtree: true });
});
