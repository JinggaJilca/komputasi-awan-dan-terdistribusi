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
| ... | ... | ... | ... | ... |
