from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from services.llm_prompt_service import llm_prompt_service
from services.firebase_auth_service import FirebaseAuthService
from models.user import User
from models.llm.requests import (
    ComplexLLMRequest, 
    LLMQueryResponse, 
    TimeRangeExtractionResponse,
    BatchLLMRequest,
    BatchLLMResponse,
    QueryType,
    LocationData,
    TimeContext,
    UserContext
)

router = APIRouter(prefix="/llm", tags=["LLM Queries"])
firebase_auth = FirebaseAuthService()

# Dependency to get current user from Firebase ID token (optional)
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

@router.post("/time-range-extraction", response_model=TimeRangeExtractionResponse)
async def extract_time_range(
    request_data: dict,
    current_user: User = Depends(get_current_user_optional)
):
    """
    Extract time range from user query with context
    
    Example request:
    {
        "query": "What should I do tonight?",
        "location": {
            "lat": 40.7128,
            "lng": -74.0060,
            "city": "New York"
        },
        "timezone": "America/New_York"
    }
    """
    try:
        # Build time context
        current_time = datetime.now(timezone.utc)
        timezone_str = request_data.get("timezone", "UTC")
        
        time_context = TimeContext(
            current_time=current_time,
            timezone=timezone_str
        )
        
        # Build location context if provided
        location = None
        if location_data := request_data.get("location"):
            location = LocationData(**location_data)
        
        # Build user context if authenticated
        user_context = None
        if current_user:
            user_context = UserContext(
                user_id=current_user.uid,
                display_name=current_user.display_name
            )
        
        # Create complex LLM request
        llm_request = ComplexLLMRequest(
            query=request_data["query"],
            query_type=QueryType.TIME_RANGE_EXTRACTION,
            location=location,
            time_context=time_context,
            user_context=user_context
        )
        
        # Process the query
        response = await llm_prompt_service.process_query(llm_request)
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error)
        
        # Convert to time range extraction response
        return TimeRangeExtractionResponse(**response.response_data)
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/activity-recommendation", response_model=LLMQueryResponse)
async def get_activity_recommendation(
    request_data: dict,
    current_user: User = Depends(get_current_user_optional)
):
    """
    Get activity recommendations based on query and context
    
    Example request:
    {
        "query": "What should I do this afternoon?",
        "location": {
            "lat": 40.7128,
            "lng": -74.0060,
            "city": "New York"
        },
        "timezone": "America/New_York"
    }
    """
    try:
        # Build time context
        current_time = datetime.now(timezone.utc)
        timezone_str = request_data.get("timezone", "UTC")
        
        time_context = TimeContext(
            current_time=current_time,
            timezone=timezone_str
        )
        
        # Build location context if provided
        location = None
        if location_data := request_data.get("location"):
            location = LocationData(**location_data)
        
        # Build user context if authenticated
        user_context = None
        if current_user:
            user_context = UserContext(
                user_id=current_user.uid,
                display_name=current_user.display_name
            )
        
        # Create complex LLM request
        llm_request = ComplexLLMRequest(
            query=request_data["query"],
            query_type=QueryType.ACTIVITY_RECOMMENDATION,
            location=location,
            time_context=time_context,
            user_context=user_context
        )
        
        # Process the query
        response = await llm_prompt_service.process_query(llm_request)
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/music-discovery", response_model=LLMQueryResponse)
async def discover_music(
    request_data: dict,
    current_user: User = Depends(get_current_user_optional)
):
    """
    Get music recommendations and discovery based on query
    
    Example request:
    {
        "query": "Recommend some chill music for studying",
        "preferences": {
            "genres": ["indie", "electronic"],
            "mood": "relaxed"
        }
    }
    """
    try:
        # Build time context
        current_time = datetime.now(timezone.utc)
        time_context = TimeContext(current_time=current_time)
        
        # Build user context with preferences
        user_context = None
        if current_user:
            preferences = request_data.get("preferences", {})
            user_context = UserContext(
                user_id=current_user.uid,
                display_name=current_user.display_name,
                preferences=preferences
            )
        
        # Create complex LLM request
        llm_request = ComplexLLMRequest(
            query=request_data["query"],
            query_type=QueryType.MUSIC_DISCOVERY,
            time_context=time_context,
            user_context=user_context
        )
        
        # Process the query
        response = await llm_prompt_service.process_query(llm_request)
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/complex-query", response_model=LLMQueryResponse)
async def process_complex_query(
    llm_request: ComplexLLMRequest,
    current_user: User = Depends(get_current_user_optional)
):
    """
    Process any complex LLM query with full context support
    
    This is the most flexible endpoint that accepts the full ComplexLLMRequest model
    """
    try:
        # Add user context if authenticated and not already provided
        if current_user and not llm_request.user_context:
            llm_request.user_context = UserContext(
                user_id=current_user.uid,
                display_name=current_user.display_name
            )
        
        # Process the query
        response = await llm_prompt_service.process_query(llm_request)
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=BatchLLMResponse)
async def process_batch_queries(
    batch_request: BatchLLMRequest,
    current_user: User = Depends(get_current_user_optional)
):
    """
    Process multiple LLM queries in batch (sequential or parallel)
    
    Example request:
    {
        "requests": [
            {
                "query": "What should I do tonight?",
                "query_type": "time_range_extraction",
                "time_context": {"current_time": "2024-01-15T20:00:00Z"}
            },
            {
                "query": "Recommend some music for my mood",
                "query_type": "music_discovery",
                "time_context": {"current_time": "2024-01-15T20:00:00Z"}
            }
        ],
        "parallel": true,
        "max_parallel": 3
    }
    """
    try:
        # Add user context to all requests if authenticated
        if current_user:
            for request in batch_request.requests:
                if not request.user_context:
                    request.user_context = UserContext(
                        user_id=current_user.uid,
                        display_name=current_user.display_name
                    )
        
        # Process the batch
        response = await llm_prompt_service.process_batch(batch_request)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/example-queries")
async def get_example_queries():
    """Get example queries for testing different prompt types"""
    from prompts.time_range_extractor import TimeRangeExtractorPrompt
    
    return {
        "time_range_extraction": TimeRangeExtractorPrompt.get_example_queries(),
        "activity_recommendation": {
            "indoor_activities": {
                "query": "What can I do indoors on a rainy day?",
                "description": "Indoor activity suggestions"
            },
            "outdoor_adventure": {
                "query": "I want to go on an outdoor adventure this weekend",
                "description": "Outdoor activity planning"
            },
            "date_night": {
                "query": "Plan a romantic date night in the city",
                "description": "Date planning with location context"
            }
        },
        "music_discovery": {
            "mood_based": {
                "query": "I'm feeling nostalgic, what music should I listen to?",
                "description": "Mood-based music recommendations"
            },
            "activity_based": {
                "query": "What's good workout music for running?",
                "description": "Activity-specific music suggestions"
            },
            "genre_exploration": {
                "query": "I like indie rock, what similar genres should I explore?",
                "description": "Genre discovery and expansion"
            }
        }
    }