from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class QueryType(str, Enum):
    TIME_RANGE_EXTRACTION = "time_range_extraction"
    ACTIVITY_RECOMMENDATION = "activity_recommendation"  
    LOCATION_ANALYSIS = "location_analysis"
    MUSIC_DISCOVERY = "music_discovery"
    CONVERSATION = "conversation"

class LocationData(BaseModel):
    lat: float = Field(..., description="Latitude coordinate")
    lng: float = Field(..., description="Longitude coordinate")
    accuracy: Optional[float] = Field(None, description="GPS accuracy in meters")
    address: Optional[str] = Field(None, description="Human readable address")
    city: Optional[str] = Field(None, description="City name")
    country: Optional[str] = Field(None, description="Country name")

class TimeContext(BaseModel):
    current_time: datetime = Field(..., description="Current timestamp")
    timezone: Optional[str] = Field(None, description="User's timezone (e.g., 'America/New_York')")
    is_weekend: Optional[bool] = Field(None, description="Whether current time is weekend")
    time_of_day: Optional[str] = Field(None, description="morning|afternoon|evening|night")

class UserContext(BaseModel):
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    display_name: Optional[str] = Field(None, description="User display name")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    history: Optional[List[str]] = Field(None, description="Recent query history")

class ComplexLLMRequest(BaseModel):
    query: str = Field(..., description="User's query or request")
    query_type: QueryType = Field(..., description="Type of query being processed")
    location: Optional[LocationData] = Field(None, description="User's location context")
    time_context: TimeContext = Field(..., description="Current time context")
    user_context: Optional[UserContext] = Field(None, description="User-specific context")
    additional_context: Optional[Dict[str, Any]] = Field(None, description="Any additional context data")
    
    @validator('query')
    def query_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

class TimeRange(BaseModel):
    start_time: datetime = Field(..., description="Start of time range")
    end_time: datetime = Field(..., description="End of time range")
    description: str = Field(..., description="Human readable description of time range")
    
    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class TimeRangeExtractionResponse(BaseModel):
    time_range: TimeRange = Field(..., description="Extracted time range")
    reasoning: str = Field(..., description="Explanation of how time range was determined")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    query_type: str = Field(..., description="Classification of query type")
    raw_llm_response: Optional[str] = Field(None, description="Raw LLM response for debugging")

class LLMQueryResponse(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    query_type: QueryType = Field(..., description="Type of query processed")
    response_data: Dict[str, Any] = Field(..., description="Structured response data")
    raw_response: Optional[str] = Field(None, description="Raw LLM response")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if processing failed")

class BatchLLMRequest(BaseModel):
    requests: List[ComplexLLMRequest] = Field(..., description="List of LLM requests to process")
    parallel: bool = Field(default=False, description="Whether to process requests in parallel")
    max_parallel: int = Field(default=5, description="Maximum parallel requests")
    
    @validator('requests')
    def requests_not_empty(cls, v):
        if not v:
            raise ValueError('Requests list cannot be empty')
        if len(v) > 50:
            raise ValueError('Maximum 50 requests per batch')
        return v

class BatchLLMResponse(BaseModel):
    batch_id: str = Field(..., description="Unique batch identifier")
    responses: List[LLMQueryResponse] = Field(..., description="Individual responses")
    total_processing_time_ms: Optional[int] = Field(None, description="Total batch processing time")
    successful_count: int = Field(..., description="Number of successful responses")
    failed_count: int = Field(..., description="Number of failed responses")