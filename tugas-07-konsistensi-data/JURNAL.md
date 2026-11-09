# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: ...
- Kesimpulan akhir & alasan: ...

## Simulasi
- Skenario Naif
Ketika top-up pada server Jakarta saldo = 50000.0, version = 1 replikasi server Bandung tertunda selama 2,0 detik akibat``threading.Timer(REPLICATION_DELAY, self.bandung.write, args=(user_id, saldo_baru, version)).start()`` . yaitu skenario delay. Namun dijalankan pembacaan langsung dari server bandung sehingga saldo terbaca  0,0 karena belum memiliki catatan pada data tersebut karena masih version = 0 

- Skenario Read Your Write
Top up dilakukan pada sever Jakarta saldo = 7000.0, version = 2 dengan durasi delay jaringan selama 2,0 detik. Saat pembacaan dipanggil dari server Bandung sebelum replikasi selesai (t < 2,0 detik), mekanisme baca_saldo_read_your_writes secara proaktif memeriksa versi data di server tujuan. Karena versi di Bandung masih usang (version 1 < 2), sistem menahan pembacaan (polling wait) hingga thread replikasi memperbarui server Bandung ke version = 2. Setelah replikasi tiba, fungsi baru melepaskan nilainya dan mengembalikan angka saldo yang konsisten dan akurat, yaitu 70000.0




## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
