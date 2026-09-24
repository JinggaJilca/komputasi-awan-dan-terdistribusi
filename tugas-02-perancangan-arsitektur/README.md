# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo









**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

**Kelompok:** Kelompok 2

| Nama | NIM | Kontribusi |
|---|---|---|
| Neista Arsha Javana | 103072400067 | Latency is Zero |
| Nayyara Aurelia Putri | 103072400097 | Network is Reliable |
| Jingga Jil Carissa | 103072400121 | Bandwidth is Infinite |

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok

1. Pilih **satu** gaya arsitektur utama: **Service-Oriented Architecture (SOA)** atau **Publish-Subscribe**. Boleh dikombinasikan (mis. SOA untuk service inti + Pub-Sub untuk notifikasi), tapi harus dijustifikasi kenapa kombinasi ini yang dipilih.
2. Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
3. Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan **jenis komunikasinya** (sinkron/asinkron, request-response/event).
4. Analisis tertulis: kenapa gaya ini mengatasi masalah *coupling* dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).





# Hasil Diskusi

## Usulan Arsitektur  

Kombinasi **Service-Oriented Architecture (SOA)** dan **Message-Oriented Middleware (MOM)** merupakan arsitektur hybrid yang kami pilih untuk mengatasi permasalahan pada sistem FoodGo. Arsitektur ini dinilai jauh lebih efisien dibandingkan menerapkan arsitektur SOA murni maupun Publish-Subscribe murni secara terpisah.

Melalui pendekatan ini:
* **SOA** berperan memisahkan fungsi aplikasi menjadi layanan-layanan (*services*) mandiri di mana setiap layanan mewakili fungsi bisnis spesifik.
* **MOM** bertindak sebagai perantara komunikasi asinkron yang memutus pemanggilan langsung (*direct synchronous call*) antar-layanan.

Penerapan arsitektur hybrid ini sangat efisien saat lonjakan trafik (*traffic spike*) terjadi. Sebagai contoh, pada alur pemesanan, **Modul Pesanan** tidak perlu menunggu pemrosesan di **Modul Pembayaran** selesai secara sinkron. Pesan transaksi langsung dimasukkan ke dalam antrean MOM, sementara sistem secara instan memberikan respons balasan (*acknowledgment*) ke pengguna. MOM bertindak sebagai peredam kejut (*rate flattening*) yang menampung antrean transaksi tanpa memicu pemblokiran *thread* (*thread blocking*) pada server utama.

---

### Perbandingan Penanganan Lonjakan Trafik

Keunggulan kombinasi **SOA + MOM** dalam menangani lonjakan trafik tinggi terlihat jelas jika dibandingkan dengan arsitektur lain:

* **SOA Murni (Synchronous):** Gagal akibat akumulasi *blocking thread* yang memicu *Out of Memory* (OOM) dan *crash* pada server.
* **Publish-Subscribe Murni:** Mampu mengamankan pemrosesan transaksi, tetapi kurang efisien dan memberikan *overhead* tinggi untuk aktivitas yang bersifat *read-heavy*.

> **Kesimpulan:**  
> Kombinasi **SOA + MOM (Hybrid)** paling efisien karena memisahkan lalu lintas pemanggilan data (*read* via SOA + Caching) dan pemrosesan transaksi (*write* via MOM Async Queue). Hasilnya, sistem FoodGo tetap responsif bagi pengguna sekaligus tahan terhadap risiko *crash* saat promo jam makan siang.

## Alur Skenario End-To-End FoodGo

0. Pencarian Menu
- Komponen yang berkomunikasi: Pelanggan -> Modul Katalog (REST).
- Jenis komunikasi: Sinkron (Request-Response).
- Pejelasan: Sebelum melakukan transaksi, pelanggan membuka aplikasi untuk melihat daftar menu. Pelanggan mengirimkan HTTP GET Request ke modul katalog, lalu sistem membalas (response) dengan data menu secara real-time.

1. Pembuatan Pesanan
- Komponen yang berkomunikasi: Pelanggan -> Modul Pesanan (SOA).
- Jenis komunikasi: Sinkron (Request-Response).
- Penjelasan: Saat pelanggan memilih menu di keranjang dan menekan tombol "Pesan", aplikasi mengirimkan HTTP POST Request ke modul pesanan. Komunikasi bersifat asinkron karena pelanggan membutuhkan kepastian secara real-time apakah pesanan mereka berhasil dicatat oleh sistem atau mengalami kendala (misalnya stok habis).

