# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
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
