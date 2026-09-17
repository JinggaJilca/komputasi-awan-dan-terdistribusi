# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 2

| Nama | NIM | Kontribusi |
|---|---|---|
| Neista Arsha Javana | 103072400067 | [pitfall/bagian yang dikerjakan] |
| Nayyara Aurelia Putri | 103072400097 | [pitfall/bagian yang dikerjakan] |
| Jingga Jil Carissa | 103072400121 | Bandwidth is Infinite |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

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
