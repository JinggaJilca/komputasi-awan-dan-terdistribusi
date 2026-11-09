# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).

    Jawaban:

    Pada kasus ini, Eventual Consistency saja tidak cukup. Eventual Consistency hanya menjamin bahwa semua replika akan sama pada akhirnya, tanpa menjamin berapa lama waktu yang dibutuhkan. Selama menunggu, Jakarta dan Bandung boleh menyimpan saldo yang berbeda. Itulah yang terjadi pada kasus FoodGo, yaitu pelanggan top-up di Jakarta, tetapi beberapa detik kemudian Bandung masih menyimpan saldo lama. Sistem ini menggunakan prinsip Eventual Consistency, karena Bandung boleh terlambat. Maka dari itu, Eventual Consistency saja tidak cukup, karena aturannya membolehkan kejadian yang menimbulkan masalah, yaitu keterlambatan update saldo.

    Dampak bisnisnya, jika saldo yang terbaca salah, transaksi yang seharusnya berhasil malah ditolak, sehingga pelanggan kehilangan pesanan dan merasa uangnya hilang. Pada akhirnya pelanggan kehilangan kepercayaan, dan FoodGo kehilangan penjualan. Eventual Consistency lebih cocok untuk data seperti jumlah like di media sosial, karena jika jumlah like terlambat beberapa detik, tidak ada yang dirugikan dan tidak ada keputusan penting yang bergantung pada angka tersebut. Untuk data keuangan, model Eventual Consistency kurang cocok.

    Jika menggunakan Sequential Consistency, semua server harus sepakat pada urutan operasi yang sama sebelum operasi dianggap selesai. Namun, biaya Sequential Consistency relatif mahal. Setiap pembaruan data harus menunggu konfirmasi dari server lain, padahal server berada di kota yang berbeda dan jaraknya menambah delay. Hal tersebut dapat membuat aplikasi menjadi lambat, dan jika koneksi antara Jakarta dan Bandung terganggu, pembaruan data bisa terhambat. Padahal, masalah di kasus FoodGo sebenarnya lebih sempit daripada yang diselesaikan Sequential Consistency. Yang dikeluhkan adalah pelanggan tidak melihat top-up miliknya sendiri, bukan seluruh server harus selalu sepakat soal setiap operasi. Karena itu, kebutuhan kasus ini berada di antara keduanya, yaitu tidak cukup jika hanya Eventual Consistency, tetapi tidak harus sampai Sequential Consistency. Pelanggan perlu dijamin selalu melihat data terbarunya sendiri, dan jaminan tersebut bisa diberikan lewat Client-Centric Consistency, yaitu Read-Your-Writes.


2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
