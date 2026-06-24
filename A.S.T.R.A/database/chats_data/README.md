# Chat Data Examples
This folder stores your chat session history in JSON format.

Each chat is saved with a unique UUID as the filename. The actual chat data is automatically created when you use the application, but is NOT committed to version control for privacy reasons.

## Example Chat File Structure
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "What is machine learning?",
      "timestamp": "2024-06-24T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Machine learning is a subset of artificial intelligence...",
      "timestamp": "2024-06-24T10:30:05"
    }
  ],
  "created_at": "2024-06-24T10:30:00",
  "updated_at": "2024-06-24T10:30:05"
}
```

## Privacy Note
- Your chat history is stored locally only
- Chat files are NEVER committed to GitHub (see .gitignore)
- Each user's data remains completely private
