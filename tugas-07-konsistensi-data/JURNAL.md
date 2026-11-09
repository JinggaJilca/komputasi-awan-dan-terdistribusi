# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
1. Sequential Consistency
   - Kelebihan: Semua server (Jakarta dan Bandung) dapat melihat urutan operasi saldo yang sama (seperti top-up yang selalu tercatat sebelum pemesanan dilakukan), sistem mudah untuk diprediksi dan diaudit, serta logika aplikasi yang lebih sederhana karena tidak perlu menangani data lama atau konflik secara manual.
   - Kekurangan: Latensi lebih tinggi karena server harus berkoordinasi sebelum merespons, ketersediaan menurun saat terjadi partisi jaringan antar-wilayah, dan skalabilitas lintas wilayah lebih terbatas.
2. Eventual Consistency
   - Kelebihan: Ketersediaan tinggi, latensi rendah, dan mudah diskalakan lintas wilayah karena server tidak perlu menunggu proses replikasi selesai sebelum melayani pengguna.
   - Kekurangan: Server dapat membaca saldo lama, urutan pembaruan dapat berbeda antar-replika, konflik penulisan berisiko menghilangkan data, dan beban penanganan inkonsistensi berpindah ke logika aplikasi.
3. Pertimbangan dampak bisnis: Saldo e-wallet merupakan data yang sangat sensitif, sehingga ketidaksesuaian saldo antar-server dapat menyebabkan transaksi ditolak meski saldo cukup, saldo tercatat salah, atau pesanan yang lolos dengan saldo yang sama. Akibatnya FoodGo berisiko kehilangan dana dan kepercayaan pelanggan, menanggung klaim ganti rugi, serta melanggar kewajiban pencatatan keuangan yang akurat dan dapat diadit. Kerugian ini lebih besar dibandingkan dengan kerugian pada data non-kritis seperti jumlah like.

- Kesimpulan akhir & alasan: Kami menyimpulkan bahwa Eventual Consistency tidak cukup untuk data saldo e-wallet FoodGo. Replikasi yang lambat antara server Jakarta dan Bandung membuat pelanggan yang baru top-up masih melihat saldo yang lama. Kondisi ini berdampak langsung pada bisnis, yaitu hilangnya pesanan dan menurunnya kepercayaan pelanggan. Karena itu, Sequential Consistency diperlukan untuk operasi saldo agar semua server sepakat pada satu urutan operasi yang sama. Sebagai pelengkap, kami menerapkan Read-Your-Writes sebagai pendekatan client-centric, sehingga pelanggan yang baru top-up dapat melihat saldo terbarunya meskipun terhubung ke server yang berbeda. 

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
