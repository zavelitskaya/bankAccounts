#!/bin/bash
echo "=== Setting up MinIO ==="
docker volume create mc-config
sleep 15
docker run --rm -it -v mc-config:/root/.mc --network minio-docker_default minio/mc:latest \
  alias set myminio http://minio:9000 admin admin123456
docker run --rm -it -v mc-config:/root/.mc --network minio-docker_default minio/mc:latest \
  mb myminio/public-bucket
docker run --rm -it -v mc-config:/root/.mc --network minio-docker_default minio/mc:latest \
  anonymous set download myminio/public-bucket
echo "This is a public test file!" > test-public.txt
docker run --rm -it -v mc-config:/root/.mc --network minio-docker_default -v $(pwd):/data minio/mc:latest \
  cp /data/test-public.txt myminio/public-bucket/
echo "=== Setup Complete ==="
echo "MinIO Console: http://localhost:9001"
echo "Public file URL: http://localhost:9000/public-bucket/test-public.txt"