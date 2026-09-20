# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 2

| Nama | NIM | Kontribusi |
|---|---|---|
| Neista Arsha Javana | 103072400067 | Latency is Zero |
| Nayyara Aurelia Putri | 103072400097 | Network is Reliable |
| Jingga Jil Carissa | 103072400121 | Bandwidth is Infinite |

## Pitfall 1: Latency is Zero — ditulis oleh Neista Arsha Javana

**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout." dan "... tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)."


**Kenapa ini keliru**: Asumsi bahwa latency is zero merupakan analisa yang keliru, karena komunikasi melalui jaringan tidak pernah terjadi secara instan (0 milidetik). Pengiriman data selalu membutuhkan waktu untuk melalui jaringan (seperti kabel dan router), serta sangat bergantung pada kecepatan pemrosesan dan kondisi server tujuan. 

**Dampak ke FoodGo**: Ketiadaan timeout membuat thread di modul pesanan terhenti (mengalami blocking) karena terus menunggu respon dari modul pembayaran tanpa batas waktu. Saat jam makan siang, penumpukkan thread yang menggantung ini dapat menghabiskan kapasitas pemrosesan server (thread exhaustion), sehingga aplikasi berjalan dengan sangat lambat. pesanan baru bertumpuk, dan proses server akhirnya mengalami crash secara menyeluruh.  

**Solusi desain awal:** 
1. Memasang timeout (batas waktu) sehingga saat tidak ada respons dalam kurun waktu tertentu, sistem akan langsung memutus koneksi secara sepihak dan membebaskan thread server.
2. Jika terjadi kegagalan berturut-turut pada pemanggilan modul pembayaran, maka request pemanggilan berikutnya akan ditolak dengan cepat tanpa membebani server.


**Trade-off:** FoodGo mengorbankan potensi pendapatan dari pengguna dan waktu atau kenyamanan pengguna saat terjadi gangguan demi mencegah server mati total (crash). Sistem lebih memilih menolak sebagian transaksi dengan cepat (fail-fast) daripada membiarkan seluruh aplikasi lumpuh untuk semua pengguna.

---

## Pitfall 2: Network is Reliable — ditulis oleh Nayyara Aurelia Putri

**Bukti di skenario:** "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)."

**Kenapa ini keliru:** Paket request yang dikirim tidak selalu dapat sampai secara utuh, karena jaringan dapat mengalami packet loss, ketidakstabilan, maupun terputus secara fisik. Mengasumsikan jaringan selalu andal adalah langkah yang keliru bagi developer, karna ketika gateway pembayaran lambat atau terjadi kesalahan pada jaringan, aplikasi akan terjebak pada infinite atau blocking wait tanpa adanya kepastian status yang jelas.

**Dampak ke FoodGo:** Ketika pesanan melonjak di jam makan siang, modul pesanan akan melakukan pemanggilan secara blocking ke modul pembayaran, karena modul pesanan tidak memasang timeout dan membiarkan threadnya menunggu balasan selamanya. Akhirnya, seluruh thread pool habis, dan membuat incoming request yang lain menjadi tertahan. Hal ini akan berakibat pada aplikasi yang melambat, dan dibutuhkannya scale up pada server.

**Solusi desain awal:** 
1. Memutus paksa blocking setelah durasi tertentu (misalnya 300 ms) agar thread tidak terjadi blocking selamanya.
2. Mencegah modul mengirim request secara terus-menerus.

**Trade-off:** FoodGo perlu membayar peningkatan kompleksitas engineering dan operasional, karena sistem memerlukan implementasi operasi yang menghasilkan hasil akhir yang sama meski telah dijalankan berkali-kali, dan menghindari terjadinya inkonsistensi data.

---

## Pitfall 3: Bandwidth is Infinite — ditulis oleh Jingga Jil Carissa

**Bukti di skenario:** "Server backend kadang crash total dan perlu di-restart manual".

**Kenapa ini keliru:**  Asumsi bahwa bandwidth tidak terbatas (bandwidth is infinite) berisiko memicu kemacetan jaringan (network congestion) saat terjadi lonjakan pengguna. Batas bandwidth yang terlampaui membuat paket data tertahan di antrean memori. Penumpukan koneksi yang tertahan ini memaksa server mengalokasikan RAM dan thread secara berlebihan hingga memicu kondisi Out of Memory (OOM) dan crash pada sistem.

