# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:
1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut *successor*).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

Soal 1: Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal. (Neista)

#### Jawaban No.1:

Soal 2: Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana. (Nayya)

#### Jawaban No.2:

Soal 3: Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.

#### Jawaban No.3:
Didapatkan output program sebagai berikut:
```bash
[JOIN] Node 'node-jakarta-1' (id=177) bergabung, alamat 10.0.0.1
[JOIN] Node 'node-jakarta-2' (id=102) bergabung, alamat 10.0.0.2
[JOIN] Node 'node-bandung-1' (id=40) bergabung, alamat 10.0.0.3
[JOIN] Node 'node-surabaya-1' (id=136) bergabung, alamat 10.0.0.4
```

Berikut gambaran dari topologi ring
```                        
                     [ ID: 40 ]
                    node-bandung-1
                      (10.0.0.3)
                      /        \
                     /          \
        [ ID: 177 ]                [ ID: 102 ]
      node-jakarta-1              node-jakarta-2
        (10.0.0.1)                  (10.0.0.2)
              \                      /
               \                    /
          [ ID: 136 ] ------- [ ID: 123 ]
        node-surabaya-1       node-medan-1
          (10.0.0.4)           (10.0.0.5)

```


Node telah diurutkan ascending (terkecil ke terbesar) pada program node dengan id =  177 yaitu node-jakarta-1 akan keluar dari ring

```bash
[LEAVE] Node 'node-jakarta-1' (id=177) keluar dari ring
```

Selanjutnya, successor yang meneruskan pada lokasi terdekat dan bertanggung jawab adalah node-bandung-1, id = 40 karena ring melingkar sehingga node-bandung-1 akan mengambil seluruh wilayah dengan id = 137 - 177

``` bash
--- Sebuah node keluar ---
[LEAVE] Node 'node-jakarta-1' (id=177) keluar dari ring
kurir-001 -> 192.168.1.10
kurir-002 -> 192.168.1.11
```

Karena kurir tidak ditugaskan pada node-jakarta-1 sehingga tidak memunculkan log pesan, sehingga keluarnya node tidak merusak struktur pencarian pada node-node lain yang masih aktif


## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi lookup/join/leave benar | 35% | Consistent hashing & successor lookup sesuai aturan Chord |
| Bukti perubahan topologi (join/leave) | 25% | Output menunjukkan mapping berpindah dengan benar |
| Analisis kenapa DHT vs flat naming/DNS | 25% | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
