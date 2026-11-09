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

    Jawaban:

    Pendekatan yang kami usulkan adalah Read-Your-Writes. Alasannya adalah karena bug di kasus ini terjadi karena pelanggan tidak melihat hasil top-up miliknya sendiri. Read-Your-Writes dapat menjamin pelanggan yang baru mengubah datanya, misalnya top-up saldo, selalu melihat hasil perubahannya sendiri, walau server lain belum sinkron. Pendekatan ini lebih ringan daripada Sequential Consistency, karena jaminannya hanya berlaku untuk pelanggan yang bersangkutan dan server tidak perlu saling menunggu pada setiap operasi.

    Cara kerjanya dapat diterapkan dengan menggunakan nomor versi. Setiap kali saldo berubah, server yang menerima penulisan memberi nomor versi baru pada saldo tersebut. Contohnya, saldo pelanggan berada di versi 5, lalu ketika top-up di Jakarta, nomor versinya menjadi 6. Server Jakarta mengirim nomor versi 6 kembali ke aplikasi pelanggan, dan aplikasi menyimpannya sebagai bukti bahwa pelanggan tersebut sudah mengubah data sampai versi 6. Setiap kali aplikasi membaca saldo atau memesan makanan, aplikasi menyertakan nomor versi terakhir yang disimpannya.

    Saat permintaan tersebut sampai di server Bandung, server memeriksa versi saldo di dalam salinannya. Jika versinya sudah 6 atau lebih baru, Bandung langsung menjawab. Jika versinya masih 5, berarti pembaruan dari Jakarta belum sampai. Server Bandung tidak boleh menjawab dengan saldo lama, dan ada dua pilihan. Pilihan yang pertama, Bandung menunggu beberapa saat sampai pembaruan tiba, lalu menjawab. Pilihan kedua, Bandung meneruskan permintaan ke Jakarta untuk mengambil saldo terbaru. Dengan begitu, pelanggan yang baru top-up tidak pernah ditolak karena saldo lama.

    Pelanggan lain yang tidak baru memperbarui tidak terkena aturan ini. Pelanggan lain tetap dilayani langsung oleh server terdekat tanpa menunggu, sehingga aplikasi tetap cepat. Hanya pelanggan yang baru top-up yang mungkin menunggu sebentar, dan itu hanya terjadi saat pembaruan belum selesai. Namun, Read-Your-Writes memiliki batasan, Read-Your-Writes hanya menjamin satu pelanggan melihat perubahannya sendiri, dan tidak mencegah dua server mengubah saldo yang sama pada waktu bersamaan, sehingga salah satu perubahan bisa tertimpa. Karena itu, untuk operasi yang memotong saldo, misalnya pembayaran, sebaiknya perubahan selalu diproses di satu server utama milik pelanggan tersebut, sehingga urutannya jelas dan tidak bertabrakan.

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

## Skenario Tambahan

### Studi Kasus Client-Centric Consistency dengan Monotonic Writes pada System E-Learning (LMS)

Sebuah platform e-learning (LMS) menggunakan arsitektur basis data terdistribusi berbasis replikasi yang tersebar di dua wilayah: **Server Bandung** dan **Server Surabaya**.

Seorang dosen sedang menyiapkan tugas perkuliahan minggu ke-10 dengan alur sebagai berikut:

```
                      ┌────────────────────────────────────────┐
                      │    Pengguna (Dosen / Mobile Client)    │
                      └──────────────────┬─────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
          (1) Write 1 (W₁)                                (2) Write 2 (W₂)
          Tambah Tugas M10                                Tambah Catatan Tugas
                 │                                               │
                 ▼                                               ▼
      ┌─────────────────────┐                         ┌─────────────────────┐
      │   Server Bandung    │ ─── (Replikasi Delay) ─►│   Server Surabaya   │
      └─────────────────────┘                         └─────────────────────┘
```

* **Write 1 ($W_1$) — Server Bandung:**  
  Dosen membuat tugas baru:  
  `Tambah Penugasan: "Tugas Minggu ke-10" (ID_Tugas: TUGAS-M10)`
* **Write 2 ($W_2$) — Server Surabaya:**  
  Karena koneksi internet dosen berpindah atau di-route ulang ke Server Surabaya, dosen menambahkan catatan petunjuk tugas tersebut:  
  `Tambah Catatan: "Pengumpulan maksimal Jumat jam 23:59" pada (ID_Tugas: TUGAS-M10)`

---

## Analisa Kasus Tanpa Monotonic Writes

Jika sistem **tidak menjamin** *Monotonic Writes*, urutan eksekusi penulisan dari klien yang sama dapat berantakan di server target.

### Alur Masalah (*Race Condition*)
1. **$W_1$ diproses di Bandung:** Data `TUGAS-M10` berhasil tersimpan di basis data Server Bandung.
2. **Replikasi Lambat:** Terjadi *delay* jaringan dalam pengiriman data $W_1$ dari Bandung ke Surabaya.
3. **$W_2$ Tiba Lebih Dulu di Surabaya:** Server Surabaya menerima request $W_2$ sebelum data $W_1$ sempat direplikasikan ke Surabaya.
4. **Eksekusi Gagal:** Server Surabaya mencoba memasukkan catatan ke tabel `catatan_tugas` dengan referensi `ID_Tugas: TUGAS-M10`.

### Dampak pada Sistem
* **Database Error:** Terjadi *Foreign Key Constraint Violation* (`Assignment ID TUGAS-M10 Not Found`).
* **Data Corrupt/Orphan:** Catatan terbuat tanpa ada tugas utamanya (*orphan record*).
* **User Experience Buruk:** Muncul pesan error pada layar dosen atau instruksi tugas hilang.

---

## Kesimpulan

Model **Monotonic Writes** menjamin aturan bahwa jika operasi $W_1$ dilakukan sebelum $W_2$ oleh klien yang sama, maka di replika mana pun $W_1$ **diwajibkan diproses terlebih dahulu** sebelum $W_2$.

Pada aplikasi LMS terdistribusi, **Monotonic Writes** memastikan bahwa dependensi antar-operasi penulisan yang dilakukan oleh seorang pengguna (seperti dosen yang membuat tugas lalu menambahkan catatan) akan diproses dalam **urutan kausalitas logis yang sama** di seluruh replika server.
