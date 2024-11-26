import json
import threading
import logging
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from uuid import uuid1
from datetime import datetime
import zlib  # For decompression
import time  # For timeout handling

# Constants
NUM_PARTITIONS = 8  # Match Kafka topic partitions
BATCH_SIZE = 5  # Number of records to batch insert
MAX_POLL_RECORDS = 1000  # Consumer poll size
CASSANDRA_NODES = ['127.0.0.1']  # Cassandra cluster IPs
TIMEOUT = 60  # Maximum time to run consumer before stopping (in seconds)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Shutdown flag for threads
shutdown_event = threading.Event()

# Kafka Consumer setup
def create_consumer(group_id):
    return KafkaConsumer(
        'cicids_traffic_1',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(zlib.decompress(x).decode('utf-8')),  # Decompress data after receiving
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        max_poll_records=MAX_POLL_RECORDS,
        group_id=group_id
    )

# Cassandra connection setup
def create_cassandra_session():
    cluster = Cluster(CASSANDRA_NODES)
    session = cluster.connect()

    # Ensure keyspace exists
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS network_data
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };
    """)

    session.set_keyspace("network_data")

    # Ensure table exists
    session.execute("""
        CREATE TABLE IF NOT EXISTS network_traffic_v1 (
            id UUID,
            source_ip TEXT,
            destination_ip TEXT,
            source_port INT,
            destination_port INT,
            protocol TEXT,
            syn_flags INT, 
            ack_flags INT,
            psh_flags INT,
            fin_flags INT,
            time_stamp TIMESTAMP,
            packet_size INT,
            attack_label TEXT ,
            PRIMARY KEY (source_ip, time_stamp)
) WITH CLUSTERING ORDER BY (time_stamp DESC);
    """)

    return session

def insert_to_cassandra(session, data_batch):
    """
    Insert a batch of data into Cassandra with deduplication logic.
    
    Parameters:
        session: Cassandra session object
        data_batch: List of records to be inserted
    """
    prepared_insert = session.prepare("""
        INSERT INTO network_traffic_v1 (
            id, source_ip, destination_ip, source_port, destination_port,
            protocol,syn_flags, ack_flags, psh_flags, fin_flags,time_stamp, packet_size, attack_label
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)
    """)

    for data in data_batch:
        try:
            # Parse timestamp
            try:
                time_stamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
            except ValueError:
                logger.error(f"Invalid timestamp format: {data['timestamp']}. Skipping record.")
                continue

            # Insert record into Cassandra
            session.execute(prepared_insert, (
                uuid1(), data['source_ip'], data['destination_ip'], data['source_port'],
                data['destination_port'], data['protocol'],data['syn_flags'],data['ack_flags'],data['psh_flags'],data['fin_flags'],time_stamp,
                data['packet_size'], data['attack_label']
            ))
        except Exception as e:
            logger.error(f"Error processing record: {e}")


# Consumer thread function with timeout and offset commit
def consume_and_process(consumer, session, timeout=60):
    start_time = time.time()  # Track start time
    message_batch = []
    try:
        for message in consumer:
            # Check for timeout
            if time.time() - start_time > timeout or shutdown_event.is_set():
                logger.info("Timeout exceeded or shutdown event detected. Stopping consumer.")
                break

            data = message.value
            logger.info(f"Processing message with offset: {message.offset}")
            message_batch.append(data)

            if len(message_batch) >= BATCH_SIZE:
                insert_to_cassandra(session, message_batch)
                consumer.commit()  # Commit offsets after successful batch insert
                message_batch.clear()

        # Process remaining messages before exiting
        if message_batch:
            insert_to_cassandra(session, message_batch)
            consumer.commit()

    finally:
        consumer.close()
        logger.info("Consumer thread shutting down.")

# Main function
if __name__ == "__main__":
    session = create_cassandra_session()
    threads = []

    for i in range(NUM_PARTITIONS):
        consumer = create_consumer(group_id=f'consumer-group-{i}')
        thread = threading.Thread(target=consume_and_process, args=(consumer, session, TIMEOUT))
        threads.append(thread)
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        shutdown_event.set()
        logger.info("Graceful shutdown initiated.")
