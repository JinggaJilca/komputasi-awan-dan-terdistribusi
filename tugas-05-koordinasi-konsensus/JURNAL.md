# Jurnal Proses — Tugas 5

## Implementasi Bully
| No | Kategori Kendala | Deskripsi Kendala | Dampak pada Program | Solusi / Penanganan |
|---|---|---|---|---|
| 1 | **Deadlock & Thread Lock** | Memanggil `start_election()` yang memiliki proses *blocking* (`time.sleep`) di dalam blok `with self.lock:`. | Thread socket penerima terblokir total dan tidak bisa memproses balasan pesan `"OK"` atau `"COORDINATOR"`. | Mengeluarkan panggilan `start_election()` dari blok `lock` dan menjalankannya di thread terpisah (`threading.Thread`). |
| 2 | **Syntax Error (`TypeError`)** | Menggunakan tanda kurung `higher_peers()` saat mengecek apakah dictionary peer kosong. | Program *crash* dengan error `TypeError: 'dict' object is not callable`. | Mengubah pengecekan kondisi menjadi `if not higher_peers:` tanpa menggunakan tanda kurung `()`. |
| 3 | **Struktur Logika & Scope Variabel** | Penempatan indentasi `if not is_leader_alive:` di luar blok pemeriksaan `leader_port` pada `monitor_leader()`. | Memicu `UnboundLocalError` jika port `None`, serta membuat thread *election* terpicu terus-menerus meski leader masih hidup. | Memasukkan pengecekan status ping dan pemicuan thread *election* tepat di dalam blok `if leader_port is not None:`. |
| 4 | **Kesalahan Pengiriman Pesan Socket** | Mem-ping port sendiri (`self.port`) serta memanggil `send_message("COORDINATOR")` tanpa argumen port tujuan. | Ping gagal mendeteksi status leader yang sebenarnya dan pesan coordinator gagal terkirim ke semua node. | Mengambil port leader dari `self.peers` dan melakukan *looping* ke seluruh port peer saat melakukan *broadcast* `COORDINATOR`. |
| 5 | **Sinkronisasi State Antar-Thread** | Lupa mereset `self.flag_ok.clear()` sebelum pemilihan dan lupa mereset `self.leader_id = None` saat leader mati. | Terjadi *race condition* atau pembacaan status pemilihan yang salah akibat membawa nilai dari pemilihan sebelumnya. | Menambahkan `self.flag_ok.clear()` di awal `start_election()` dan mereset `self.leader_id = None` di dalam `with self.lock:` saat ping gagal. |
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
| 15 Okt 2026 | Gemini |Bagaimana dan fungsi on_message()?" & Mengapa harus threadlock, padahal bisa self.lock | Penjelasan penanganan jenis pesan `ELECTION`, `OK`, `COORDINATOR`, serta edukasi bahwa `with self.lock:` tidak boleh membungkus proses *blocking* (`sleep`/koneksi socket) agar tidak memicu *deadlock*. | Menerapkan `threading.Thread(target=self.start_election, daemon=True).start()` saat menerima `ELECTION` di `on_message()` tanpa membungkusnya di dalam `self.lock`. |
| 15 Okt 2026 | Gemini | "Gunakan flag/event yang sudah di-set saat menerima OK dari start_election" | Menggunakan `threading.Event()` (`self.flag_ok`) untuk sinkronisasi antar-thread antara penerimaan pesan `OK` di `on_message()` dan penungguan balasan di `start_election()`. | Menginisialisasi `self.flag_ok = threading.Event()`, memanggil `self.flag_ok.set()` pada `on_message()`, serta mengecek `self.flag_ok.wait(timeout=ELECTION_TIMEOUT)` di `start_election()`. |
| 15 Okt 2026 | Gemini | Evaluasi dan koreksi alur logika pada fungsi `monitor_leader()` | Memperbaiki kesalahan *ping* ke port sendiri, mengecek *return value* boolean `send_message()`, mereset `leader_id`, dan memperbaiki struktur indentasi `if` agar tidak terjadi `UnboundLocalError`. | Menyusun fungsi `monitor_leader()` dengan mengambil `leader_port` dari `self.peers.get(current_leader_id)`, memeriksa koneksi `PING`, lalu mereset `self.leader_id = None` dan memicu election jika ping gagal. |
| 15 Okt 2026 | Gemini | Jelaskan tentang leader_id, ock, apa bedanya dengan sender_id" & Analisis error `TypeError: 'dict' object is not callable` | Penjelasan konseptual beda *shared state* (`leader_id`), data lokal sementara (`sender_id`), dan pengaman *thread safety* (`lock`), serta koreksi sintaks `higher_peers()` yang merupakan dictionary. | Menghapus tanda kurung pada `if not higher_peers:` di `start_election()` dan merevisi *looping broadcast* `send_message(port, "COORDINATOR")` di fungsi `declare_leader()`. |

