# Jurnal Proses — Tugas 4

## Jalur yang dipilih
### Jalur RPC

Pada cek_saldo, jika user_id tidak ditemukan, server menampilkan pesan bahwa user tidak ditemukan, bukan mengembalikan angka 0. Keputusan ini dipilih karena angka 0 membuat modul Pesanan sulit membedakan antara user yang memang tidak ada dan user yang ada tetapi saldonya 0. Saat diuji, waktu yang dibutuhkan untuk mendapat hasil dari modul cek_saldo pada RPC adalah 2,1141 detik. Selama waktu itu client menunggu dan tidak bisa mengerjakan hal lain, sehingga terbukti bahwa RPC bersifat sinkron. Sifat ini berkaitan dengan prinsip coupling pada RPC, yaitu ketergantungan antar modul.

Modul Pesanan bergantung pada modul Pembayaran, baik dari sisi waktu karena harus menunggu balasan, maupun dari sisi ketersediaan karena modul Pembayaran harus aktif. Karena itu RPC cocok untuk cek_saldo dan proses_pembayaran, karena hasil modul sebelumnya menentukan langkah berikutnya. Jika saldo tidak cukup atau pembayaran gagal, pesanan tidak boleh dibuat, sehingga modul Pesanan harus menunggu sampai modul Pembayaran memberikan balasan (menyatakan berhasil atau gagal). Namun, RPC tidak cocok untuk notifikasi ke kurir, karena modul Pembayaran tidak membutuhkan jawaban dari kurir dan tidak boleh ikut terhambat olehnya. Jika notifikasi dikirim dengan RPC, modul Pembayaran akan menunggu balasan kurir, sehingga ketika kurir sibuk atau mati, proses pembayaran ikut lambat atau gagal, padahal masalahnya ada di modul lain.

### Jalur MQ

Fungsi cek_saldo membutuhkan komunikasi sinkron karena modul pembayaran memerlukan respons secara langsung sebelum transaksi diproses. Sebaliknya, notifikasi "pembayaran berhasil" ke modul kurir dikirim secara asinkron melalui MOM. Dengan metode ini, modul pembayaran hanya bertugas untuk mempublikasikan event ke antrian lalu langsung melanjutkan eksekusi tanpa tertahan saat menunggu proses modul kurir. Berdasarkan hasil percobaan, waktu publish pada modul pembayaran memunjukkan rata-rata waktu yang singkat, yaitu 0.001354 detik. Waktu tersebut lebih kecil dibandingkan total end-to-end pada consumer, sehingga dapat di simpulkan bahwa modul pembayaran tidak bergantung pada ketersediaan maupun performa modul kurir.

Pada pesan pertama "user1", latensi antrean berestimasi 0.050699 detik, lebih tinggi dibandingkan dengan user2 dan user3. Hal tersebut kemungkinan berasal dari overhead saat inisialisasi pertama broker dan consumer. Setelah jaringan stabil, latensi perlahan turun menjadi 0.004755 hingga 0.006064 detik. Ini menunjukkan antrean pesan dapat menangani aliran data tanpa menimbulkan bottleneck.

Sistem ini diperkuat dengan penggunaan durable=True dan DeliveryMode.Persistent, di mana menjamin bahwa data transaksi tidak hilang dari memori meskipun RabbitMQ mengalami restart atau kegagalan sistem mendadak. Selain itu, penggunaan ch.basic_ack() pada consumer memastikan penerapan At-Least-One Delivery, dimana pesan baru terhapus dari antrean jika modul kurir telah sukses menyelesaikan tugasnya. Sehingga jika modul kurir mengalami kendala, RabbitMQ akan menampung pesan dengan amana sampai modul tersebut aktif kembali.

- [RPC / MQ / keduanya], alasan: ...

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: nilai latensi yang dihasilkan berdurasi 1 sampai 3 detik, hal tersebut menggambarkan adanya waktu jeda sejak pesan di publikasikan oleh publisher hingga consumer diaktifkan kembali. Latensi yang mengecil secara bertahap disebabkan oleh jarak waktu pengiriman yang diberi delay 1 detik untuk setiap pesan. Hasil pengamatan ini membuktikan bahwa durable=True & DeliveryMode.Persistent terbukti berhasil menyimpan pesan dalam RabbitMQ meskipun consumer sedang tidak aktif, dan modul pembayaran terbukti tidak bergantung pada status aktif modul kurir sehingga transaksi dapat terus berjalan tanpa hambatan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 5 Oktober 2026 | Claude | Apa yang akan terjadi pada pesan jika broker mengalami crash? opsi apa yang tersedia untuk mencegah hal tersebut | Perlu ditambahkan DeliveryMode.Persistent agar pesan tersimpan ke disk ketika broker mengalami crash | Memahami penggunaan DeliveryMode.Persistent dan menambahkan pengunaannya pada kode |
| ... | ... | ... | ... | ... |