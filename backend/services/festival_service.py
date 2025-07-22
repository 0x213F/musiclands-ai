import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from services.firebase_client import firestore_client
from models.festival import (
    Artist, ArtistCreate, ArtistUpdate,
    Stage, StageCreate, StageUpdate,
    Performance, PerformanceCreate, PerformanceUpdate,
    PerformanceFilters, PerformanceSchedule, Genre, StageType
)
from google.cloud.firestore_v1.base_query import FieldFilter

class ArtistService:
    """Service for managing artists in Firestore"""
    
    def __init__(self):
        self.collection_name = "artists"
        self.db = firestore_client.db

    def create_artist(self, artist_data: ArtistCreate) -> Optional[Artist]:
        """Create a new artist"""
        try:
            if not firestore_client.is_available():
                return None

            artist_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            artist_dict = {
                "artist_id": artist_id,
                **artist_data.dict(),
                "created_at": now,
                "updated_at": now
            }

            self.db.collection(self.collection_name).document(artist_id).set(artist_dict)
            return Artist(**artist_dict)

        except Exception as e:
            print(f"Error creating artist: {e}")
            return None

    def get_artist(self, artist_id: str) -> Optional[Artist]:
        """Get artist by ID"""
        try:
            if not firestore_client.is_available():
                return None

            artist_doc = self.db.collection(self.collection_name).document(artist_id).get()
            
            if artist_doc.exists:
                return Artist(**artist_doc.to_dict())
            return None

        except Exception as e:
            print(f"Error getting artist: {e}")
            return None

    def update_artist(self, artist_id: str, artist_data: ArtistUpdate) -> Optional[Artist]:
        """Update artist"""
        try:
            if not firestore_client.is_available():
                return None

            artist_ref = self.db.collection(self.collection_name).document(artist_id)
            
            if not artist_ref.get().exists:
                return None

            update_data = {k: v for k, v in artist_data.dict().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()

            artist_ref.update(update_data)
            return self.get_artist(artist_id)

        except Exception as e:
            print(f"Error updating artist: {e}")
            return None

    def delete_artist(self, artist_id: str) -> bool:
        """Delete artist"""
        try:
            if not firestore_client.is_available():
                return False

            self.db.collection(self.collection_name).document(artist_id).delete()
            return True

        except Exception as e:
            print(f"Error deleting artist: {e}")
            return False

    def list_artists(self, limit: int = 100, genre_filter: Optional[Genre] = None) -> List[Artist]:
        """List artists with optional filtering"""
        try:
            if not firestore_client.is_available():
                return []

            query = self.db.collection(self.collection_name).limit(limit)
            
            if genre_filter:
                query = query.where(filter=FieldFilter("genres", "array_contains", genre_filter))

            docs = query.stream()
            return [Artist(**doc.to_dict()) for doc in docs]

        except Exception as e:
            print(f"Error listing artists: {e}")
            return []

    def search_artists(self, search_term: str, limit: int = 20) -> List[Artist]:
        """Search artists by name (basic implementation)"""
        try:
            if not firestore_client.is_available():
                return []

            # Simple name-based search - in production, consider using Algolia or Elasticsearch
            artists = self.list_artists(limit=200)
            search_term_lower = search_term.lower()
            
            matching_artists = [
                artist for artist in artists 
                if search_term_lower in artist.name.lower()
            ]
            
            return matching_artists[:limit]

        except Exception as e:
            print(f"Error searching artists: {e}")
            return []


class StageService:
    """Service for managing stages in Firestore"""
    
    def __init__(self):
        self.collection_name = "stages"
        self.db = firestore_client.db

    def create_stage(self, stage_data: StageCreate) -> Optional[Stage]:
        """Create a new stage"""
        try:
            if not firestore_client.is_available():
                return None

            stage_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            stage_dict = {
                "stage_id": stage_id,
                **stage_data.dict(),
                "created_at": now,
                "updated_at": now
            }

            self.db.collection(self.collection_name).document(stage_id).set(stage_dict)
            return Stage(**stage_dict)

        except Exception as e:
            print(f"Error creating stage: {e}")
            return None

    def get_stage(self, stage_id: str) -> Optional[Stage]:
        """Get stage by ID"""
        try:
            if not firestore_client.is_available():
                return None

            stage_doc = self.db.collection(self.collection_name).document(stage_id).get()
            
            if stage_doc.exists:
                return Stage(**stage_doc.to_dict())
            return None

        except Exception as e:
            print(f"Error getting stage: {e}")
            return None

    def update_stage(self, stage_id: str, stage_data: StageUpdate) -> Optional[Stage]:
        """Update stage"""
        try:
            if not firestore_client.is_available():
                return None

            stage_ref = self.db.collection(self.collection_name).document(stage_id)
            
            if not stage_ref.get().exists:
                return None

            update_data = {k: v for k, v in stage_data.dict().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()

            stage_ref.update(update_data)
            return self.get_stage(stage_id)

        except Exception as e:
            print(f"Error updating stage: {e}")
            return None

    def delete_stage(self, stage_id: str) -> bool:
        """Delete stage"""
        try:
            if not firestore_client.is_available():
                return False

            self.db.collection(self.collection_name).document(stage_id).delete()
            return True

        except Exception as e:
            print(f"Error deleting stage: {e}")
            return False

    def list_stages(self, stage_type: Optional[StageType] = None) -> List[Stage]:
        """List stages with optional filtering"""
        try:
            if not firestore_client.is_available():
                return []

            query = self.db.collection(self.collection_name)
            
            if stage_type:
                query = query.where(filter=FieldFilter("stage_type", "==", stage_type))

            docs = query.stream()
            return [Stage(**doc.to_dict()) for doc in docs]

        except Exception as e:
            print(f"Error listing stages: {e}")
            return []


class PerformanceService:
    """Service for managing performances in Firestore"""
    
    def __init__(self):
        self.collection_name = "performances"
        self.db = firestore_client.db
        self.artist_service = ArtistService()
        self.stage_service = StageService()

    def create_performance(self, performance_data: PerformanceCreate) -> Optional[Performance]:
        """Create a new performance"""
        try:
            if not firestore_client.is_available():
                return None

            # Validate that artist and stage exist
            artist = self.artist_service.get_artist(performance_data.artist_id)
            if not artist:
                raise ValueError(f"Artist with ID {performance_data.artist_id} not found")
                
            stage = self.stage_service.get_stage(performance_data.stage_id)
            if not stage:
                raise ValueError(f"Stage with ID {performance_data.stage_id} not found")

            performance_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            performance_dict = {
                "performance_id": performance_id,
                **performance_data.dict(),
                "created_at": now,
                "updated_at": now
            }

            self.db.collection(self.collection_name).document(performance_id).set(performance_dict)
            
            # Return with related data
            performance = Performance(**performance_dict)
            performance.artist = artist
            performance.stage = stage
            return performance

        except Exception as e:
            print(f"Error creating performance: {e}")
            return None

    def get_performance(self, performance_id: str, include_relations: bool = True) -> Optional[Performance]:
        """Get performance by ID"""
        try:
            if not firestore_client.is_available():
                return None

            performance_doc = self.db.collection(self.collection_name).document(performance_id).get()
            
            if not performance_doc.exists:
                return None
                
            performance_data = performance_doc.to_dict()
            performance = Performance(**performance_data)
            
            if include_relations:
                performance.artist = self.artist_service.get_artist(performance.artist_id)
                performance.stage = self.stage_service.get_stage(performance.stage_id)
            
            return performance

        except Exception as e:
            print(f"Error getting performance: {e}")
            return None

    def update_performance(self, performance_id: str, performance_data: PerformanceUpdate) -> Optional[Performance]:
        """Update performance"""
        try:
            if not firestore_client.is_available():
                return None

            performance_ref = self.db.collection(self.collection_name).document(performance_id)
            
            if not performance_ref.get().exists:
                return None

            update_data = {k: v for k, v in performance_data.dict().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()

            # Validate artist and stage if they're being updated
            if "artist_id" in update_data and not self.artist_service.get_artist(update_data["artist_id"]):
                raise ValueError(f"Artist with ID {update_data['artist_id']} not found")
                
            if "stage_id" in update_data and not self.stage_service.get_stage(update_data["stage_id"]):
                raise ValueError(f"Stage with ID {update_data['stage_id']} not found")

            performance_ref.update(update_data)
            return self.get_performance(performance_id)

        except Exception as e:
            print(f"Error updating performance: {e}")
            return None

    def delete_performance(self, performance_id: str) -> bool:
        """Delete performance"""
        try:
            if not firestore_client.is_available():
                return False

            self.db.collection(self.collection_name).document(performance_id).delete()
            return True

        except Exception as e:
            print(f"Error deleting performance: {e}")
            return False

    def list_performances(self, filters: Optional[PerformanceFilters] = None, limit: int = 100) -> List[Performance]:
        """List performances with optional filtering"""
        try:
            if not firestore_client.is_available():
                return []

            query = self.db.collection(self.collection_name)
            
            if filters:
                if filters.artist_id:
                    query = query.where(filter=FieldFilter("artist_id", "==", filters.artist_id))
                if filters.stage_id:
                    query = query.where(filter=FieldFilter("stage_id", "==", filters.stage_id))
                if filters.start_date:
                    query = query.where(filter=FieldFilter("start_time", ">=", filters.start_date))
                if filters.end_date:
                    query = query.where(filter=FieldFilter("end_time", "<=", filters.end_date))
                if filters.vip_only is not None:
                    query = query.where(filter=FieldFilter("vip_only", "==", filters.vip_only))

            query = query.order_by("start_time").limit(limit)
            docs = query.stream()
            
            performances = []
            for doc in docs:
                performance = Performance(**doc.to_dict())
                # Load related data
                performance.artist = self.artist_service.get_artist(performance.artist_id)
                performance.stage = self.stage_service.get_stage(performance.stage_id)
                performances.append(performance)
            
            return performances

        except Exception as e:
            print(f"Error listing performances: {e}")
            return []

    def get_schedule(self, start_date: datetime, end_date: datetime) -> Optional[PerformanceSchedule]:
        """Get complete performance schedule for date range"""
        try:
            filters = PerformanceFilters(start_date=start_date, end_date=end_date)
            performances = self.list_performances(filters, limit=1000)
            
            # Get unique artists and stages
            artist_ids = list(set(p.artist_id for p in performances))
            stage_ids = list(set(p.stage_id for p in performances))
            
            artists = [self.artist_service.get_artist(aid) for aid in artist_ids]
            stages = [self.stage_service.get_stage(sid) for sid in stage_ids]
            
            # Filter out None values
            artists = [a for a in artists if a is not None]
            stages = [s for s in stages if s is not None]
            
            return PerformanceSchedule(
                performances=performances,
                total_count=len(performances),
                date_range={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                stages=stages,
                artists=artists
            )

        except Exception as e:
            print(f"Error getting schedule: {e}")
            return None

    def check_scheduling_conflicts(self, stage_id: str, start_time: datetime, end_time: datetime, exclude_performance_id: Optional[str] = None) -> List[Performance]:
        """Check for scheduling conflicts at a stage"""
        try:
            if not firestore_client.is_available():
                return []

            # Get all performances at this stage that overlap with the time range
            query = self.db.collection(self.collection_name).where(filter=FieldFilter("stage_id", "==", stage_id))
            docs = query.stream()
            
            conflicts = []
            for doc in docs:
                performance_data = doc.to_dict()
                performance = Performance(**performance_data)
                
                # Skip the performance we're updating
                if exclude_performance_id and performance.performance_id == exclude_performance_id:
                    continue
                
                # Check for time overlap
                if (start_time < performance.end_time and end_time > performance.start_time):
                    # Load related data
                    performance.artist = self.artist_service.get_artist(performance.artist_id)
                    performance.stage = self.stage_service.get_stage(performance.stage_id)
                    conflicts.append(performance)
            
            return conflicts

        except Exception as e:
            print(f"Error checking conflicts: {e}")
            return []


# Global service instances
artist_service = ArtistService()
stage_service = StageService()
performance_service = PerformanceService()