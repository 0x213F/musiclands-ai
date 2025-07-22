"""
Example usage of the Festival Management system
Run with: pipenv run python examples/festival_example.py
"""

import asyncio
import json
from datetime import datetime, timedelta
from services.festival_service import artist_service, stage_service, performance_service
from models.festival import (
    ArtistCreate, StageCreate, PerformanceCreate, 
    Genre, StageType, GPSCoordinate
)

async def create_sample_festival_data():
    """Create sample festival data"""
    
    print("🎵 Creating Sample Festival Data")
    print("=" * 50)
    
    # Create sample artists
    artists_data = [
        {
            "name": "Electric Dreams",
            "genres": [Genre.ELECTRONIC, Genre.HOUSE],
            "bio": "Electronic music duo from Berlin known for their energetic live performances",
            "popularity_score": 85
        },
        {
            "name": "Sunset Vibes",
            "genres": [Genre.INDIE, Genre.ALTERNATIVE],
            "bio": "Indie rock band with dreamy vocals and catchy melodies",
            "popularity_score": 70
        },
        {
            "name": "Bass Drop Kings",
            "genres": [Genre.DUBSTEP, Genre.TRAP],
            "bio": "High-energy dubstep collective that brings the party",
            "popularity_score": 90
        },
        {
            "name": "Folk Stories",
            "genres": [Genre.FOLK, Genre.COUNTRY],
            "bio": "Acoustic storytellers with heartfelt lyrics",
            "popularity_score": 60
        }
    ]
    
    print("Creating artists...")
    artists = []
    for artist_data in artists_data:
        artist = artist_service.create_artist(ArtistCreate(**artist_data))
        if artist:
            artists.append(artist)
            print(f"✅ Created artist: {artist.name}")
        else:
            print(f"❌ Failed to create artist: {artist_data['name']}")
    
    # Create sample stages
    stages_data = [
        {
            "name": "Main Stage",
            "stage_type": StageType.MAIN_STAGE,
            "location": GPSCoordinate(lat=40.7589, lng=-73.9851),  # Central Park coordinates
            "capacity": 10000,
            "description": "The main performance stage with state-of-the-art sound and lighting",
            "amenities": ["VIP viewing area", "Food vendors", "Merchandise booth"]
        },
        {
            "name": "Electronic Tent",
            "stage_type": StageType.TENT,
            "location": GPSCoordinate(lat=40.7614, lng=-73.9776),
            "capacity": 5000,
            "description": "Dedicated electronic music venue with immersive visuals",
            "amenities": ["Bar", "Lounge area", "DJ booth"]
        },
        {
            "name": "Acoustic Garden",
            "stage_type": StageType.OUTDOOR,
            "location": GPSCoordinate(lat=40.7505, lng=-73.9934),
            "capacity": 2000,
            "description": "Intimate outdoor setting perfect for acoustic performances",
            "amenities": ["Seating area", "Quiet zone", "Coffee stand"]
        },
        {
            "name": "Silent Disco",
            "stage_type": StageType.SILENT_DISCO,
            "location": GPSCoordinate(lat=40.7549, lng=-73.9840),
            "capacity": 1000,
            "description": "Wireless headphone dance party",
            "amenities": ["Headphone rental", "Multiple channels", "LED lighting"]
        }
    ]
    
    print("\nCreating stages...")
    stages = []
    for stage_data in stages_data:
        stage = stage_service.create_stage(StageCreate(**stage_data))
        if stage:
            stages.append(stage)
            print(f"✅ Created stage: {stage.name}")
        else:
            print(f"❌ Failed to create stage: {stage_data['name']}")
    
    # Create sample performances
    if artists and stages:
        base_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)  # Start at 2 PM
        
        performances_data = [
            {
                "artist_id": artists[0].artist_id,  # Electric Dreams
                "stage_id": stages[1].stage_id,     # Electronic Tent
                "start_time": base_time,
                "end_time": base_time + timedelta(hours=1, minutes=30),
                "title": "Electric Dreams Live Set",
                "description": "High-energy electronic set to kick off the festival"
            },
            {
                "artist_id": artists[1].artist_id,  # Sunset Vibes
                "stage_id": stages[2].stage_id,     # Acoustic Garden
                "start_time": base_time + timedelta(hours=1),
                "end_time": base_time + timedelta(hours=2, minutes=15),
                "title": "Acoustic Sunset Session",
                "description": "Intimate acoustic performance in the garden setting"
            },
            {
                "artist_id": artists[2].artist_id,  # Bass Drop Kings
                "stage_id": stages[0].stage_id,     # Main Stage
                "start_time": base_time + timedelta(hours=3),
                "end_time": base_time + timedelta(hours=4, minutes=30),
                "title": "Bass Drop Kings Headliner",
                "description": "Main stage headliner performance",
                "expected_attendance": 8000
            },
            {
                "artist_id": artists[3].artist_id,  # Folk Stories
                "stage_id": stages[3].stage_id,     # Silent Disco
                "start_time": base_time + timedelta(hours=2, minutes=30),
                "end_time": base_time + timedelta(hours=3, minutes=45),
                "title": "Storytelling Session",
                "description": "Unique folk storytelling in silent disco format"
            }
        ]
        
        print("\nCreating performances...")
        performances = []
        for perf_data in performances_data:
            performance = performance_service.create_performance(PerformanceCreate(**perf_data))
            if performance:
                performances.append(performance)
                artist_name = performance.artist.name if performance.artist else "Unknown"
                stage_name = performance.stage.name if performance.stage else "Unknown"
                print(f"✅ Created performance: {artist_name} at {stage_name}")
            else:
                print(f"❌ Failed to create performance")
        
        # Demonstrate schedule retrieval
        print("\n📅 Festival Schedule:")
        print("-" * 30)
        schedule_start = base_time.date()
        schedule_end = (base_time + timedelta(days=1)).date()
        
        schedule = performance_service.get_schedule(
            datetime.combine(schedule_start, datetime.min.time()),
            datetime.combine(schedule_end, datetime.max.time())
        )
        
        if schedule:
            for performance in schedule.performances:
                start_time = performance.start_time.strftime("%I:%M %p")
                end_time = performance.end_time.strftime("%I:%M %p")
                artist_name = performance.artist.name if performance.artist else "Unknown"
                stage_name = performance.stage.name if performance.stage else "Unknown"
                print(f"{start_time} - {end_time}: {artist_name} @ {stage_name}")
        
        # Check for conflicts
        print("\n⚠️  Checking for scheduling conflicts...")
        if performances:
            conflicts = performance_service.check_scheduling_conflicts(
                stages[0].stage_id,  # Main Stage
                base_time + timedelta(hours=2, minutes=45),
                base_time + timedelta(hours=4),
                exclude_performance_id=None
            )
            
            if conflicts:
                print(f"Found {len(conflicts)} scheduling conflicts on Main Stage")
                for conflict in conflicts:
                    artist_name = conflict.artist.name if conflict.artist else "Unknown"
                    print(f"  - Conflict with {artist_name} from {conflict.start_time} to {conflict.end_time}")
            else:
                print("✅ No scheduling conflicts found")
    
    print("\n" + "=" * 50)
    print("🎉 Sample festival data created successfully!")
    print(f"Created {len(artists)} artists, {len(stages)} stages, and {len(performances) if 'performances' in locals() else 0} performances")

async def main():
    """Main function"""
    await create_sample_festival_data()
    
    print("\n💡 API Usage:")
    print("Start the server: pipenv run python start.py")
    print("Check the API docs: http://localhost:8000/docs")
    print("Festival endpoints: http://localhost:8000/festival/")
    print("\nExample API calls:")
    print("- GET /festival/artists - List all artists")
    print("- GET /festival/stages - List all stages") 
    print("- GET /festival/performances - List all performances")
    print("- GET /festival/schedule?start_date=2024-01-15&end_date=2024-01-16 - Get festival schedule")

if __name__ == "__main__":
    asyncio.run(main())