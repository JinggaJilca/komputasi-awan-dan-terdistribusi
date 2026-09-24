# Jurnal Proses — Tugas 2

## Kamis, 24 September 2026
- Opsi arsitektur yang dipertimbangkan: Service Oriented Architecture (SOA) dan Message Oriented Middleware (MOM)
- Kenapa akhirnya pilih [SOA + MOM]: Karena mempertimbangan lonjakan traffic, sistem FoodGo harus tetap responsif dengan pengguna dan tahan crash pada promo jam makan siang 
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):  Memisahkan jalur read dan write untuk membantu pembacaan alur MOM
- 

## Log Penggunaan AI (Level 2)
| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|24 September 2026 | Gemini | Apa bedanya MOM dengan publish dan subscribe | MOM adalah istilah umum untuk perangkat lunak perantara (middleware) yang memungkinkan aplikasi-aplikasi terdistribusi saling berkirim pesan secara asinkron, alih-alih melakukan pemanggilan langsung (direct synchronous call). Sedangkan Pub-Sub adalah pola komunikasi (design pattern) di dalam dunia messaging.| Menggunakan penjelasan sebagai dasar pemahaman studi untuk pemilihan arsitektur |
|24 September 2026 | Gemini | Analisis efisiensi arsitektur SOA, Pub subscribe, dan SOA + MOM | Menampilkan Matriks Evaluasi Efisiensi Indikator Efisiensi | Meninjau keakuratan isi indikator efisiensi per arsitektur (SOA, Pub-Sub, SOA+MOM), menyelaraskan istilah teknis, lalu memasukkannya ke berkas |
|..|..|..|....|..


