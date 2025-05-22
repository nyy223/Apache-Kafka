# spark-streaming/consumer_join_nayla.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, expr
from pyspark.sql.types import StructType, StringType, IntegerType

# 1. Buat SparkSession
spark = SparkSession.builder \
    .appName("GabungDataSensorGudang") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Skema data suhu dan kelembaban
skema_suhu = StructType() \
    .add("gudang_id", StringType()) \
    .add("suhu", IntegerType())

skema_kelembaban = StructType() \
    .add("gudang_id", StringType()) \
    .add("kelembaban", IntegerType())

# 3. Baca stream Kafka untuk suhu
stream_suhu = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-suhu-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) AS data_json", "timestamp") \
    .select(from_json(col("data_json"), skema_suhu).alias("parsed"), "timestamp") \
    .select("parsed.*", "timestamp")

# 4. Baca stream Kafka untuk kelembaban
stream_kelembaban = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-kelembaban-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) AS data_json", "timestamp") \
    .select(from_json(col("data_json"), skema_kelembaban).alias("parsed"), "timestamp") \
    .select("parsed.*", "timestamp")

# 5. Tambahkan watermark (20 detik) untuk antisipasi data lambat
suhu_dengan_watermark = stream_suhu.withWatermark("timestamp", "20 seconds")
humi_dengan_watermark = stream_kelembaban.withWatermark("timestamp", "20 seconds")

# 6. Join berdasarkan gudang_id dan timestamp (window ±10 detik)
gabungan = suhu_dengan_watermark.alias("s") \
    .join(
        humi_dengan_watermark.alias("h"),
        (col("s.gudang_id") == col("h.gudang_id")) &
        (col("h.timestamp").between(
            col("s.timestamp") - expr("INTERVAL 10 SECONDS"),
            col("s.timestamp") + expr("INTERVAL 10 SECONDS"))
        )
    )

# 7. Tambahkan status kondisi gudang
hasil = gabungan.withColumn(
    "status_kondisi",
    expr("""
        CASE
            WHEN s.suhu > 80 AND h.kelembaban > 70 THEN 'Kondisi KRITIS: Suhu & Kelembaban Tinggi'
            WHEN s.suhu > 80 THEN 'Peringatan: Suhu Tinggi'
            WHEN h.kelembaban > 70 THEN 'Peringatan: Kelembaban Tinggi'
            ELSE 'Kondisi Normal'
        END
    """)
).select(
    col("s.gudang_id").alias("gudang_id"),
    col("s.suhu").alias("suhu (°C)"),
    col("h.kelembaban").alias("kelembaban (%)"),
    col("status_kondisi")
)

# 8. Tampilkan hasil ke console
hasil.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .option("checkpointLocation", "/tmp/checkpoint_join_nayla") \
    .start() \
    .awaitTermination()