2. Pemrosesan Pembayaran
- Komponen yang berkomunikasi: Modul Pesanan -> Modul Pembayaran (SOA).
- Jenis komunikasi: Sinkron (Request-Response).
- Penjelasan: Setelah pesanan diverifikasi, modul pesanan secara langsung memanggil modul pembayaran secara real-time untuk memproses saldo pelanggan. Proses ini wajib bersifat sinkron agar status "pembayaran berhasil atau gagal" langsung diketahui saat itu juga.

3. Pengiriman Event ke Message Broker
- Komponen yang berkomunikasi: Modul Pembayaran -> Message Broker (MOM).
- Jenis komunikasi: Asinkron (Publish Event).
- Penjelasan: Setelah pembayaran berhasil, modul pembayaran tidak menghubungi modul resto dan modul notifikasi/kurir secara manual. Sebaliknya, modul pembayaran cukup mengirimkan pesan sukses ke message broker (MOM). Dengan cara ini, modul pembayaran tidak perlu menunggu modul resto dan modul notifikasi/kurir selesai.

4. Distribusi Tugas ke Resto dan Kurir
- Komponen yang berkomunikasi: Message Broker (MOM) -> Modul Resto dan Modul Notifikasi/Kurir.
- Jenis komunikasi: Asinkron (Pub-Sub).
- Penjelasan: MOM berperan sebagai perantara untuk menyebarkan (broadcast) salinan pesan event secara pararel kepada modul resto dan modul notifikasi/kurir. Ketika menerima pesan tersebut, modul resto dapat menyiapkan pesanan, sedangkan modul notifikasi/kurir akan memproses pencarian serta melakukan penugasan kurir untuk menjemput pesanan.

## Analisis Tertulis

Pada tugas 1, FoodGo terkena masalah coupling (ketergantungan) karena seluruh modul digabungkan menjadi 1 program. Penerapan gaya arsitektur SOA (Service Oriented Architecture) yang dikombinasikan dengan MOM (Message Oriented Middleware) mengatasi masalah tersebut dengan melakukan pemisahan layanan (decoupling). Jika sebelumnya modul pesanan, pembayaran, katalog resto, pelanggan, dan kurir digabung dalam satu proses server, maka dengan gaya arsitektur SOA ini, setiap modul diubah menjadi layanan mandiri (independent services) yang berjalan di proses atau server terpisah. Dengan begitu, risiko downtime total dapat dihilangkan.

Sedangkan, pengombinasian dengan MOM mengurangi ketergantungan waktu. Pada kondisi sebelumnya, modul pesanan memanggil modul lain secara langsung dan menunggu respons secara linier (blocking). Jika modul pembayaran melambat, seluruh proses tertahan dan memicu timeout serta crash pada server Utama. Dengan menggunakan MOM (seperti RabbitMQ atau kafka) yang dikombinasikan dengan SOA, komunikasi diubah menjadi asinkron. Jadi, masing-masing modul tidak lagi terikat secara langsung dengan modul lainnya. Setiap modul (seperti resto dan kurir) akan mengambil antrean sesuai kapasitas masing-masing. Hal ini memastikan gangguan di salah satu modul tidak memengaruhi dan melumpuhkan layanan lainnya.

**Trade Off**

Pada sistem monolitik, melacak sebuah error lebih mudah karena semua proses berjalan secara berurutan dalam satu log server. Sedangkan, dengan komunikasi asinkron via MOM, alur program menjadi tidak linear. Jika pesanan gagal, tim developer harus melacak pesan tersebut melalui beberapa layanan dan antrean broker, yang membutuhkan alat tambahan (seperti Centralized Logging atau Correlation ID). Pesan juga berisiko mengalami duplikasi atau tertahan di antrean, sehingga harus ditambahkan logika baru (seperti idempotency) untuk mengatasi pemrosesan ganda.

Selain itu, infrastruktur dan biaya operasional harus ditambah. Jika sebelumnya FoodGo hanya perlu memelihara satu server monolitik, sekarang tim harus mengelola beberapa server layanan terpisah, ditambah infrastruktur pengelola antrean seperti RabbitMQ atau Apache Kafka. Jika salah satu komponen message broker mengalami gangguan, seluruh komunikasi asinkron di FoodGo bisa lumpuh, sehingga membutuhkan pengawasan (monitoring) yang lebih ketat.
