from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class EventData(BaseModel):
    """Event happening at a location"""
    name: str = Field(..., description="Event name")
    artist: Optional[str] = Field(None, description="Artist/performer name")
    genre: Optional[str] = Field(None, description="Music genre or event type")
    start_time: str = Field(..., description="Event start time (formatted string)")
    end_time: str = Field(..., description="Event end time (formatted string)")
    description: Optional[str] = Field(None, description="Event description")
    type: Optional[str] = Field(None, description="Event type (performance, food, activity, etc.)")
    vip_only: bool = Field(default=False, description="Whether event is VIP only")
    age_restriction: Optional[str] = Field(None, description="Age restrictions if any")
    expected_crowd: Optional[str] = Field(None, description="Expected crowd level")
    ticket_required: bool = Field(default=False, description="Whether separate ticket needed")

class LocationCoordinates(BaseModel):
    """GPS coordinates for a location"""
    lat: float = Field(..., description="Latitude", ge=-90, le=90)
    lng: float = Field(..., description="Longitude", ge=-180, le=180)

class LocationData(BaseModel):
    """Complete location data with events"""
    id: str = Field(..., description="Unique location identifier")
    name: str = Field(..., description="Location name")
    description: Optional[str] = Field(None, description="Location description")
    coordinates: LocationCoordinates = Field(..., description="GPS coordinates")
    capacity: Optional[int] = Field(None, description="Maximum capacity", ge=0)
    current_crowd_level: Optional[str] = Field(None, description="Current crowd level (Low/Medium/High/Very High)")
    amenities: List[str] = Field(default_factory=list, description="Available amenities")
    events: List[EventData] = Field(default_factory=list, description="Events at this location")
    accessibility: Optional[str] = Field(None, description="Accessibility information")
    wait_time: Optional[int] = Field(None, description="Current wait time in minutes", ge=0)
    
    @validator('id')
    def id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Location ID cannot be empty')
        return v.strip()
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Location name cannot be empty')
        return v.strip()

class UserContextData(BaseModel):
    """User's current context and situation"""
    energy_level: Optional[str] = Field(None, description="User's energy level (Low/Medium/High)")
    group_size: Optional[int] = Field(None, description="Size of user's group", ge=1)
    group_vibe: Optional[str] = Field(None, description="Group mood/vibe")
    time_at_festival: Optional[str] = Field(None, description="How long user has been at the event")
    last_meal: Optional[str] = Field(None, description="When user last ate")
    budget_level: Optional[str] = Field(None, description="Budget level (Low/Medium/High)")
    mobility: Optional[str] = Field(None, description="Mobility level (Limited/Normal/High)")
    weather_preference: Optional[str] = Field(None, description="Weather/indoor/outdoor preference")

class UserPreferences(BaseModel):
    """User's preferences and interests"""
    music_genres: List[str] = Field(default_factory=list, description="Preferred music genres")
    activity_types: List[str] = Field(default_factory=list, description="Preferred activity types")
    crowd_preference: Optional[str] = Field(None, description="Preferred crowd size")
    walking_tolerance: Optional[str] = Field(None, description="Walking tolerance (Low/Medium/High)")
    discovery_mode: bool = Field(default=False, description="Whether user wants to discover new things")
    food_preferences: List[str] = Field(default_factory=list, description="Food preferences/restrictions")
    social_level: Optional[str] = Field(None, description="Social engagement preference")

