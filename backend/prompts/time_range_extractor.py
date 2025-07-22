"""
Time Range Extraction Prompt
This prompt analyzes user requests and determines the relevant time range they're asking about.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
import json

class TimeRangeExtractorPrompt:
    """Prompt template for extracting time ranges from user queries"""
    
    @staticmethod
    def build_prompt(
        user_query: str,
        current_time: datetime,
        user_location: Optional[Dict[str, float]] = None,
        timezone_info: Optional[str] = None
    ) -> str:
        """
        Build a prompt to extract time range from user query
        
        Args:
            user_query: The user's request/question
            current_time: Current datetime
            user_location: Dict with 'lat' and 'lng' keys (optional)
            timezone_info: User's timezone (optional)
            
        Returns:
            Formatted prompt string
        """
        
        # Format current time info
        time_info = f"Current time: {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}"
        if timezone_info:
            time_info += f" ({timezone_info})"
        
        # Format location info if provided
        location_info = ""
        if user_location:
            location_info = f"""
Location Context:
- GPS Coordinates: {user_location.get('lat', 'N/A')}, {user_location.get('lng', 'N/A')}
- This can help determine local context for activities, weather, business hours, etc.
"""
        
        prompt = f"""You are an expert at analyzing user requests and determining the time range they are asking about. Your job is to extract the relevant time period from their query.

CONTEXT:
{time_info}
{location_info}

USER QUERY: "{user_query}"

INSTRUCTIONS:
1. Analyze the user's query to determine what time range they are asking about
2. Consider implicit time references (e.g., "what should I do?" likely means "right now" or "soon")
3. Consider the current time of day and how it affects the request
4. Consider location context if activities are location-dependent

RESPONSE FORMAT:
You must respond with a JSON object containing:
{{
    "time_range": {{
        "start_time": "YYYY-MM-DD HH:MM",
        "end_time": "YYYY-MM-DD HH:MM",
        "description": "Brief description of the time range"
    }},
    "reasoning": "Explain why you chose this time range",
    "confidence": 0.95,
    "query_type": "immediate|planned|scheduled|recurring|vague"
}}

EXAMPLES:
- "What should I do?" → Next 1-2 hours from now
- "What should I do tonight?" → Evening hours (6 PM - 12 AM today)
- "What should I do this weekend?" → Upcoming weekend
- "What should I do for lunch?" → Next 1-2 hours around typical lunch time
- "Activities for tomorrow morning" → Tomorrow 6 AM - 12 PM
- "Weekend plans" → Upcoming Saturday-Sunday
- "Date ideas for Friday night" → This coming Friday evening

IMPORTANT:
- Always use 24-hour format for times
- Default to reasonable time ranges if the query is vague
- Consider the user's current time zone
- Be practical about activity timing
- If very vague, default to the next 1-2 hours

Now analyze the user query and provide the time range analysis:"""

        return prompt

    @staticmethod
    def parse_response(llm_response: str) -> Optional[Dict[str, Any]]:
        """
        Parse the LLM response to extract structured time range data
        
        Args:
            llm_response: Raw response from the LLM
            
        Returns:
            Parsed time range data or None if parsing fails
        """
        try:
            # Try to find JSON in the response
            start_idx = llm_response.find('{')
            end_idx = llm_response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                return None
            
            json_str = llm_response[start_idx:end_idx]
            parsed_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['time_range', 'reasoning', 'confidence', 'query_type']
            if not all(field in parsed_data for field in required_fields):
                return None
            
            time_range = parsed_data['time_range']
            if not all(field in time_range for field in ['start_time', 'end_time', 'description']):
                return None
            
            return parsed_data
            
        except (json.JSONDecodeError, KeyError, IndexError):
            return None

    @staticmethod
    def get_example_queries() -> Dict[str, Dict[str, Any]]:
        """
        Return example queries and their expected time ranges for testing
        
        Returns:
            Dictionary of example queries with expected responses
        """
        return {
            "what_should_i_do": {
                "query": "What should I do?",
                "expected_type": "immediate",
                "expected_duration_hours": 2,
                "description": "Immediate activity request"
            },
            "tonight_plans": {
                "query": "What should I do tonight?",
                "expected_type": "planned",
                "expected_duration_hours": 6,
                "description": "Evening activity request"
            },
            "lunch_ideas": {
                "query": "Where should I go for lunch?",
                "expected_type": "immediate",
                "expected_duration_hours": 2,
                "description": "Meal-specific request"
            },
            "weekend_activities": {
                "query": "What are some fun weekend activities?",
                "expected_type": "planned",
                "expected_duration_hours": 48,
                "description": "Weekend planning request"
            },
            "date_night": {
                "query": "Date ideas for Friday night",
                "expected_type": "scheduled",
                "expected_duration_hours": 4,
                "description": "Specific day evening request"
            },
            "morning_routine": {
                "query": "What should I do tomorrow morning?",
                "expected_type": "planned",
                "expected_duration_hours": 6,
                "description": "Next day morning request"
            }
        }