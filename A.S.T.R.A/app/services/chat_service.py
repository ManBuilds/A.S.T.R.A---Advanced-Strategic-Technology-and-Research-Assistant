import json
import logging
from pathlib import Path
from typing import List, Optional, Dict
import uuid

from config import CHATS_DATA_DIR, MAX_CHAT_HISTORY_TURNS
from app.models import ChatMessage, ChatHistory
from app.services.groq_services import GroqService
from app.services.realtime_service import RealtimeGroqService

# Changed logger name to A.S.T.R.A
logger = logging.getLogger("A.S.T.R.A")

# ==============================================================================
# CHAT SERVICE CLASS - ASTRA AI SYSTEM
# ==============================================================================

class ChatService:
    """
    Manages chat sessions: in-memory message lists, load/save to disk, and
    calling Groq (or Realtime) to get replies. All state for active sessions
    is in self.sessions; saving to disk is done after each message so
    conversations survive restarts.
    """

    def __init__(self, groq_service: GroqService, realtime_service: RealtimeGroqService = None):
        """Store references to the Groq and Realtime services; keep sessions in memory."""
        self.groq_service = groq_service
        self.realtime_service = realtime_service
        # Map: session_id -> list of ChatMessage (user and assistant messages in order).
        self.sessions: Dict[str, List[ChatMessage]] = {}

    # --------------------------------------------------------------------------
    # SESSION LOAD / VALIDATE / GET-OR-CREATE
    # --------------------------------------------------------------------------

    def load_session_from_disk(self, session_id: str) -> bool:
        """
        Load a session from database/chats_data/ if a file for this session_id exists.
        Returns True if loaded, False if file missing or unreadable.
        """
        # Sanitize ID for use in filename (no dashes or spaces).
        safe_session_id = session_id.replace("-", "").replace(" ", "_")
        filename = f"chat_{safe_session_id}.json"
        filepath = CHATS_DATA_DIR / filename

        if not filepath.exists():
            return False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                chat_dict = json.load(f)
            
            # Convert stored dicts back to ChatMessage objects.
            messages = [
                ChatMessage(role=msg.get("role"), content=msg.get("content"))
                for msg in chat_dict.get("messages", [])
            ]
            self.sessions[session_id] = messages
            return True
        except Exception as e:
            logger.warning("Failed to load session %s from disk: %s", session_id, e)
            return False

    def validate_session_id(self, session_id: str) -> bool:
        """Return True if session_id is safe to use."""
        if not session_id or not session_id.strip():
            return False
        
        if ".." in session_id or "/" in session_id or "\\" in session_id:
            return False
        
        if len(session_id) > 255:
            return False
            
        return True

    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Return a session ID and ensure it exists in memory."""
        if not session_id:
            new_session_id = str(uuid.uuid4())
            self.sessions[new_session_id] = []
            return new_session_id

        if not self.validate_session_id(session_id):
            raise ValueError(f"Invalid session_id format: {session_id}.")

        if session_id in self.sessions:
            return session_id

        if self.load_session_from_disk(session_id):
            return session_id

        # New session if not found on disk
        self.sessions[session_id] = []
        return session_id

    # --------------------------------------------------------------------------
    # MESSAGES AND HISTORY FORMATTING
    # --------------------------------------------------------------------------

    def add_message(self, session_id: str, role: str, content: str):
        """Append one message to the session's list."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(ChatMessage(role=role, content=content))

    def get_chat_history(self, session_id: str) -> List[ChatMessage]:
        """Return chronological message list."""
        return self.sessions.get(session_id, [])

    def format_history_for_llm(self, session_id: str, exclude_last: bool = False) -> List[tuple]:
        """Build (user, assistant) pairs for the LLM prompt."""
        messages = self.get_chat_history(session_id)
        history = []
        
        messages_to_process = messages[:-1] if exclude_last and messages else messages
        
        i = 0
        while i < len(messages_to_process) - 1:
            u_msg, a_msg = messages_to_process[i], messages_to_process[i + 1]
            if u_msg.role == "user" and a_msg.role == "assistant":
                history.append((u_msg.content, a_msg.content))
                i += 2
            else:
                i += 1
        
        if len(history) > MAX_CHAT_HISTORY_TURNS:
            history = history[-MAX_CHAT_HISTORY_TURNS:]
            
        return history

    # --------------------------------------------------------------------------
    # PROCESS MESSAGE
    # --------------------------------------------------------------------------

    def process_message(self, session_id: str, user_message: str) -> str:
        """Handle standard chat messages via Astra core."""
        self.add_message(session_id, "user", user_message)
        chat_history = self.format_history_for_llm(session_id, exclude_last=True)
        
        response = self.groq_service.get_response(question=user_message, chat_history=chat_history)
        
        self.add_message(session_id, "assistant", response)
        self.save_chat_session(session_id)
        return response

    def process_realtime_message(self, session_id: str, user_message: str) -> str:
        """Handle realtime (search-enabled) messages via Astra search."""
        if not self.realtime_service:
            raise ValueError("Astra Realtime service is not initialized.")
            
        self.add_message(session_id, "user", user_message)
        chat_history = self.format_history_for_llm(session_id, exclude_last=True)
        
        response = self.realtime_service.get_response(question=user_message, chat_history=chat_history)
        
        self.add_message(session_id, "assistant", response)
        self.save_chat_session(session_id)
        return response

    # --------------------------------------------------------------------------
    # PERSIST SESSION TO DISK
    # --------------------------------------------------------------------------

    def save_chat_session(self, session_id: str):
        """Write session to database/chats_data/*.json for persistence."""
        if session_id not in self.sessions:
            return

        safe_session_id = session_id.replace("-", "").replace(" ", "_")
        filename = f"chat_{safe_session_id}.json"
        filepath = CHATS_DATA_DIR / filename

        try:
            CHATS_DATA_DIR.mkdir(parents=True, exist_ok=True)
            session_data = {
                "session_id": session_id,
                "messages": [{"role": m.role, "content": m.content} for m in self.sessions[session_id]]
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save Astra session {session_id}: {e}")