class LocationIntelligenceRequest(BaseModel):
    """Request for location-based intelligence"""
    query: str = Field(..., description="User's query/question")
    current_time: datetime = Field(..., description="Current timestamp")
    user_location: Optional[LocationCoordinates] = Field(None, description="User's current GPS location")
    locations_data: List[LocationData] = Field(..., description="List of all locations with events")
    travel_time_matrix: Dict[str, Dict[str, int]] = Field(..., description="Travel times between locations in minutes")
    user_context: Optional[UserContextData] = Field(None, description="User's current context")
    user_preferences: Optional[UserPreferences] = Field(None, description="User preferences")
    timezone: Optional[str] = Field(None, description="User's timezone")
    
    @validator('query')
    def query_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()
    
    @validator('locations_data')
    def locations_not_empty(cls, v):
        if not v:
            raise ValueError('Locations data cannot be empty')
        if len(v) > 50:  # Reasonable limit
            raise ValueError('Too many locations (max 50)')
        return v
    
    @validator('travel_time_matrix')
    def travel_matrix_valid(cls, v, values):
        if not v:
            return v
        
        # Validate that all location IDs in matrix exist in locations_data
        if 'locations_data' in values:
            location_ids = {loc.id for loc in values['locations_data']}
            matrix_ids = set(v.keys())
            
            # Check if all matrix keys correspond to actual locations
            invalid_ids = matrix_ids - location_ids
            if invalid_ids:
                raise ValueError(f'Travel matrix contains invalid location IDs: {invalid_ids}')
        
        return v

class LocationIntelligenceResponse(BaseModel):
    """Response from location intelligence system"""
    recommendation: str = Field(..., description="Main recommendation response")
    reasoning: Optional[str] = Field(None, description="Reasoning behind the recommendation")
    suggested_locations: List[str] = Field(default_factory=list, description="Suggested location IDs")
    travel_estimates: Optional[Dict[str, int]] = Field(None, description="Travel time estimates to suggested locations")
    alternative_options: Optional[str] = Field(None, description="Alternative options if applicable")
    pro_tips: Optional[str] = Field(None, description="Pro tips for the best experience")
    timing_considerations: Optional[str] = Field(None, description="Important timing information")
    crowd_warnings: Optional[str] = Field(None, description="Crowd level warnings or info")
    practical_info: Optional[str] = Field(None, description="Practical logistics information")
    confidence_score: Optional[float] = Field(None, description="Confidence in recommendation (0-1)", ge=0, le=1)

class BatchLocationRequest(BaseModel):
    """Request for processing multiple location queries"""
    requests: List[LocationIntelligenceRequest] = Field(..., description="List of location intelligence requests")
    shared_context: Optional[Dict[str, Any]] = Field(None, description="Context shared across all requests")
    processing_mode: str = Field(default="sequential", description="Processing mode: sequential or parallel")
    
    @validator('requests')
    def requests_not_empty(cls, v):
        if not v:
            raise ValueError('Requests list cannot be empty')
        if len(v) > 20:
            raise ValueError('Too many requests in batch (max 20)')
        return v

class LocationDataSummary(BaseModel):
    """Summary of location data for quick overview"""
    total_locations: int = Field(..., description="Total number of locations")
    total_events: int = Field(..., description="Total number of events")
    active_events_now: int = Field(..., description="Number of events happening now")
    upcoming_events: int = Field(..., description="Number of upcoming events in next 2 hours")
    high_crowd_locations: List[str] = Field(default_factory=list, description="Locations with high crowds")
    recommended_for_discovery: List[str] = Field(default_factory=list, description="Locations good for discovery")
    food_locations: List[str] = Field(default_factory=list, description="Food/dining locations")
    music_locations: List[str] = Field(default_factory=list, description="Music performance locations")
    quiet_zones: List[str] = Field(default_factory=list, description="Quieter locations for rest")

class SmartRoutingRequest(BaseModel):
    """Request for smart routing between multiple locations"""
    start_location: str = Field(..., description="Starting location ID")
    desired_locations: List[str] = Field(..., description="List of locations user wants to visit")
    available_time: int = Field(..., description="Available time in minutes", gt=0)
    priorities: Optional[List[str]] = Field(None, description="Priority order of locations")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Constraints (avoid crowds, time windows, etc.)")

class SmartRoutingResponse(BaseModel):
    """Response with optimized route and timeline"""
    optimized_route: List[Dict[str, Any]] = Field(..., description="Optimized route with timing")
    total_time_needed: int = Field(..., description="Total time needed for the route in minutes")
    feasibility_score: float = Field(..., description="How feasible the route is (0-1)", ge=0, le=1)
    alternative_routes: Optional[List[Dict[str, Any]]] = Field(None, description="Alternative route options")
    recommendations: str = Field(..., description="Recommendations for the route")
    potential_issues: Optional[str] = Field(None, description="Potential issues or conflicts")