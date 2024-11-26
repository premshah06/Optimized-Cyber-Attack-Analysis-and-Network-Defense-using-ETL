import random
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

faker= Faker()

def generate_network_traffic_data(num_records):
    data = []
    attack_types = ['BENIGN','FTP-Patator','SSH-Patator','DDoS','PortScan','Infiltration','DoS slowloris'
                    ,'DoS Slowhttptest','DoS Hulk','DoS GoldenEye','Heartbleed']
    protocols = ['TCP', 'UDP', 'Reserved']
    start_date=datetime(2024,11,16)
    source_ip_list = [faker.ipv4() for _ in range(100000)]
    destination_ip_list=[faker.ipv4() for _ in range(100000)]
    for x in range(num_records):
        timestamp=start_date+timedelta(seconds=x)

        source_ip=random.choice(source_ip_list)
        destination_ip=random.choice(destination_ip_list)

        source_port = random.randint(1024, 65535)
        destination_port = random.randint(1024, 65535)

        protocol=random.choice(protocols)

        Average_Packet_Size=random.randint(0,4000)

        packet_size = random.randint(40, 1500)
        syn_flags = random.randint(0, 1)
        ack_flags = random.randint(0, 1)
        psh_flags = random.randint(0, 1)
        fin_flags = random.randint(0, 1)

        attack_label=random.choice(attack_types)

        data.append([source_ip, destination_ip, source_port, destination_port, protocol, timestamp.strftime("%Y-%m-%d %H:%M:%S"), packet_size, syn_flags, ack_flags, psh_flags, fin_flags, attack_label])
        print(f"Data {x} appended successfully!!!")
    
    columns=[source_ip, destination_ip, source_port, destination_port, protocol, timestamp, packet_size, syn_flags, ack_flags, psh_flags, fin_flags, attack_label]
    df = pd.DataFrame(data, columns=columns)

    return df

number_of_records=int(input("Enter how many records want to simulate for real time processing:"))
synthetic_data=generate_network_traffic_data(number_of_records) 

print("Data Simulation Done!!")

synthetic_data.to_csv('synthetic_network_traffic_v2.csv', index=False,header=[
    'source_ip', 'destination_ip', 'source_port', 'destination_port', 
    'protocol', 'timestamp', 'packet_size', 'syn_flags', 'ack_flags', 
    'psh_flags', 'fin_flags', 'attack_label'
])




