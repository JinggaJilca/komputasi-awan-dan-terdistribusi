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


## Analisis Tertulis

Pada tugas 1, FoodGo terkena masalah coupling (ketergantungan) karena seluruh modul digabungkan menjadi 1 program. Penerapan gaya arsitektur SOA (Service Oriented Architecture) yang dikombinasikan dengan MOM (Message Oriented Middleware) mengatasi masalah tersebut dengan melakukan pemisahan layanan (decoupling). Jika sebelumnya modul pesanan, pembayaran, katalog resto, pelanggan, dan kurir dugabung dalam satu proses server, maka dengan gaya arsitektur SOA ini, setiap modul diubah menjadi layanan mandiri (independent services) yang berjalan di proses atau server terpisah. Dengan begitu, risiko downtime total dapat dihilangkan.

Sedangkan, pengombinasian dengan MOM mengurangi ketergantungan waktu. Pada kondisi sebelumnya, modul pesanan memanggil modul lain secara langsung dan menunggu respons secara linier (blocking). Jika modul pembayaran melambat, seluruh proses tertahan dan memicu timeout serta crash pada server Utama. Dengan menggunakan MOM (seperti RabbitMQ atau kafka) yang dikombinasikan dengan SOA, komunikasi diubah menjadi asinkron. Jadi, masing-masing modul tidak lagi terikat secara langsung dengan modul lainnya. Setiap modul (seperti resto dan kurir) akan mengambil antrean sesuai kapasitas masing-masing. Hal ini memastikan gangguan di salah satu modul tidak memengaruhi dan melumpuhkan layanan lainnya.