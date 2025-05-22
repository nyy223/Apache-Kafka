# spark-streaming/consumer_filter.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Inisialisasi Spark session
spark = SparkSession.builder.appName("PeringatanSensorGudang").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Skema masing-masing sensor
schema_suhu = StructType() \
    .add("gudang_id", StringType()) \
    .add("suhu", IntegerType())

schema_humi = StructType() \
    .add("gudang_id", StringType()) \
    .add("kelembaban", IntegerType())

# Fungsi parsing dan filter suhu
suhu_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-suhu-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema_suhu).alias("data")) \
    .select("data.*") \
    .filter(col("suhu") > 80)

# Fungsi parsing dan filter kelembaban
humi_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-kelembaban-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema_humi).alias("data")) \
    .select("data.*") \
    .filter(col("kelembaban") > 70)

# Fungsi output untuk suhu
def log_suhu_alert(df, epoch_id):
    if df.count() > 0:
        print(f"\n=== Batch {epoch_id} - SUHU ===")
        df.selectExpr("concat('Gudang ', gudang_id, ': Suhu ', suhu, '°C') as alert") \
            .toPandas()["alert"].apply(print)

# Fungsi output untuk kelembaban
def log_humi_alert(df, epoch_id):
    if df.count() > 0:
        print(f"\n=== Batch {epoch_id} - KELEMBABAN ===")
        df.selectExpr("concat('Gudang ', gudang_id, ': Kelembaban ', kelembaban, '%') as alert") \
            .toPandas()["alert"].apply(print)

# Streaming suhu
suhu_stream.writeStream \
    .foreachBatch(log_suhu_alert) \
    .outputMode("append") \
    .start()

# Streaming kelembaban
humi_stream.writeStream \
    .foreachBatch(log_humi_alert) \
    .outputMode("append") \
    .start()

# Menunggu semua stream
spark.streams.awaitAnyTermination()
