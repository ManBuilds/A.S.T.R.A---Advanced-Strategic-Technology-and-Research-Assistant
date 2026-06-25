# A.S.T.R.A - Advanced Strategic Technology and Research Assistant

A personal AI assistant backend built with **FastAPI** that combines:
- **LLM Intelligence** - Powered by Groq's high-speed LLMs
- **Real-time Web Search** - Via Tavily API for up-to-date information
- **Vector Store Memory** - FAISS-based retrieval of past conversations and learning data
- **Session Management** - Persistent chat history across restarts

Perfect for building your own AI-powered applications with reliable, self-hosted infrastructure.

---

## Features

 **Dual Chat Modes**
- **General Chat**: Pure LLM responses enriched with your learning data and past conversations
- **Realtime Chat**: Performs live web search first, then combines results with context for current answers

 **Smart Memory System**
- Vector store retrieval from past chats and learning documents
- Persistent sessions that survive server restarts
- Automatic chat history management

 **High Performance**
- Groq's rapid inference for sub-second response times
- Async/await support for concurrent requests
- Built-in rate limit handling

 **Privacy-Focused**
- Single-user architecture (one server per person)
- All data stays on your machine
- API keys managed securely via `.env`

 **Easy Integration**
- RESTful API with clear endpoints
- Interactive API documentation at `/docs`
- Health monitoring for all services

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Web Framework** | FastAPI + Uvicorn |
| **LLM** | Groq (llama-3.3-70b-versatile) |
| **Web Search** | Tavily API |
| **Vector Store** | FAISS + Sentence Transformers |
| **Embeddings** | HuggingFace Sentence Transformers |
| **Vector DB** | LangChain |
| **Type Validation** | Pydantic |

---

## Installation

### Prerequisites
- Python 3.10+
- pip or conda
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ManBuilds/A.S.T.R.A---Advanced-Strategic-Technology-and-Research-Assistant.git
cd A.S.T.R.A/A.S.T.R.A
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### Get Your API Keys

1. **Groq API Key**
   - Go to [console.groq.com](https://console.groq.com)
   - Sign up and get your API key
   - You can generate multiple keys for rate limit rotation

2. **Tavily API Key**
   - Visit [tavily.com](https://tavily.com)
   - Create an account and get your search API key

### Setup Environment Variables

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_KEY_2=optional_backup_key
GROQ_API_KEY_3=optional_backup_key
GROQ_API_KEY_4=optional_backup_key
GROQ_MODEL=llama-3.3-70b-versatile

TAVILY_API_KEY=your_tavily_api_key_here

ASTRA_USER_TITLE=Your Name
ASSISTANT_NAME=A.S.T.R.A
```

⚠️ **Security Note**: Never commit `.env` to version control. It's automatically ignored by `.gitignore`.

---

## Running the Server

```bash
python run.py
```

The server will start at `http://localhost:8000`

### Access Points
- **API Endpoints**: http://localhost:8000
- **Interactive Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

---

## API Endpoints

### 1. Get API Info
```
GET /
```
Returns the API name and list of available endpoints.

### 2. Health Check
```
GET /health
```
Checks the status of all services (Groq, Tavily, Vector Store, etc.).

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "groq": "connected",
    "tavily": "connected",
    "vector_store": "ready"
  }
}
```

### 3. General Chat
```
POST /chat
```
Send a message for a pure LLM response, enhanced with your learning data and past chats.

**Request Body:**
```json
{
  "message": "What is artificial intelligence?",
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "Artificial intelligence refers to...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "model": "llama-3.3-70b-versatile",
  "context_used": 2
}
```

### 4. Real-time Chat with Web Search
```
POST /chat/realtime
```
Performs a live web search, then responds with current information.

**Request Body:**
```json
{
  "message": "What are the latest AI trends in 2024?",
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "Based on current web results...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "search_results": [
    {
      "title": "Recent AI Developments",
      "url": "https://example.com",
      "snippet": "..."
    }
  ]
}
```

### 5. Get Chat History
```
GET /chat/history/{session_id}
```
Retrieve all messages from a specific chat session.

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-06-24T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help?",
      "timestamp": "2024-06-24T10:30:05"
    }
  ]
}
```

---

## Project Structure

```
A.S.T.R.A/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application & routes
│   ├── models.py               # Pydantic request/response models
│   ├── services/
│   │   ├── groq_services.py    # Groq LLM integration
│   │   ├── chat_service.py     # Chat logic
│   │   ├── realtime_service.py # Web search + response
│   │   └── vector_store.py     # FAISS vector store
│   └── utils/
│       ├── retry.py            # Retry logic for API calls
│       └── time_info.py        # Timestamp utilities
├── database/
│   ├── chats_data/             # Persisted chat sessions (JSON)
│   ├── learning_data/          # Your custom documents & knowledge
│   └── vector_store/           # FAISS index files
├── config.py                   # Configuration & paths
├── run.py                      # Entry point to start the server
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment variables
├── .env                        # Your actual API keys (gitignored)
└── README.md                   # This file
```

---

## Private Data Storage

A.S.T.R.A stores your personal data locally on your machine and **never commits it to GitHub**. This includes:

