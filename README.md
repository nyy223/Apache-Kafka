# Problem Based Learning : Apache Kafka

| Nama  | NRP  |
|----------|----------|
| Nayla Raissa Azzahra  | 5027231054 |

## Latar Belakang Masalah
Sebuah perusahaan logistik mengelola beberapa gudang yang menyimpan barang-barang sensitif seperti makanan, obat-obatan, dan elektronik. Untuk menjaga kualitas penyimpanan, gudang dilengkapi dengan **sensor suhu** dan **sensor kelembaban** yang mengirimkan data setiap detik. Perusahaan ingin memantau kondisi gudang secara **real-time** untuk mencegah kerusakan barang akibat suhu terlalu tinggi atau kelembaban berlebih.

---
## Tujuan Pembelajaran
- Memahami alur kerja real-time data streaming menggunakan Apache Kafka dan PySpark.
- Menerapkan sistem pemantauan gudang berbasis sensor suhu dan kelembaban.
- Mempelajari filtering dan join stream untuk mendeteksi kondisi abnormal.
---

## Tools yang Digunakan
- Apache Kafka `3.9.0`
- PySpark `3.5.5`
- Kafka Python Library (`kafka-python`)
- Python `>=3.8`

---

## Langkah Instalasi & Setup
### 1. Install Dependencies
```bash
pip install kafka-python pyspark
```
### 2. Download & Setup Kafka
```bash
wget https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
tar -xzf kafka_2.13-3.9.0.tgz
cd kafka_2.13-3.9.0
```
### 3. Jalankan Zookeeper dan Kafka
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```
### 4. Buat Kafka Topics
```bash
bin/kafka-topics.sh --create --topic sensor-suhu-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

bin/kafka-topics.sh --create --topic sensor-kelembaban-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
---
## Jalankan proyek
### Kafka Producers
- producer_suhu.py: Mengirimkan data suhu secara real-time.
```bash
python producer_suhu.py
```

- producer_kelembaban.py: Mengirimkan data kelembaban secara real-time.
```bash
python producer_kelembaban.py
```

### Kafka Consumers (PySpark)
a. Filtering Stream (peringatan individual)
```bash
spark-submit \
  --master "local[*]" \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  consumer_filter.py
```

b. Join Stream (peringatan gabungan)
```bash
spark-submit \
  --master "local[*]" \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  consumer_join.py
```

---
## Format Data
### Producer Suhu (Kafka Topic: sensor-suhu-gudang)
<img width="532" alt="Screenshot 2025-05-22 at 07 56 56" src="https://github.com/user-attachments/assets/88e18f7e-0751-4523-ad12-43d5347711c4" />

### Producer Kelembaban (Kafka Topic: sensor-kelembaban-gudang)
<img width="572" alt="Screenshot 2025-05-22 at 07 57 35" src="https://github.com/user-attachments/assets/3913619a-02ef-49b5-8de9-edd10f00039d" />

---
## Output Konsumen
### Peringatan Individual
Jika nilai melebihi ambang batas:
- Suhu > 80°C
- Kelembaban > 70%
<img width="275" alt="Screenshot 2025-05-22 at 07 58 21" src="https://github.com/user-attachments/assets/5ac741cd-cfdb-435e-a0f0-4ff953a0a308" />

### Peringatan Gabungan
Join data suhu dan kelembaban berdasarkan gudang_id dalam window waktu (10 detik) dan tampilkan status:
<img width="559" alt="Screenshot 2025-05-22 at 07 59 16" src="https://github.com/user-attachments/assets/ddb67f33-91d4-4216-a981-7c8c0b067a70" />
---
## Kesimpulan
Melalui proyek ini, berhasil dibangun sistem monitoring gudang real-time menggunakan Apache Kafka dan PySpark. Sistem ini dapat mendeteksi secara cepat kondisi tidak normal berdasarkan ambang batas suhu dan kelembaban, serta menggabungkan data untuk peringatan gabungan antar sensor. Implementasi ini dapat dikembangkan lebih lanjut untuk pengambilan keputusan otomatis.
