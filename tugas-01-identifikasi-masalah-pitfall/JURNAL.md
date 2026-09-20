# Jurnal Proses — Tugas 1


## Kamis, 17 September 2026
- Peserta: Jingga Jil Carissa, Nayyara Aurelia Putri, Neista Arsha Javana
- Poin diskusi: 
  - Memahami pitfall

  - Menentukan bagian pitfall yang akan diambil masing-masing anggota
  - Menentukan arsitektur untuk FoodGo

- Perbedaan pendapat (jika ada): 

  - Trade off hanya salah satu pitfall atau mencakup keseluruhan
  - Terdapat kasus yang memiliki jenis Fallacies of Distributed Computing yang sama
  - Penggunaan Message-Oriented Middleware (MOM) sebagai arsitektur dinilai kurang tepat karena hanya untuk membantu menyampaikan pesan agar tidak duplikasi

 -  Solusi
    - Mengidentitfikasi trade-off dari setiap solusi yang dianalisis tiap pitfall

    - Tetap menganalisa masing-masing gejala untuk mengetahui perbedaannya

    - Memilih arsitektur SOA untuk solusi dari FoodGo
       
## Minggu, 20 September 2026

- Peserta: Jingga Jil Carissa, Nayyara Aurelia Putri, Neista Arsha Javana
- Poin diskusi: 
  - Memberikan tanggapan terhadap masing-masing analisis pitfall
  - 

- Perbedaan pendapat (jika ada): 

 
- Solusi

## Review Silang
- Jingga Jil Carissa mengomentari analisis Neista Arsha Javana (Pitfall 1): "Latency is Zero"
 menurut saya sangat mustahil aplikasi menghilangkan latensi karena sangat bergantung pada sinyal, perangkat keras dan sistem operasi. Namun hal tersebut dapat ditangani dengan menerapkan latensi yang rendah dan masih bisa ditolerir oleh pengguna sekitar di bawah 40 ms. Atau menerapkan metode caching agar data dapat diakses lebih cepat atau mengubah arsitektur dan komunikasi 
## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|17 September 2026 | Gemini | Jelaskan seluruh 8 Fallacies of Distributed Computing beserta kasus pada dunia nyata | Memberikan penjelasan komprehensif mengenai 8 asumsi keliru jaringan beserta contoh kasus di sistem nyata | Menggunakan penjelasan sebagai dasar pemahaman studi untuk kasus skenario FoodGo |
|17 September 2026|Gemini|Koreksi analisis saya mengenai pitfall pada bandwith is infinite dengan keterkaitannya RAM/CPU crash|Meluruskan bahwa bandwidth overload tidak langsung memicu crash CPU/RAM, melainkan menumpuk request di buffer hingga pemicu Out of Memory (OOM)|Asumsi bahwa bandwidth tidak terbatas (bandwidth is infinite) berisiko memicu kemacetan jaringan (network congestion) saat terjadi lonjakan pengguna. Batas bandwidth yang terlampaui membuat paket data tertahan di antrean memori. Penumpukan koneksi yang tertahan ini memaksa server mengalokasikan RAM dan thread secara berlebihan hingga memicu kondisi Out of Memory (OOM) dan crash pada sistem.|
|17 September 2026|Gemini|Jelaskan mengenai penyebab terjadinya deadlock dan hubungannya dengan lonjakan request|Menjelaskan bahwa lonjakan request bukan penyebab utama deadlock, melainkan pemicu (trigger) munculnya bug locking pada kode (Coffman Conditions).|Memahami analisis deadlock pada asumsi Bandwith is Infinite dan mekanisme kegagalannya pada kasus FoodGo|
|---|---|---|---|---|
|---|---|---|---|---|
|---|---|---|---|---|




