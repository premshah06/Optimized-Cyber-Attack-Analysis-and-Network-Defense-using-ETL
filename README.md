# Optimized-Cyber-Attack-Analysis-and-Network-Defense-using-ETL

Welcome to the Cyber Attack Analysis and Network Defense project! This project uses advanced data warehousing and real-time data processing to analyze cyber threats using Amazon Redshift, Neo4j, Cassandra, and Kafka.

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Technologies Used](#technologies-used)
- [Data Model](#data-model)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Results](#results)
- [Contributors](#contributors)

---

## **Overview**

This project leverages Amazon Redshift, Neo4j, and Cassandra with Kafka streaming to create a scalable, real-time intrusion detection system. Utilizing the CICIDS 2017 dataset, the system analyzes network traffic data, identifies patterns, and detects anomalies efficiently.

## **Features**
- **Optimized ETL Pipelines**: High-speed data extraction, transformation, and loading processes with Amazon Redshift and Neo4j using Apache NiFi.
- **Advanced Data Modeling**: Implementation of star and snowflake schemas in Redshift to optimize query performance and enable large-scale data analytics.
- **Real-Time Data Processing**: Real-time data streaming and ingestion using Kafka and Cassandra, enabling dynamic anomaly detection and immediate response capabilities.

## **Project Architecture**
The architecture includes:
1. **Data Ingestion**: Data loaded from CSV files in Amazon S3.
2. **Data Warehousing**: Data processed in Amazon Redshift using a star schema.
3. **Real-Time Streaming**: Apache Kafka streams data to Cassandra for real-time insights.
4. **Graph Analysis**: Neo4j is used to model and query complex data relationships.

![Project Architecture Diagram](path/to/architecture_diagram.png)

## **Technologies Used**
- **Amazon Redshift**: Data warehousing for optimized query performance.
- **Neo4j**: Graph database for relational data analysis.
- **Apache Kafka**: Real-time data streaming.
- **Cassandra**: Distributed NoSQL database for low-latency storage.
- **Apache NiFi**: ETL processing and workflow automation.

## **Data Model**
The project uses a **star schema** with a fact table and multiple dimension tables to optimize query performance. Key dimensions include:
- **Source Dimension**: Source IP and port information.
- **Destination Dimension**: Destination IP and port information.
- **Protocol Dimension**: Protocol types (TCP, UDP).
- **Packet Dimension**: Packet forwarding and size metrics.
- **Date Dimension**: Timestamp details.

![Data Model Diagram](path/to/data_model_diagram.png)

## **Installation and Setup**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CyberAttack-DataWarehouse.git
   cd CyberAttack-DataWarehouse
   ```

2. **Environment Setup**:
   - Install necessary dependencies: Redshift, Neo4j, Kafka, Cassandra, and NiFi.
   - Set up Amazon S3 bucket for data storage.

3. **Load Data**:
   - Use the included scripts to load the CICIDS 2017 dataset to S3.
   - Use NiFi workflows to extract, transform, and load data into Redshift.

4. **Run the Project**:
   - Start Kafka and Cassandra for real-time data processing.
   - Run Redshift queries to analyze batch data.
   - Use Neo4j for graph-based analysis.

## **Usage**

- **Real-Time Analysis**:
   - Kafka streams data into Cassandra for immediate detection of anomalies.
   - Run Neo4j queries for network relationship insights.
- **Batch Analysis**:
   - Use Redshift to analyze historical data for patterns and trends in network traffic.

## **Results**
The project provides key insights:
1. **Attack Patterns**: Identifies patterns by source IP, destination IP, and protocol.
2. **Real-Time Detection**: Real-time streaming enables immediate detection of suspicious activity.
3. **Performance Benchmarking**: Comparison across Redshift, Neo4j, and Cassandra for efficiency, latency, and scalability.

---

## **License**
This project is licensed under the MIT License.

## **Acknowledgments**
- The CICIDS 2017 dataset was used as the primary data source for this project.
