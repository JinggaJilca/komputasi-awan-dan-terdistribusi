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

## Simulasi
- Skenario Naif
Ketika top-up pada server Jakarta saldo = 50000.0, version = 1 replikasi server Bandung tertunda selama 2,0 detik akibat``threading.Timer(REPLICATION_DELAY, self.bandung.write, args=(user_id, saldo_baru, version)).start()`` . yaitu skenario delay. Namun dijalankan pembacaan langsung dari server bandung sehingga saldo terbaca  0,0 karena belum memiliki catatan pada data tersebut karena masih version = 0 

- Skenario Read Your Write
Top up dilakukan pada sever Jakarta saldo = 7000.0, version = 2 dengan durasi delay jaringan selama 2,0 detik. Saat pembacaan dipanggil dari server Bandung sebelum replikasi selesai (t < 2,0 detik), mekanisme baca_saldo_read_your_writes secara proaktif memeriksa versi data di server tujuan. Karena versi di Bandung masih usang (version 1 < 2), sistem menahan pembacaan (polling wait) hingga thread replikasi memperbarui server Bandung ke version = 2. Setelah replikasi tiba, fungsi baru melepaskan nilainya dan mengembalikan angka saldo yang konsisten dan akurat, yaitu 70000.0




## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 09 November 2026 | Claude | Apa saja jenis Client-Centric Consistency? | Menjelaskan empat model (Monotonic Reads, Monotonic Writes, Read-Your-Writes, Writes Follow Reads) beserta contohnya. | Dipakai untuk memilih model yang relevan dengan kasus saldo. |
| 09 November 2026 | Claude | Jelaskan konsep sequential dan eventual consistency beserta analogi sehari-hari. | Menjelaskan konsep, tabel perbandingan, dan kaitannya dengan teorema CAP | Memahami konsep dan analogi dari sequential dan eventual consistency. | 