# Problem Based Learning : Apache Kafka

| Nama  | NRP  |
|----------|----------|
| Nayla Raissa Azzahra  | 5027231054 |

## Latar Belakang Masalah
Sebuah perusahaan logistik mengelola beberapa gudang yang menyimpan barang-barang sensitif seperti makanan, obat-obatan, dan elektronik. Untuk menjaga kualitas penyimpanan, gudang dilengkapi dengan **sensor suhu** dan **sensor kelembaban** yang mengirimkan data setiap detik. Perusahaan ingin memantau kondisi gudang secara **real-time** untuk mencegah kerusakan barang akibat suhu terlalu tinggi atau kelembaban berlebih.

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