**Dampak ke FoodGo:** Pada kasus FoodGo, lonjakan pengguna secara tiba-tiba (traffic spike) terjadi akibat diskon promo di jam makan siang. Ketika puluhan ribu pengguna mengakses aplikasi secara bersamaan, terjadi beberapa rentetan masalah teknis:

1. Pengiriman Data Berlebih: Server dipaksa mengirimkan seluruh data berat seperti detail pesanan, gambar menu beresolusi tinggi, hingga lokasi kurir melalui pemanggilan API (Application Programming Interface, yaitu antarmuka penghubung antar-aplikasi) tanpa adanya pembatasan atau penyaringan data.

2. Penyumbatan Jalur (Bottleneck): Lonjakan lalu lintas data ini melampaui batas maksimal bandwidth. Terjadilah penumpukan antrean permintaan (request) yang menyebabkan penurunan performa secara drastis (lag).

3. Kehabisan Sumber Daya (Resource Exhaustion): Penumpukan request yang tidak kunjung terproses ini memaksa server menampung data di dalam memori sementara. Akibatnya, penggunaan RAM (Random Access Memory) dan pemrosesan CPU (Central Processing Unit) mencapai kapasitas maksimal 100%.

4. Penghentian Paksa oleh Sistem Operasi (OOM Killer): Karena memori habis total (Out of Memory), Sistem Operasi (OS) server secara otomatis menghentikan (kill) proses backend secara paksa untuk menyelamatkan mesin dasar. Akibatnya, aplikasi crash total dan tidak bisa pulih sendiri tanpa tindakan restart manual.
5. Skenarion terparah selain masalah kehabisan memori, lonjakan request yang sangat cepat di jam sibuk memicu terjadinya deadlock (kondisi kebuntuan di mana dua atau lebih proses saling mengunci dan berhenti permanen karena saling menunggu).

**Solusi desain awal:** 

1. Pagination dan Optimasi Payload API untuk mengurangi ukuran data dengan membatasi 1 halaman hanya 10 - 20 item. 
2. Kompresi file berupa CDN (Content Delivery Network) agar lebih kecil untuk foto menu, logo toko.
3. Pembatasan Lalu Lintas membatasi jumlah pemintaan misalnya 10 request/detik.

**Trade-off:**

Penggunaan CDN dan API Gateaway membuat biaya operasional membengkak
Melakukan pembatasan lalu lintas juga menyebabkan menurunnya user experience karena limitasi request sehingga user merasa aplikasi tidak responsif, cepat


---

## Kesimpulan Kelompok

Berdasarkan gejala yang dialami oleh FoodGo, kami menemukan kegagalan sistem yang berasal dari 3 pitfall akibat asumsi yang keliru, seperti jaringan yang selalu andal (network is reliable), latensi yang mendekati nol (latency is zero), dan bandwith yang tidak terbatas (bandwith is infinite). Asumsi ini mengakibatkan terjadinya deadlock dan berujung terjadinya crash pada aplikasi karena banyaknya request saat jam makan siang dan tidak diaturnya waktu tunggu per modul.

Untuk mengatasi 3 pitfall tersebut, kami menyarankan FoodGo menggunakan kombinasi arsitektur SOA untuk membagi batas domain antar modul, MOM (Message-Oriented Middleware) sebagai media komunikasi antar modul, dilengkapi dengan pagination untuk mencegah bottleneck akibat lonjakan lalu lintas data, serta dipadukan mekanisme pemisahan jalur sehingga ketika terjadinya lonjakan beban di salah satu modul tidak perlu dilakukannya reset secara manual.

Dengan menerapkan kombinasi arsitektur tersebut, FoodGo akan menerima trade-off berupa peningkatan kompleksitas serta pembengkakan biaya operasional. Meski demikian, kombinasi arsitektur tersebut dapat membantu FoodGo untuk mengatasi gejala yang ditimbulkan akibat kegagalan sistem, sehingga trade-off yang didapat akan sesuai dengan stabilitas sistem yang diperoleh.