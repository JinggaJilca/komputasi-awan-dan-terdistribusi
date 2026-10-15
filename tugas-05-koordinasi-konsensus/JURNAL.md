# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: ...

## Skenario 1: Start normal
- Leader yang terpilih: Node 5 (node ber-ID tertinggi)
- Log/observasi:
Kelima node dinyalakan satu per satu secara berurutan dari node 1 sampai node 5, dengan masing-masing di terminal terpisah. Tujuan dari program ini adalah memilih satu node yang menjadi leader, yaitu node yang bertugas mengatur antrean pesanan pusat. Pemilihan ini disebut election, dengan aturan node yang hidup dengan ID paling besar yang menang untuk menjadi leader.

Saat node 1 dinyalakan, leader belum ada, sehingga node 1 memulai election dengan mengirim pesan ELECTION ke node 2, 3, 4, dan 5. Namun node-node tersebut belum menyala, sehingga tidak ada satu pun yang membalas. Setelah menunggu selama 2 detik (ELECTION_TIMEOUT), node 1 menyimpulkan bahwa tidak ada node yang lebih besar darinya yang hidup. Maka node 1 menyatakan dirinya sebagai leader dengan mengirim pesan COORDINATOR. Pesan COORDINATOR merupakan pengumuman bahwa hasil election sudah ditentukan dan node tersebut adalah leader.

Ketika node 2 dinyalakan, node 2 mengirim ELECTION ke node 3, 4, dan 5 yang belum hidup, menunggu 2 detik, lalu menyatakan dirinya leader dan mengirim COORDINATOR ke semua node lain. Node 1 yang menerima pesan itu mengganti catatan leadernya dari node 1 menjadi node 2. Node 2 mengumumkan dirinya sebagai leader, dan node 1 menerima serta mencatatnya. Begitu juga saat node 3 dan node 4 menyala, masing-masing mengumumkan dirinya sebagai leader, jadi leader sempat berpindah ke node 3, lalu ke node 4.

Terakhir, saat node 5 dinyalakan, ia tidak memiliki node dengan ID lebih besar (higher_peers kosong). Karena itu node 5 tidak perlu mengirim ELECTION atau menunggu balasan, dan langsung menyatakan dirinya leader dengan mengirim COORDINATOR ke node 1 sampai 4. Karena tidak ada node yang lebih besar dari 5, tidak akan ada lagi yang menggantikannya, sehingga node 5 menjadi leader final. Node 1 sampai 4 menerima COORDINATOR dari node 5 dan mencatat node 5 sebagai leader, sehingga kelima node sepakat pada leader yang sama.

Di log tidak muncul pesan ELECTION maupun OK, karena node dinyalakan satu per satu dengan jeda cukup lama, jadi node yang lebih besar belum hidup saat election dimulai. Kalau kelima node dinyalakan hampir bersamaan, kedua pesan itu seharusnya muncul, tapi hasil akhirnya tetap node 5.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: ...
- Berapa lama waktu sampai leader baru terdeteksi: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
