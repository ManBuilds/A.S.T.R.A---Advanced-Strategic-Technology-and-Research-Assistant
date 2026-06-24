# Learning Data

This folder stores your personal knowledge base documents that A.S.T.R.A uses for enhanced responses.

## Adding Learning Data

Place any `.txt` files in this folder. On server startup, A.S.T.R.A will:
1. Read all text files
2. Convert them to embeddings using Sentence Transformers
3. Store them in the vector store for retrieval

## Example Content

You can add text files with:
- Personal notes and research
- Company information
- Technical documentation
- Domain expertise
- Reference materials

## Example File: my_knowledge.txt
```
My name is John Doe.
I work as a Senior Software Engineer at TechCorp.
I have expertise in Python, FastAPI, and Machine Learning.
I'm particularly interested in LLMs and vector databases.
My favorite AI models are Llama and Groq's offerings.
```

## Privacy Note
- Your learning data is stored locally only
- These files are NEVER committed to GitHub (see .gitignore)
- Your personal documents remain completely private
