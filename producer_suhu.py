from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

gudangs = ["G1", "G2", "G3"]

while True:
    for gudang in gudangs:
        data = {
            "gudang_id": gudang,
            "suhu": random.randint(75, 90)
        }
        producer.send('sensor-suhu-gudang', value=data)
        print(f"[Suhu] Data terkirim: {data}")
    time.sleep(1)