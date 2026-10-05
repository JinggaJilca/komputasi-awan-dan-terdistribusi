"""
Tugas 4 - Jalur B: Consumer (simulasi modul Kurir/Notifikasi)
Jalankan file ini SEBELUM publisher.py untuk uji normal, atau SESUDAHNYA
untuk membuktikan pesan tetap tersimpan di antrean (asynchronous decoupling).
"""

import time
import pika
import json

QUEUE_NAME = "pembayaran_berhasil"


def callback(ch, method, properties, body):
    waktu_diterima = time.time()
    pesan = json.loads(body)
    # TODO 1: proses pesan (misalnya cetak "Kurir menerima notifikasi
    # pembayaran untuk {user_id} sejumlah {jumlah}").
    waktu_dibuat = pesan.get("timestamp", waktu_diterima)
    latensi_antrean = waktu_diterima - waktu_dibuat

    print(f"[CONSUMER] Kurir menerima notifikasi pembayaran untuk {pesan['user_id']} sejumlah {pesan['jumlah']}")

    waktu_selesai = time.time()
    total_waktu_selesai = waktu_selesai - waktu_dibuat

    print(f"---- Latensi di Antrean : {latensi_antrean:.6f} detik")
    print(f"---- Total End-to-End  : {total_waktu_selesai:.6f} detik\n")


    # TODO 2: kirim acknowledgement ke RabbitMQ (ch.basic_ack) supaya
    # pesan dihapus dari antrean setelah berhasil diproses.
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # TODO 3: buat koneksi & channel seperti di publisher.py, deklarasikan
    # queue yang SAMA (durable=True), lalu daftarkan `callback` dengan
    # channel.basic_consume(...).
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("Menunggu event dari antrean 'pembayaran_berhasil'... (Ctrl+C untuk berhenti)")

    # TODO 4: panggil channel.start_consuming()
    channel.start_consuming()


if __name__ == "__main__":
    main()
