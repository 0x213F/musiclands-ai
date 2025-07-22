import os
from typing import Optional, Dict, List
from openai import OpenAI

class ChatGPTService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("Warning: OPENAI_API_KEY not found in environment variables")

    def is_available(self) -> bool:
        """Check if OpenAI client is available"""
        return self.client is not None and self.api_key is not None

    def chat_completion(
        self, 
        message: str, 
        system_prompt: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Send a message to ChatGPT and get a response
        
        Args:
            message: User message to send to ChatGPT
            system_prompt: Optional system prompt to set context
            model: OpenAI model to use (default: gpt-3.5-turbo)
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0-1)
            
        Returns:
            ChatGPT response as string or None if error
        """
        if not self.is_available():
            return None
            
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"ChatGPT API error: {e}")
            return None

    def music_chat_completion(self, message: str, user_context: Optional[Dict] = None) -> Optional[str]:
        """
        Specialized chat completion for music-related queries
        
        Args:
            message: User's music-related question
            user_context: Optional user context (preferences, history, etc.)
            
        Returns:
            Music-focused ChatGPT response
        """
        # Create a music-focused system prompt
        system_prompt = """You are a knowledgeable music assistant for Musiclands AI. 
        You help users with music recommendations, song analysis, artist information, 
        playlist creation, and music-related questions. Always be helpful, enthusiastic 
        about music, and provide specific, actionable advice when possible."""
        
        # Add user context to the message if available
        if user_context:
            context_info = []
            if user_context.get("display_name"):
                context_info.append(f"User name: {user_context['display_name']}")
            if user_context.get("music_preferences"):
                context_info.append(f"Music preferences: {user_context['music_preferences']}")
            
            if context_info:
                message = f"Context: {', '.join(context_info)}\n\nQuestion: {message}"
        
        return self.chat_completion(
            message=message,
            system_prompt=system_prompt,
            model="gpt-3.5-turbo",
            max_tokens=800,
            temperature=0.8
        )

    def conversation_chat(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ) -> Optional[str]:
        """
        Handle multi-turn conversations
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt
            model: OpenAI model to use
            
        Returns:
            ChatGPT response as string or None if error
        """
        if not self.is_available():
            return None
            
        try:
            chat_messages = []
            
            # Add system prompt if provided
            if system_prompt:
                chat_messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation messages
            chat_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=chat_messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"ChatGPT conversation error: {e}")
            return None

# Global ChatGPT service instance
chatgpt_service = ChatGPTService()