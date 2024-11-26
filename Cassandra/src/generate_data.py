from kafka import KafkaProducer
import pandas as pd
import json
import time
import zlib  # Import compression library

# Load CICIDS dataset
cicids_data = pd.read_csv('/Users/mayankkapadia/Desktop/synthetic_network_traffic_v1.csv')

# Kafka Producer with batching and compression (zlib)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: zlib.compress(json.dumps(x).encode('utf-8')),  # Compress data before sending
    batch_size=65536,  # 64 KB
    linger_ms=5,  # 5 ms
    compression_type='gzip'  # Optional: Use built-in Kafka compression (gzip/snappy/lz4)
)

# Send each row to Kafka
for _, row in cicids_data.iterrows():
    data = row.to_dict()
    producer.send('cicids_traffic_1', value=data)  # Ensure proper partitioning
    print(f"Loaded {_} Successfully.....")
producer.flush()
