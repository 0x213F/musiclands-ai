from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Genre(str, Enum):
    """Music genres"""
    ELECTRONIC = "electronic"
    HIP_HOP = "hip-hop"
    ROCK = "rock"
    INDIE = "indie"
    POP = "pop"
    JAZZ = "jazz"
    REGGAE = "reggae"
    FOLK = "folk"
    COUNTRY = "country"
    RNB = "r&b"
    FUNK = "funk"
    HOUSE = "house"
    TECHNO = "techno"
    DUBSTEP = "dubstep"
    TRAP = "trap"
    ALTERNATIVE = "alternative"
    PUNK = "punk"
    METAL = "metal"
    CLASSICAL = "classical"
    WORLD = "world"
    OTHER = "other"

class StageType(str, Enum):
    """Stage types"""
    MAIN_STAGE = "main_stage"
    SECONDARY_STAGE = "secondary_stage"
    TENT = "tent"
    PAVILION = "pavilion"
    OUTDOOR = "outdoor"
    INDOOR = "indoor"
    VIP = "vip"
    SILENT_DISCO = "silent_disco"
    COMEDY = "comedy"
    WORKSHOP = "workshop"

# GPS Coordinate model
class GPSCoordinate(BaseModel):
    """GPS coordinates for location data"""
    lat: float = Field(..., description="Latitude coordinate", ge=-90, le=90)
    lng: float = Field(..., description="Longitude coordinate", ge=-180, le=180)
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    accuracy: Optional[float] = Field(None, description="GPS accuracy in meters")

