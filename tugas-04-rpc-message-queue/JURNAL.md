# Jurnal Proses — Tugas 4

## Jalur yang dipilih
# Jalur RPC

Pada cek_saldo, jika user_id tidak ditemukan, server menampilkan pesan bahwa user tidak ditemukan, bukan mengembalikan angka 0. Keputusan ini dipilih karena angka 0 membuat modul Pesanan sulit membedakan antara user yang memang tidak ada dan user yang ada tetapi saldonya 0. Saat diuji, waktu yang dibutuhkan untuk mendapat hasil dari RPC ini adalah 2,1141 detik. Selama waktu itu client menunggu dan tidak bisa mengerjakan hal lain, sehingga terbukti bahwa RPC bersifat sinkron. Sifat ini berkaitan dengan prinsip coupling pada RPC, yaitu ketergantungan antar modul.

Modul Pesanan bergantung pada modul Pembayaran, baik dari sisi waktu karena harus menunggu balasan, maupun dari sisi ketersediaan karena modul Pembayaran harus aktif. Karena itu RPC cocok untuk cek_saldo dan proses_pembayaran, karena hasil modul sebelumnya menentukan langkah berikutnya. Jika saldo tidak cukup atau pembayaran gagal, pesanan tidak boleh dibuat, sehingga modul Pesanan harus menunggu sampai modul Pembayaran menyatakan berhasil. Namun, RPC tidak cocok untuk notifikasi ke kurir, karena modul Pembayaran tidak membutuhkan jawaban dari kurir dan tidak boleh ikut terhambat olehnya. Jika notifikasi dikirim dengan RPC, modul Pembayaran akan menunggu balasan kurir, sehingga ketika kurir sibuk atau mati, proses pembayaran ikut lambat atau gagal, padahal masalahnya ada di modul lain.

- [RPC / MQ / keduanya], alasan: ...

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
