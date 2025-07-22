from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime, date
from models.festival import (
    Artist, ArtistCreate, ArtistUpdate,
    Stage, StageCreate, StageUpdate,
    Performance, PerformanceCreate, PerformanceUpdate,
    PerformanceFilters, PerformanceSchedule, Genre, StageType
)
from services.festival_service import artist_service, stage_service, performance_service

router = APIRouter(prefix="/festival", tags=["Festival Management"])

# Artist endpoints
@router.post("/artists", response_model=Artist)
async def create_artist(artist_data: ArtistCreate):
    """Create a new artist"""
    try:
        artist = artist_service.create_artist(artist_data)
        if not artist:
            raise HTTPException(status_code=500, detail="Failed to create artist")
        return artist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/artists/{artist_id}", response_model=Artist)
async def get_artist(artist_id: str):
    """Get artist by ID"""
    artist = artist_service.get_artist(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.put("/artists/{artist_id}", response_model=Artist)
async def update_artist(artist_id: str, artist_data: ArtistUpdate):
    """Update artist"""
    try:
        artist = artist_service.update_artist(artist_id, artist_data)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        return artist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/artists/{artist_id}")
async def delete_artist(artist_id: str):
    """Delete artist"""
    try:
        success = artist_service.delete_artist(artist_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete artist")
        return {"message": "Artist deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/artists", response_model=List[Artist])
async def list_artists(
    limit: int = Query(default=100, le=500),
    genre: Optional[Genre] = Query(default=None)
):
    """List artists with optional filtering"""
    try:
        artists = artist_service.list_artists(limit=limit, genre_filter=genre)
        return artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/artists/search/{search_term}", response_model=List[Artist])
async def search_artists(search_term: str, limit: int = Query(default=20, le=100)):
    """Search artists by name"""
    try:
        artists = artist_service.search_artists(search_term, limit=limit)
        return artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Stage endpoints
@router.post("/stages", response_model=Stage)
async def create_stage(stage_data: StageCreate):
    """Create a new stage"""
    try:
        stage = stage_service.create_stage(stage_data)
        if not stage:
            raise HTTPException(status_code=500, detail="Failed to create stage")
        return stage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stages/{stage_id}", response_model=Stage)
async def get_stage(stage_id: str):
    """Get stage by ID"""
    stage = stage_service.get_stage(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage

@router.put("/stages/{stage_id}", response_model=Stage)
async def update_stage(stage_id: str, stage_data: StageUpdate):
    """Update stage"""
    try:
        stage = stage_service.update_stage(stage_id, stage_data)
        if not stage:
            raise HTTPException(status_code=404, detail="Stage not found")
        return stage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/stages/{stage_id}")
async def delete_stage(stage_id: str):
    """Delete stage"""
    try:
        success = stage_service.delete_stage(stage_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete stage")
        return {"message": "Stage deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stages", response_model=List[Stage])
async def list_stages(stage_type: Optional[StageType] = Query(default=None)):
    """List stages with optional filtering"""
    try:
        stages = stage_service.list_stages(stage_type=stage_type)
        return stages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Performance endpoints
@router.post("/performances", response_model=Performance)
async def create_performance(performance_data: PerformanceCreate):
    """Create a new performance"""
    try:
        performance = performance_service.create_performance(performance_data)
        if not performance:
            raise HTTPException(status_code=500, detail="Failed to create performance")
        return performance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performances/{performance_id}", response_model=Performance)
async def get_performance(performance_id: str):
    """Get performance by ID"""
    performance = performance_service.get_performance(performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="Performance not found")
    return performance

@router.put("/performances/{performance_id}", response_model=Performance)
async def update_performance(performance_id: str, performance_data: PerformanceUpdate):
    """Update performance"""
    try:
        performance = performance_service.update_performance(performance_id, performance_data)
        if not performance:
            raise HTTPException(status_code=404, detail="Performance not found")
        return performance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/performances/{performance_id}")
async def delete_performance(performance_id: str):
    """Delete performance"""
    try:
        success = performance_service.delete_performance(performance_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete performance")
        return {"message": "Performance deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performances", response_model=List[Performance])
async def list_performances(
    artist_id: Optional[str] = Query(default=None),
    stage_id: Optional[str] = Query(default=None),
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
    vip_only: Optional[bool] = Query(default=None),
    limit: int = Query(default=100, le=500)
):
    """List performances with filtering options"""
    try:
        filters = PerformanceFilters(
            artist_id=artist_id,
            stage_id=stage_id,
            start_date=start_date,
            end_date=end_date,
            vip_only=vip_only
        )
        performances = performance_service.list_performances(filters, limit=limit)
        return performances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedule", response_model=PerformanceSchedule)
async def get_schedule(
    start_date: date = Query(..., description="Schedule start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Schedule end date (YYYY-MM-DD)")
):
    """Get complete festival schedule for date range"""
    try:
        # Convert dates to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        schedule = performance_service.get_schedule(start_datetime, end_datetime)
        if not schedule:
            raise HTTPException(status_code=500, detail="Failed to generate schedule")
        return schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performances/conflicts/{stage_id}")
async def check_scheduling_conflicts(
    stage_id: str,
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    exclude_performance_id: Optional[str] = Query(default=None)
):
    """Check for scheduling conflicts at a stage"""
    try:
        conflicts = performance_service.check_scheduling_conflicts(
            stage_id, start_time, end_time, exclude_performance_id
        )
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicts": conflicts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints
@router.get("/genres", response_model=List[str])
async def get_genres():
    """Get list of available music genres"""
    return [genre.value for genre in Genre]

@router.get("/stage-types", response_model=List[str])
async def get_stage_types():
    """Get list of available stage types"""
    return [stage_type.value for stage_type in StageType]

@router.get("/stats")
async def get_festival_stats():
    """Get festival statistics"""
    try:
        artists = artist_service.list_artists(limit=1000)
        stages = stage_service.list_stages()
        performances = performance_service.list_performances(limit=1000)
        
        return {
            "total_artists": len(artists),
            "total_stages": len(stages),
            "total_performances": len(performances),
            "genres": {genre.value: len([a for a in artists if genre in a.genres]) for genre in Genre},
            "stage_types": {st.value: len([s for s in stages if s.stage_type == st]) for st in StageType}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))