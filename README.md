# RAG Assistant
---
An end-to-end Retrieval-Augmented Generation (RAG) system built from scratch.

This project focuses on building a practical and production-oriented RAG pipeline, including document ingestion, text preprocessing, chunking, embedding generation, vector storage, semantic retrieval, and LLM-based answer generation.

## Project Goals

- Build an end-to-end RAG system from scratch
- Document every setup and development step
- Store and search document embeddings using Qdrant
- Experiment with different chunking and retrieval strategies
- Evaluate retrieval quality and generated answers
- Create a clean and reproducible project structure
- Prepare a portfolio-ready AI/ML engineering project

## Planned Features

- [ ] Project initialization
- [ ] Environment and dependency setup
- [ ] Document loading
- [ ] Text cleaning and preprocessing
- [ ] Document chunking
- [ ] Embedding generation
- [ ] Qdrant collection creation
- [ ] Vector insertion
- [ ] Semantic search
- [ ] Metadata filtering
- [ ] Context construction
- [ ] LLM-based answer generation
- [ ] Retrieval evaluation
- [ ] Answer evaluation
- [ ] FastAPI service
- [ ] Dockerized application
- [ ] Tests
- [ ] Monitoring and logging

## System Architecture

The initial RAG pipeline will follow this workflow:
```
Documents
   |
   v
Document Loading
   |
   v
Text Cleaning and Chunking
   |
   v
Embedding Generation
   |
   v
Qdrant Vector Database
   |
   v
User Query
   |
   v
Query Embedding
   |
   v
Semantic Retrieval
   |
   v
Context Construction
   |
   v
LLM Answer Generation

```

## Project Structure

```
rag-system-mvp/
├── app/
│   ├── api/
│   ├── config/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   └── main.py
├── configs/
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── docs/
│   ├── setup/
│   ├── architecture/
│   └── experiments/
├── notebooks/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── setup.py
├── requirements.txt
└── README.md
```

