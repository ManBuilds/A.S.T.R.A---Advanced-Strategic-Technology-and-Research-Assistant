# Vector Store

This folder stores the FAISS vector database and embeddings.

## Contents

- `index.faiss` - The FAISS vector index file containing embeddings
- `index.pkl` - Pickle file with metadata and document mappings

## How It Works

1. When the server starts, it reads all text files from `learning_data/`
2. Each document is converted to embeddings using Sentence Transformers
3. Embeddings are stored in the FAISS index for fast retrieval
4. When you chat, relevant documents are retrieved and added as context

## Rebuilding the Vector Store

If you want to rebuild the vector store from scratch:

1. Stop the server
2. Delete `index.faiss` and `index.pkl`
3. Restart the server

The vector store will be automatically recreated from your learning data files.

## Privacy Note
- Vector embeddings are computed locally
- These files are NEVER committed to GitHub (see .gitignore)
- Your data remains completely private on your machine