# Artist models
class Artist(BaseModel):
    """Artist/performer model"""
    artist_id: str = Field(..., description="Unique artist identifier")
    name: str = Field(..., description="Artist name", min_length=1, max_length=200)
    genres: List[Genre] = Field(default_factory=list, description="Music genres")
    bio: Optional[str] = Field(None, description="Artist biography", max_length=2000)
    image_url: Optional[str] = Field(None, description="Artist profile image URL")
    website: Optional[str] = Field(None, description="Artist website")
    spotify_url: Optional[str] = Field(None, description="Spotify artist URL")
    instagram: Optional[str] = Field(None, description="Instagram handle")
    twitter: Optional[str] = Field(None, description="Twitter handle")
    popularity_score: Optional[int] = Field(None, description="Popularity score (0-100)", ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Artist name cannot be empty')
        return v.strip()

class ArtistCreate(BaseModel):
    """Artist creation request"""
    name: str = Field(..., description="Artist name", min_length=1, max_length=200)
    genres: List[Genre] = Field(default_factory=list, description="Music genres")
    bio: Optional[str] = Field(None, description="Artist biography", max_length=2000)
    image_url: Optional[str] = Field(None, description="Artist profile image URL")
    website: Optional[str] = Field(None, description="Artist website")
    spotify_url: Optional[str] = Field(None, description="Spotify artist URL")
    instagram: Optional[str] = Field(None, description="Instagram handle")
    twitter: Optional[str] = Field(None, description="Twitter handle")
    popularity_score: Optional[int] = Field(None, description="Popularity score (0-100)", ge=0, le=100)

class ArtistUpdate(BaseModel):
    """Artist update request"""
    name: Optional[str] = Field(None, description="Artist name", min_length=1, max_length=200)
    genres: Optional[List[Genre]] = Field(None, description="Music genres")
    bio: Optional[str] = Field(None, description="Artist biography", max_length=2000)
    image_url: Optional[str] = Field(None, description="Artist profile image URL")
    website: Optional[str] = Field(None, description="Artist website")
    spotify_url: Optional[str] = Field(None, description="Spotify artist URL")
    instagram: Optional[str] = Field(None, description="Instagram handle")
    twitter: Optional[str] = Field(None, description="Twitter handle")
    popularity_score: Optional[int] = Field(None, description="Popularity score (0-100)", ge=0, le=100)

# Stage models
class Stage(BaseModel):
    """Stage/venue location model"""
    stage_id: str = Field(..., description="Unique stage identifier")
    name: str = Field(..., description="Stage name", min_length=1, max_length=200)
    stage_type: StageType = Field(..., description="Type of stage")
    location: GPSCoordinate = Field(..., description="GPS coordinates of the stage")
    capacity: Optional[int] = Field(None, description="Maximum capacity", ge=0)
    description: Optional[str] = Field(None, description="Stage description", max_length=1000)
    amenities: List[str] = Field(default_factory=list, description="Available amenities (food, drinks, seating, etc.)")
    accessibility: Optional[str] = Field(None, description="Accessibility information")
    sound_system: Optional[str] = Field(None, description="Sound system details")
    lighting: Optional[str] = Field(None, description="Lighting system details")
    backstage_facilities: Optional[str] = Field(None, description="Backstage facilities")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Stage name cannot be empty')
        return v.strip()

class StageCreate(BaseModel):
    """Stage creation request"""
    name: str = Field(..., description="Stage name", min_length=1, max_length=200)
    stage_type: StageType = Field(..., description="Type of stage")
    location: GPSCoordinate = Field(..., description="GPS coordinates of the stage")
    capacity: Optional[int] = Field(None, description="Maximum capacity", ge=0)
    description: Optional[str] = Field(None, description="Stage description", max_length=1000)
    amenities: List[str] = Field(default_factory=list, description="Available amenities")
    accessibility: Optional[str] = Field(None, description="Accessibility information")
    sound_system: Optional[str] = Field(None, description="Sound system details")
    lighting: Optional[str] = Field(None, description="Lighting system details")
    backstage_facilities: Optional[str] = Field(None, description="Backstage facilities")

class StageUpdate(BaseModel):
    """Stage update request"""
    name: Optional[str] = Field(None, description="Stage name", min_length=1, max_length=200)
    stage_type: Optional[StageType] = Field(None, description="Type of stage")
    location: Optional[GPSCoordinate] = Field(None, description="GPS coordinates of the stage")
    capacity: Optional[int] = Field(None, description="Maximum capacity", ge=0)
    description: Optional[str] = Field(None, description="Stage description", max_length=1000)
    amenities: Optional[List[str]] = Field(None, description="Available amenities")
    accessibility: Optional[str] = Field(None, description="Accessibility information")
    sound_system: Optional[str] = Field(None, description="Sound system details")
    lighting: Optional[str] = Field(None, description="Lighting system details")
    backstage_facilities: Optional[str] = Field(None, description="Backstage facilities")

# Performance models
class Performance(BaseModel):
    """Performance/show model with relationships to Artist and Stage"""
    performance_id: str = Field(..., description="Unique performance identifier")
    artist_id: str = Field(..., description="Reference to Artist")
    stage_id: str = Field(..., description="Reference to Stage")
    start_time: datetime = Field(..., description="Performance start time")
    end_time: datetime = Field(..., description="Performance end time")
    title: Optional[str] = Field(None, description="Performance title (if different from artist name)")
    description: Optional[str] = Field(None, description="Performance description", max_length=1000)
    set_type: Optional[str] = Field(None, description="Type of set (main, opening, closing, etc.)")
    special_notes: Optional[str] = Field(None, description="Special performance notes")
    ticket_required: bool = Field(default=False, description="Whether separate ticket is required")
    vip_only: bool = Field(default=False, description="Whether performance is VIP only")
    age_restriction: Optional[int] = Field(None, description="Minimum age requirement", ge=0, le=21)
    expected_attendance: Optional[int] = Field(None, description="Expected attendance", ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # Related data (populated by service layer)
    artist: Optional[Artist] = Field(None, description="Artist details")
    stage: Optional[Stage] = Field(None, description="Stage details")
    
    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v
    
    @validator('title')
    def title_valid(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None

class PerformanceCreate(BaseModel):
    """Performance creation request"""
    artist_id: str = Field(..., description="Reference to Artist")
    stage_id: str = Field(..., description="Reference to Stage")
    start_time: datetime = Field(..., description="Performance start time")
    end_time: datetime = Field(..., description="Performance end time")
    title: Optional[str] = Field(None, description="Performance title")
    description: Optional[str] = Field(None, description="Performance description", max_length=1000)
    set_type: Optional[str] = Field(None, description="Type of set")
    special_notes: Optional[str] = Field(None, description="Special performance notes")
    ticket_required: bool = Field(default=False, description="Whether separate ticket is required")
    vip_only: bool = Field(default=False, description="Whether performance is VIP only")
    age_restriction: Optional[int] = Field(None, description="Minimum age requirement", ge=0, le=21)
    expected_attendance: Optional[int] = Field(None, description="Expected attendance", ge=0)
    
    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class PerformanceUpdate(BaseModel):
    """Performance update request"""
    artist_id: Optional[str] = Field(None, description="Reference to Artist")
    stage_id: Optional[str] = Field(None, description="Reference to Stage")
    start_time: Optional[datetime] = Field(None, description="Performance start time")
    end_time: Optional[datetime] = Field(None, description="Performance end time")
    title: Optional[str] = Field(None, description="Performance title")
    description: Optional[str] = Field(None, description="Performance description", max_length=1000)
    set_type: Optional[str] = Field(None, description="Type of set")
    special_notes: Optional[str] = Field(None, description="Special performance notes")
    ticket_required: Optional[bool] = Field(None, description="Whether separate ticket is required")
    vip_only: Optional[bool] = Field(None, description="Whether performance is VIP only")
    age_restriction: Optional[int] = Field(None, description="Minimum age requirement", ge=0, le=21)
    expected_attendance: Optional[int] = Field(None, description="Expected attendance", ge=0)

# Query/filter models
class PerformanceFilters(BaseModel):
    """Filters for querying performances"""
    artist_id: Optional[str] = Field(None, description="Filter by artist ID")
    stage_id: Optional[str] = Field(None, description="Filter by stage ID")
    start_date: Optional[datetime] = Field(None, description="Filter performances starting after this date")
    end_date: Optional[datetime] = Field(None, description="Filter performances ending before this date")
    genres: Optional[List[Genre]] = Field(None, description="Filter by artist genres")
    stage_type: Optional[StageType] = Field(None, description="Filter by stage type")
    vip_only: Optional[bool] = Field(None, description="Filter VIP performances")
    age_restriction: Optional[int] = Field(None, description="Filter by age restriction")

class PerformanceSchedule(BaseModel):
    """Performance schedule view with all related data"""
    performances: List[Performance] = Field(..., description="List of performances with related data")
    total_count: int = Field(..., description="Total number of performances")
    date_range: dict = Field(..., description="Start and end dates of the schedule")
    stages: List[Stage] = Field(..., description="All stages in the schedule")
    artists: List[Artist] = Field(..., description="All artists in the schedule")