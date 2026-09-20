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

- Perbedaan pendapat (jika ada): 

  - Mengapa memakai arsitektur SOA karena terbagi menjadi beberapa modul, dan faktor crash lebih kecil sehingga SOA dinilai efisien

## Review Silang
- Jingga Jil Carissa mengomentari analisis Neista Arsha Javana (Pitfall 1): "Latency is Zero"
 menurut saya sangat mustahil aplikasi menghilangkan latensi karena sangat bergantung pada sinyal, perangkat keras dan sistem operasi. Namun hal tersebut dapat ditangani dengan menerapkan latensi yang rendah dan masih bisa ditolerir oleh pengguna sekitar di bawah 40 ms. Atau menerapkan metode caching agar data dapat diakses lebih cepat atau mengubah arsitektur dan komunikasi
- Neista Arsha Javana mengomentari analisis Nayyara Aurelia Putri (Pitfall 2): "Network is Reliable". Identifikasi skenario dan analisis dampak awal yang dibuat sudah tepat, terutama pada poin ketiadaan timeout yang menyebabkan thread blocking serta risiko packet loss saat jaringan tidak stabil. Namun menurut saya, scale up pada sever tidak menyelesaikan masalah, karena pada akhirnya thread server tetap akan habis dan malah mengabiskan resource.
- Nayyara Aurelia Putri mengomentari analisis Jingga Jil Carissa (Pitfall 3): "Bandwith is Infinite". Dampak yang di timbulkan sudah di jelaskan dengan baik. Karena gejala yang terjadi pada FoodGo "Server backend kadang crash" menandakan adanya kegagalan pada sistem yang dapat memicu kondisi Out-Of-Memory (OOM) dan deadlock. Namun menurut saya, pada solusi awal desain diperlukannya tambahan mekanisme pemisahan jalur, agar ketika terjadinya lonjakan beban di salah satu modul, sistem akan pulih secara otomatis tanpa perlu dilakukannya reset server secara manual.
## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|17 September 2026 | Gemini | Jelaskan seluruh 8 Fallacies of Distributed Computing beserta kasus pada dunia nyata | Memberikan penjelasan komprehensif mengenai 8 asumsi keliru jaringan beserta contoh kasus di sistem nyata | Menggunakan penjelasan sebagai dasar pemahaman studi untuk kasus skenario FoodGo |
|17 September 2026|Gemini|Koreksi analisis saya mengenai pitfall pada bandwith is infinite dengan keterkaitannya RAM/CPU crash|Meluruskan bahwa bandwidth overload tidak langsung memicu crash CPU/RAM, melainkan menumpuk request di buffer hingga pemicu Out of Memory (OOM)|Asumsi bahwa bandwidth tidak terbatas (bandwidth is infinite) berisiko memicu kemacetan jaringan (network congestion) saat terjadi lonjakan pengguna. Batas bandwidth yang terlampaui membuat paket data tertahan di antrean memori. Penumpukan koneksi yang tertahan ini memaksa server mengalokasikan RAM dan thread secara berlebihan hingga memicu kondisi Out of Memory (OOM) dan crash pada sistem.|
|17 September 2026|Gemini|Jelaskan mengenai penyebab terjadinya deadlock dan hubungannya dengan lonjakan request|Menjelaskan bahwa lonjakan request bukan penyebab utama deadlock, melainkan pemicu (trigger) munculnya bug locking pada kode (Coffman Conditions).|Memahami analisis deadlock pada asumsi Bandwith is Infinite dan mekanisme kegagalannya pada kasus FoodGo|
|17 September 2026|Gemini|Apa solusi desain awal untuk mengatasi thread blocking akibat ketiadaan timeout pada pemanggilan antar modul, dan apa trade off yang dikorbankan?|Solusi awalnya yaitu memberikan timeout dan menggunakan prinsip circuit breaker pattern. trade offnya adalah mengorbanan keberhasilan transaksi sementara (fail-fast) dan kenyamanan serta waktu pengguna demi menjaga seluruh sistem.|Menulis ulang penjelasan dengan bahasa sendiri, menyesuaikannya dengan studi kasus FoodGo, serta memperjelas dampak kegagalan transaksi (fail-fast) pada user experience dan potensi pendapatan.|
|17 September 2026|Gemini|Tolong jelaskan perbedaan arsitektur Layered, SOA, Peer-to-Peeer, Pub-Sub, dan MOM. dan buatkan tabel perbandingan 5 arsitektur tersebut yang merangkum konsep, kelebihan dan kekurangannya, serta contoh kasus penggunaannya.|Menjelaskan perbedaan, konsep, kelebihan, kekurangan dan contoh kasus penggunaan dari arsitektur Layered, SOA, Peer-to-Peer, Pub-Sub, dan MOM.|Memahami perbedaan, konsep, kelebihan, kekurangan, serta kasus penggunaan dari masing-masing arsitektur serta melakukan analisis kombinasi arsitektur untuk kegagalan yang dialami oleh FoodGo.|
