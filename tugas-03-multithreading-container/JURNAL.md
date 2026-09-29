# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: kami mendapati hasil yang sama dengan percobaan dengan lock (processed_count = 100).
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): tanpa menggunakan time.sleep(), thread dapat menyelesaikan seluruh tugasnya sebelum python sempat melakukan melakukan context switch ke thread lain. Hal ini disebut False Impression of Safety, karena kodenya terlihat aman namun tidak thread-safe.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: hasil yang kami dapatkan adalah 100 (sesuai dengan NUM_ORDERS), dan selalu sama setiap dijalankan ulang. Hasilnya selalu benar karena lock menjadikan operasi processed_count += 1 menjadi kode yang hanya boleh dieksekusi oleh satu thread dalam satu waktu. Saat sebuah thread masuk ke critical section, thread lain yang ingin memasuki critical section yang sama akan menunggu (blocking) sampai lock dilepaskan oleh thread sebelumnya. Dengan begitu, proses membaca, menambah, dan menyimpan nilai processed_count selalu selesai secara utuh sebelum thread lain memulai prosesnya, sehingga tidak ada nilai yang tertimpa atau "hilang" seperti pada percobaan tanpa lock.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/Ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| :--- | :--- | :--- | :--- | :--- |
| 29 September 2026 | Gemini | *"Apakah tidak bisa menggunakan `processed_count += 1` saja untuk memicu race condition?"* | Menjelaskan bahwa `processed_count += 1` di Python terpecah menjadi 4 instruksi *bytecode*. Namun, pada beban kecil (100 pesanan), *context switch* jarang memotong instruksi tersebut karena eksekusi CPU yang sangat cepat dan batasan GIL. | Tetap mempertahankan modifikasi pemisahan operasi `temp = read` $\rightarrow$ `time.sleep` $\rightarrow$ `write` untuk memperlebar *window of vulnerability* agar *race condition* terbukti secara konsisten saat dijalankan tanpa *lock*. |
| 29 September 2026 | Gemini | *"Mengapa kode `temp = processed_count; time.sleep(0.0001); processed_count = temp + 1` memicu race condition?"* | Menjelaskan skenario *Lost Update* secara *step-by-step*: Thread B membaca nilai `processed_count` lama yang masih dipegang Thread A saat tertidur di baris `time.sleep`, sehingga salah satu update tertimpa. | Menuliskan komentar dokumentasi di dalam fungsi `process_order()` untuk memperjelas alasan penggunaan `time.sleep(0.0001)` sebagai pemicu *delay* bentrokan antar-thread pada bagian `==== START TANPA LOCK ====`. |
| 29 September 2026 | Gemini | *"Bantu saya memahami bagian `if i == NUM_WORKERS - 1: end_index = len(order_ids)` dan kenapa harus ditambah 1 untuk worker selain yang terakhir?"* | Menjelaskan bahwa `(i + 1)` mengalikan kelipatan jatah *worker* dari indeks 0, sedangkan `if i == NUM_WORKERS - 1` adalah *edge-case handling* untuk mengambil sisa data akibat pembagian bulat (`//`) agar tak ada pesanan tertinggal. | Mengimplementasikan logika *slicing* `order_ids[start_index:end_index]` pada perulangan `main()` di `TODO 3`, serta menambahkan penanganan khusus untuk *worker* ke-10 (`NUM_WORKERS - 1`) menggunakan `len(order_ids)`. |
| 29 September 2026 | Gemini | *"Dockerfile ... apakah bisa langsung dipakai?"* dan *"Cara running kembali ketika kode ada yang berubah?"* | Menjelaskan pengisian *placeholder* `Dockerfile` (`FROM python:3.11-slim`, `RUN pip install ...`, `CMD ["python3", "..."]`) dan menegaskan perlunya `docker build` ulang setiap kali ada perubahan kode sebelum `docker run`. | Melengkapi berkas `Dockerfile` proyek dan menyusun alur pengujian containerization di terminal dengan menjalankan perintah `docker build -t foodgo-order-sim .` lalu `docker run --rm foodgo-order-sim`. |

