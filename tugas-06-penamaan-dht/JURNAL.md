# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Terjadi error pada baris terakhir saat menggunakan `return self.nodes[0]`. Hal ini dikarenakan `self.nodes` merupakan dictionary yang menyimpan `node_id` sebagai key, sehingga ketika dijalankan muncul pesan error karena `self.nodes[0]` tidak mengambil elemen pertama, melainkan mencari key bernilai 0. 
- Cara memperbaikinya: Menyimpan hasil pengurutan `self.nodes` ke dalam variabel baru bernama `nodes_id` menggunakan `sorted(self.nodes.keys())`, lalu mengembalikan nilai `nodes_id[0]`. Sehingga **find_successor** berhasil mengembalikan nilai node_id terkecil sesuai dengan konsep wrap_around.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20/10/2026 | Gemini | **Mekanisme Logika `join()`**<br>Menanyakan alasan teknis pelepasan node sementara (`pop`) sebelum pencarian *successor*. | Menjelaskan bahwa pelepasan ID node sementara bertujuan agar pencarian *successor* tidak mengembalikan ID node itu sendiri, melainkan mengidentifikasi penanggung jawab wilayah sebelum node baru bergabung. | Menerapkan alur *pop-then-push* pada metode pendaftaran node baru untuk mengidentifikasi pemilik lama data secara akurat. |
| 20/10/2026 | Gemini | **Logika Pemindahan Data `leave()`**<br>Diskusi cara kerja pemindahan data kurir ke successor* baru saat sebuah node keluar. | Menjelaskan bahwa pada simulasi *single-process*, data tidak perlu dipindah secara fisik, melainkan perubahan hak kelola terjadi secara otomatis melalui pembacaan ulang struktur ring dan pencatatan log transaksi. | Menyusun alur logika pasang-lepas node pada perulangan data untuk mendeteksi pemilik lama dan menentukan *successor* penerus. |
| 20/10/2026 | Gemini | **Debugging `IndexError`**<br>Menganalisis penyebab `IndexError: list index out of range` pada fungsi pencarian *successor*. | Menganalisis bahwa *exception* terjadi akibat pengaksesan indeks pertama pada koleksi ID node yang masih kosong ketika node pertama di dalam ring diproses. | Menambahkan validasi kondisi batas (*guard clause*) untuk menangani status ring saat belum memiliki node terdaftar. |
| 23/10/2026 | Gemini | **Troubleshooting Bug Penumpukan Data**<br> Menganalisis penyebab seluruh data tersimpan pada satu node dan pengembalian *successor* bernilai `None`. | Menjelaskan kesalahan logika pengondisian pada metode `join()`, di mana instruksi pendaftaran ulang node secara tidak sengaja terisolasi di dalam blok kondisi node pertama, sehingga node berikutnya terhapus permanen dari ring. | Mengubah cakupan (*scope*) instruksi pendaftaran ulang node agar selalu dieksecusi di luar blok pengondisian. |
| 23/10/2026 | Gemini | **Verifikasi Logika Chord DHT**<br> Memeriksa kesesuaian implementasi fungsi *lookup*, *join*, dan *leave* terhadap spesifikasi tugas. | Mengonfirmasi bahwa pemetaan *Consistent Hashing* 8-bit, penentuan *successor*, dan penanganan perubahan topologi ring telah sesuai dengan aturan algoritma Chord. | Memastikan seluruh fungsi dasar berjalan dan menghasilkan *output* yang konsisten sesuai skenario pengujian. |
| 23/10/2026 | Gemini | **Analisis Topologi & Range ID**<br>Meminta penjelasan peralihan wilayah ID saat sebuah node keluar dan konsep *wrap-around*. | Menjelaskan bahwa pengambilalihan wilayah ID bergerak searah jarum jam (ID >= key_hash), sehingga saat node dengan ID terbesar keluar, tanggung jawab dialihkan ke node dengan ID terkecil melalui mekanisme *wrap-around*. | Menyusun narasi analisis topologi ring dan mengonfirmasi bahwa tidak adanya log pemindahan data disebabkan oleh tidak adanya key yang menempati rentang ID node yang keluar. |