### 1. **Chat History** (`database/chats_data/`)
- All your conversations with A.S.T.R.A are stored as JSON files
- Each session gets a unique UUID
- Files are stored locally only and excluded from version control
- See [database/chats_data/README.md](A.S.T.R.A/database/chats_data/README.md) for details

### 2. **Learning Data** (`database/learning_data/`)
- Your personal documents, notes, and knowledge base
- Used to enhance A.S.T.R.A's responses
- Completely private and not shared or backed up to GitHub
- See [database/learning_data/README.md](A.S.T.R.A/database/learning_data/README.md) for details

### 3. **Vector Store** (`database/vector_store/`)
- FAISS index and embeddings of your documents
- Generated automatically from your learning data
- Rebuilt on server restart if deleted
- Completely private to your machine
- See [database/vector_store/README.md](A.S.T.R.A/database/vector_store/README.md) for details

**Security Promise:**
- ✅ All data stays on your machine
- ✅ Nothing is uploaded to GitHub (see `.gitignore`)
- ✅ API keys are protected via `.env`
- ✅ You have complete control over your data

---

## Adding Learning Data

To make your assistant smarter with custom knowledge:

1. **Create text files** in `database/learning_data/`
```bash
database/learning_data/
├── my_knowledge.txt
├── research_notes.txt
└── company_info.txt
```

2. **Restart the server** - It will automatically vectorize your documents on startup

3. **Use in chats** - The vector store will retrieve relevant passages automatically

**Example learning_data.txt:**
```
My name is John Doe.
I work as a software engineer.
I'm interested in AI and machine learning.
```

For more details, see [database/learning_data/README.md](A.S.T.R.A/database/learning_data/README.md)

---

## Usage Examples

### Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Start a new chat session
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "Hello, A.S.T.R.A!"}
)

data = response.json()
print(f"Response: {data['response']}")
session_id = data['session_id']

# Continue conversation
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "message": "Tell me more about AI",
        "session_id": session_id
    }
)
print(response.json()['response'])

# Get full chat history
history = requests.get(f"{BASE_URL}/chat/history/{session_id}")
print(json.dumps(history.json(), indent=2))
```

### cURL

```bash
# General chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'

# Realtime chat with web search
curl -X POST "http://localhost:8000/chat/realtime" \
  -H "Content-Type: application/json" \
  -d '{"message": "Latest AI news 2024"}'

# Health check
curl "http://localhost:8000/health"
```

### JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000";

async function chat(message, sessionId = null) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId })
  });
  
  return await response.json();
}

// Start conversation
const firstMessage = await chat("Hello!");
console.log(firstMessage.response);
console.log("Session ID:", firstMessage.session_id);

// Continue with same session
const followUp = await chat("Tell me more", firstMessage.session_id);
console.log(followUp.response);
```

---

## Troubleshooting

### "Module not found" errors
```bash
# Ensure virtual environment is activated
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### API key errors
- Verify `.env` file exists in `A.S.T.R.A/` directory
- Check that `GROQ_API_KEY` and `TAVILY_API_KEY` are set correctly
- Ensure keys are not expired or revoked

### Connection refused (localhost:8000)
- Check if server is running
- Try a different port by editing `run.py`
- Ensure no other service is using port 8000

### Slow responses
- First query is slower (builds vector store)
- Check your internet connection for web search queries
- Consider your Groq API plan limits

### Vector store errors
- Delete `database/vector_store/` folder and restart
- Ensure `database/learning_data/` folder exists
- Check file permissions in database folders

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key |
| `GROQ_API_KEY_2-4` | ❌ | Backup keys for rate limit rotation |
| `GROQ_MODEL` | ✅ | Model name (default: `llama-3.3-70b-versatile`) |
| `TAVILY_API_KEY` | ✅ | Your Tavily web search API key |
| `ASTRA_USER_TITLE` | ❌ | Your name (for context) |
| `ASSISTANT_NAME` | ❌ | Assistant name (default: `A.S.T.R.A`) |

---

## Performance & Limits

- **Response Time**: 1-5 seconds for general chat, 3-10 seconds for realtime search
- **Concurrent Users**: Limited to 1 (single-user architecture)
- **Chat History**: Unlimited (stored as JSON files)
- **Learning Data**: Recommended max 50MB text files
- **Rate Limits**: Depends on your Groq/Tavily API plan

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source. Check the LICENSE file for details.

---

## Support & Contact

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Questions**: Check existing discussions or open a new one
- **Email**: Reach out through your GitHub profile

---

## Roadmap

- [ ] Multi-user support with authentication
- [ ] Database backend (PostgreSQL) instead of JSON files
- [ ] WebSocket support for real-time streaming
- [ ] UI dashboard for chat management
- [ ] Advanced prompt templating
- [ ] Rate limiting per session
- [ ] Analytics and usage tracking

---

## Acknowledgments

- **Groq** for lightning-fast LLM inference
- **Tavily** for web search capabilities
- **LangChain** for agent orchestration
- **FAISS** for vector similarity search
- **FastAPI** for the amazing web framework

---

## Disclaimer

This is a personal AI assistant project. Always ensure API keys are kept private and never commit `.env` files to version control. Use this responsibly and in accordance with Groq and Tavily's terms of service.

---

**Made with ❤️ by the A.S.T.R.A team**

Happy Coding! 🚀
