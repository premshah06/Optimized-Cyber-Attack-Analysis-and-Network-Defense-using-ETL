#!/bin/bash

# Step 1: Run Zookeeper container
echo "Starting Zookeeper container..."
docker run --name my-zookeeper -d zookeeper

# Step 2: Wait for Zookeeper to fully start
echo "Waiting for Zookeeper to start..."
sleep 10

# Step 3: Run Kafka container linked to Zookeeper
echo "Starting Kafka container linked to Zookeeper..."
docker run --name my-kafka --link my-zookeeper -d -p 9092:9092 kafka

# Step 4: Verify if both containers are running
echo "Verifying if containers are running..."
docker ps

echo "Zookeeper and Kafka containers are now running!"
