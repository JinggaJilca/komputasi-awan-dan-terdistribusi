# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

**Kelompok:** Kelompok 2

| Nama | NIM |
|---|---|
| Neista Arsha Javana | 103072400067 | 
| Nayyara Aurelia Putri | 103072400097 |
| Jingga Jil Carissa | 103072400121 |

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Hasil Analisis
### Kenapa perlu leader
Dalam sistem terdistribusi, leader adalah satu node yang dipilih untuk memegang kendali atas suatu tugas, sementara node lainnya mengikuti keputusannya. Fungsi utamanya adalah menjadi satu-satunya pusat pengambilan keputusan, misalnya menentukan urutan pekerjaan, sehingga semua node punya acuan yang sama. Tanpa leader, setiap node memutuskan sendiri-sendiri. Masing-masing node bisa memiliki jam dan data yang berbeda, jadi hasilnya bisa saling bertentangan sehingga urutan kerja tidak sama dan pekerjaan yang sama bisa diproses lebih dari sekali.

Hal ini juga yang terjadi pada kasus FoodGo. Dua server mencatat urutan pesanan yang berbeda karena jam keduanya tidak sinkron, sehingga pesanan yang masuk hampir bersamaan bisa dianggap datang lebih dulu oleh server A, tetapi belakangan oleh server B. Akibatnya pesanan bisa diproses ganda atau dengan urutan yang berbeda. Dengan adanya satu node leader yang mengelola antrean pesanan pusat, semua pesanan diurutkan di satu tempat dan node lain cukup mengikutinya, sehingga urutan tidak lagi bergantung pada jam masing-masing server.

Namun leader juga bisa mati. Jika tidak ada pengganti, antrean pesanan ikut macet. Karena itu dibutuhkan election, yaitu cara otomatis memilih leader baru, supaya sistem tetap berjalan tanpa perbaikan manual.

### Trade Off Bully Algorithm vs Raft Algorithm
Bully Algorithm menerapkan perbandingan ID tertinggi untuk menentukan leader. Hal ini dapat di lihat pada pengujian skenario pertama (start normal) di mana node 5 otomatis terpilih sebagai leader, serta pada skenario kedua ketika node 4 berhasil mengambil alih posisi leader dalam waktu 3-5 detik setelah node 5 dimatikan. Sebaliknya, Raft algorithm menggunakan sistem suara terbanyak dan waktu tunggu acak untuk memastikan proses pemilihan berjalan dengan adil dan konsisten. 

Adapun trade off dari kedua algoritma tersebut meliputi:
1. Bully Algorithm: ketika node dengan ID terendah memulai ELECTION, setiap node di atasnya yang menerima pesan juga akan memulai proses election masing-masing. Hal ini menimbulkan konkurensi serta penumpukan thread. Selain itu, bully algorithm menyebabkan jeda layanan sementara sebelum leader baru terpilih.
2. Raft Algoritm: memilki logika dan struktur kode yang lebih kompleks dibandingkan bully algorithm. Selain itu, proses pergantian leader mewajibkan adanya suara mayoritas, sehingga jika jumlah node yang mati melebihi batas mayoritas, sistem tidak bisa memilih leader baru.

### Hasil Pengujian 2 skenario
Pada skenario pertama (start normal), kelima node dinyalakan satu per satu dari node 1 sampai node 5 di terminal terpisah. Setiap node yang menyala memulai election dengan mengirim ELECTION ke node ber-ID lebih besar. Karena node-node tersebut belum hidup, tidak ada balasan OK, sehingga setelah menunggu 2 detik (ELECTION_TIMEOUT) node itu menyatakan dirinya leader dan mengirim COORDINATOR ke node lain. Akibatnya leader sempat berpindah dari node 1 ke 2, 3, dan 4. Saat node 5 menyala, ia tidak punya node dengan ID lebih besar, sehingga langsung menjadi leader dan mengirim COORDINATOR ke node 1 sampai 4. Hasil akhirnya, node 5 terpilih sebagai leader dan keempat node lain mencatatnya. Pesan ELECTION dan OK tidak muncul di log karena node yang lebih besar belum hidup saat election dimulai. Jika kelima node dinyalakan hampir bersamaan, kedua pesan itu seharusnya muncul, tetapi hasil akhirnya tetap node 5.

Pada skenario kedua (leader dimatikan), node 5 dihentikan dengan Ctrl+C. Node 1 sampai 4 mendeteksi bahwa node 5 tidak merespons PING lewat monitor_leader, lalu masing-masing memulai election. Node 1 sampai 3 menerima balasan OK dari node di atasnya yang masih hidup, sehingga mereka berhenti mencalonkan diri. Node 4 tidak mendapat balasan dari node 5 sampai batas waktu habis, jadi ia menyatakan dirinya leader baru dan mengirim COORDINATOR ke semua node yang masih hidup. Node 4 terpilih sebagai leader baru, yaitu node ber-ID tertinggi yang tersisa. Waktu sampai leader baru terpilih sekitar 2 sampai 5 detik, dipengaruhi interval pengecekan monitor_leader (3 detik) dan ELECTION_TIMEOUT (2 detik). Karena beberapa node memicu election hampir bersamaan, pesan COORDINATOR dari node 4 bisa muncul lebih dari sekali di log, tetapi hasil akhirnya tetap node 4.


## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
