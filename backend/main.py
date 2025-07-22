import os
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import auth, llm, festival
from services.firebase_auth_service import FirebaseAuthService
from services.chatgpt_service import chatgpt_service
from models.user import User
from models.chat import ChatMessage, ChatResponse, ConversationRequest, MusicChatRequest

load_dotenv()

app = FastAPI(
    title="Musiclands AI API",
    description="Backend API for Musiclands AI mobile application with Firebase auth and ChatGPT integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
firebase_auth = FirebaseAuthService()

# Include authentication routes
app.include_router(auth.router)

# Include LLM routes
app.include_router(llm.router)

# Include festival routes
app.include_router(festival.router)

# Dependency to get current user from Firebase ID token
async def get_current_user_optional(authorization: str = None) -> User:
    """Get current user from Firebase ID token (optional)"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    id_token = authorization.split("Bearer ")[1]
    token_data = firebase_auth.verify_id_token(id_token)
    
    if not token_data:
        return None
    
    user = firebase_auth.get_user_by_uid(token_data.get("uid"))
    return user

@app.get("/")
async def root():
    return {"message": "Welcome to Musiclands AI API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "firebase": firebase_auth.db is not None,
            "chatgpt": chatgpt_service.is_available()
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_user_optional)
):
    """Simple chat endpoint using ChatGPT"""
    if not chatgpt_service.is_available():
        raise HTTPException(status_code=503, detail="ChatGPT service is not available")
    
    user_message = chat_request.message
    
    # Get ChatGPT response
    if current_user:
        # Include user context for personalized responses
        user_context = {
            "display_name": current_user.display_name,
            "email": current_user.email
        }
        ai_response = chatgpt_service.music_chat_completion(user_message, user_context)
    else:
        ai_response = chatgpt_service.music_chat_completion(user_message)
    
    if not ai_response:
        ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
    
    return ChatResponse(
        response=ai_response,
        message_id=str(uuid.uuid4()),
        user_id=current_user.uid if current_user else None
    )

@app.post("/chat/music", response_model=ChatResponse)
async def music_chat_endpoint(
    chat_request: MusicChatRequest,
    current_user: User = Depends(get_current_user_optional)
):
    """Music-specialized chat endpoint"""
    if not chatgpt_service.is_available():
        raise HTTPException(status_code=503, detail="ChatGPT service is not available")
    
    user_context = None
    if current_user and chat_request.include_user_context:
        user_context = {
            "display_name": current_user.display_name,
            "email": current_user.email
        }
    
    ai_response = chatgpt_service.music_chat_completion(chat_request.message, user_context)
    
    if not ai_response:
        ai_response = "I'm sorry, I'm having trouble processing your music question right now. Please try again later."
    
    return ChatResponse(
        response=ai_response,
        message_id=str(uuid.uuid4()),
        user_id=current_user.uid if current_user else None
    )

@app.post("/chat/conversation", response_model=ChatResponse)
async def conversation_endpoint(
    conversation_request: ConversationRequest,
    current_user: User = Depends(get_current_user_optional)
):
    """Multi-turn conversation endpoint"""
    if not chatgpt_service.is_available():
        raise HTTPException(status_code=503, detail="ChatGPT service is not available")
    
    # Convert to format expected by ChatGPT service
    messages = [{"role": msg.role, "content": msg.content} for msg in conversation_request.messages]
    
    ai_response = chatgpt_service.conversation_chat(
        messages=messages,
        system_prompt=conversation_request.system_prompt
    )
    
    if not ai_response:
        ai_response = "I'm sorry, I'm having trouble with this conversation right now. Please try again later."
    
    return ChatResponse(
        response=ai_response,
        message_id=str(uuid.uuid4()),
        user_id=current_user.uid if current_user else None
    )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    environment = os.getenv("ENVIRONMENT", "development")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=environment == "development"
    )