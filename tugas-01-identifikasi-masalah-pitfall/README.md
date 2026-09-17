# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 2

| Nama | NIM | Kontribusi |
|---|---|---|
| Neista Arsha Javana | 103072400067 | Latency is Zero |
| Nayyara Aurelia Putri | 103072400097 | [pitfall/bagian yang dikerjakan] |
| Jingga Jil Carissa | 103072400121 | Bandwidth is Infinite |

## Pitfall 1: Latency is Zero — ditulis oleh Neista Arsha Javana]

**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout." dan "... tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu."


**Kenapa ini keliru**: Asumsi bahwa latency is zero merupakan analisa yang keliru, karena komunikasi melalui jaringan tidak dapat terjadi secara instan dan selalu membutuhkan waktu. Asumsi ini dapat memicu terjadinya kelumpuhan pada aplikasi karena proses yang terhambat. Tidak adanya timeout menyebabkan thread server mengalami blocking karena menunggu balasan dari modul lain tanpa batas waktu (tidak adanya timeout). Penumpukan thread ini menyebabkan aplikasi sangat lambat, antrian pengguna bertumpuk, dan sistem mengalami crash.an]

**Dampak ke FoodGo**: Ketiadaan timeout membuat thread di modul pesanan terhenti (mengalami blocking) karena terus menunggu respon dari modul pembayaran dengan waktu tanpa batas. Saat jam makan siang, penumpukkan thread yang menggantung ini dapat menghabiskan kapasitas pemrosesan server, sehingga aplikasi berjalan dengan sangat lambat. pesanan baru bertumpuk, dan proses server akhirnya mengalami crash.  

**Solusi desain awal:**
. 
1. 
Memasang timeout (batas waktu) sehingga saat tidak ada respons dalam kurun waktu tertentu, sistem akan langsung memutus koneksi secara sepihak dan membebaskan thread serve
2.Jika modul pembayaran gagal berkali-kali, maka pemanggilan berikutnya akan ditolak dengan cepat tanpa membebani server.r. 
1

**Trade-off:** Pengguna yang memesan saat sisem pembayaran sedang bermasalah akan langsung ditolak.  ni]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: Bandwidth is Infinite — ditulis oleh Jingga Jil Carissa

**Bukti di skenario:** "Server backend kadang crash total dan perlu di-restart manual"

**Kenapa ini keliru:**  Asumsi bahwa bandwidth tidak terbatas (bandwidth is infinite) berisiko memicu kemacetan jaringan (network congestion) saat terjadi lonjakan pengguna. Batas bandwidth yang terlampaui membuat paket data tertahan di antrean memori. Penumpukan koneksi yang tertahan ini memaksa server mengalokasikan RAM dan thread secara berlebihan hingga memicu kondisi Out of Memory (OOM) dan crash pada sistem

**Dampak ke FoodGo:** Pada kasus FoodGo, lonjakan pengguna secara tiba-tiba (traffic spike) terjadi akibat diskon promo di jam makan siang. Ketika puluhan ribu pengguna mengakses aplikasi secara bersamaan, terjadi beberapa rentetan masalah teknis:

1. Pengiriman Data Berlebih: Server dipaksa mengirimkan seluruh data berat seperti detail pesanan, gambar menu beresolusi tinggi, hingga lokasi kurir melalui pemanggilan API (Application Programming Interface, yaitu antarmuka penghubung antar-aplikasi) tanpa adanya pembatasan atau penyaringan data.

2. Penyumbatan Jalur (Bottleneck): Lonjakan lalu lintas data ini melampaui batas maksimal bandwidth. Terjadilah penumpukan antrean permintaan (request) yang menyebabkan penurunan performa secara drastis (lag).

3. Kehabisan Sumber Daya (Resource Exhaustion): Penumpukan request yang tidak kunjung terproses ini memaksa server menampung data di dalam memori sementara. Akibatnya, penggunaan RAM (Random Access Memory) dan pemrosesan CPU (Central Processing Unit) mencapai kapasitas maksimal 100%.

4. Penghentian Paksa oleh Sistem Operasi (OOM Killer): Karena memori habis total (Out of Memory), Sistem Operasi (OS) server secara otomatis menghentikan (kill) proses backend secara paksa untuk menyelamatkan mesin dasar. Akibatnya, aplikasi crash total dan tidak bisa pulih sendiri tanpa tindakan restart manual.
5. Skenarion terparah selain masalah kehabisan memori, lonjakan request yang sangat cepat di jam sibuk memicu terjadinya deadlock (kondisi kebuntuan di mana dua atau lebih proses saling mengunci dan berhenti permanen karena saling menunggu).

**Solusi desain awal:** 

1. Pagination dan Optimasi Payload API untuk mengurangi ukuran data dengan membatasi 1 halaman hanya 10 - 20 item 
2. Kompresi file berupa CDN (Content Delivery Network) agar lebih kecil untuk foto menu, logo toko
3. Pembatasan Lalu Lintas membatasi jumlah pemintaan misalnya 10 request/detik

**Trade-off:**

Penggunaan CDN dan API Gateaway membuat biaya operasional membengkak
Melakukan pembatasan lalu lintas juga menyebabkan menurunnya user experience karena limitasi request sehingga user merasa aplikasi tidak responsif, cepat


---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
