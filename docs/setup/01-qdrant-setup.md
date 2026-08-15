# Qdrant Local Setup

## Objective

Run Qdrant locally as the vector database for the RAG MVP.

## Prerequisites

- Docker installed
- Docker daemon running
- Ports `6333` and `6334` available

## Docker Image
```
sudo docker pull qdrant/qdrant:latest
```

## Run Qdrant
```
sudo docker run -d   --name qdrant-local   --restart unless-stopped   -p 127.0.0.1:6333:6333   -p 127.0.0.1:6334:6334   -e QDRANT__TELEMETRY_DISABLED=true   -v qdrant_storage:/qdrant/storage   qdrant/qdrant
```
## Verification
```
sudo docker ps
curl http://localhost:6333/healthz
```

## Qdrant dashboard
```
curl http://localhost:6333/dashboard
```

