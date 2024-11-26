echo "Starting Cassandra container..."
docker run --name my-cassandra -d cassandra

echo "Verifying if containers are running..."
docker ps
