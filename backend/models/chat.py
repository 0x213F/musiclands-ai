from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ChatMessage(BaseModel):
    message: str = Field(..., description="User message to send to AI")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response")
    message_id: str = Field(..., description="Unique message identifier")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")

class ConversationMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")

class ConversationRequest(BaseModel):
    messages: List[ConversationMessage] = Field(..., description="Conversation history")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt")

class MusicChatRequest(BaseModel):
    message: str = Field(..., description="Music-related question")
    include_user_context: bool = Field(default=True, description="Include user preferences in context")