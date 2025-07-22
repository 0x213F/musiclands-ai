#!/usr/bin/env python3
"""
Performances Import Script
Imports performance data from JSON file into Firestore database
Requires artists and stages to already exist in the database
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the backend root to Python path to import our modules
backend_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(backend_root))

from models.festival import PerformanceCreate
from services.festival_service import performance_service, artist_service, stage_service

def load_performance_data(json_file_path: str):
    """Load performance data from JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return data.get('performances', [])
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return []

def find_artist_by_name(artist_name: str):
    """Find artist ID by name"""
    artists = artist_service.list_artists(limit=500)
    for artist in artists:
        if artist.name == artist_name:
            return artist.artist_id
    return None

def find_stage_by_name(stage_name: str):
    """Find stage ID by name"""
    stages = stage_service.list_stages()
    for stage in stages:
        if stage.name == stage_name:
            return stage.stage_id
    return None

def import_performances(json_file_path: str, dry_run: bool = False):
    """Import performances from JSON file to database"""
    
    print("🎭 Performances Import Script")
    print("=" * 50)
    
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return False
    
    print(f"📂 Loading data from: {json_file_path}")
    
    # Load performance data
    performance_data_list = load_performance_data(json_file_path)
    
    if not performance_data_list:
        print("❌ No performance data found in JSON file")
        return False
    
    print(f"📊 Found {len(performance_data_list)} performances to import")
    
    # Pre-load artists and stages for lookup
    print("🔍 Loading existing artists and stages for lookup...")
    artists = artist_service.list_artists(limit=500)
    stages = stage_service.list_stages()
    
    artist_lookup = {artist.name: artist.artist_id for artist in artists}
    stage_lookup = {stage.name: stage.stage_id for stage in stages}
    
    print(f"   Found {len(artist_lookup)} artists and {len(stage_lookup)} stages in database")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No data will be written to database")
        print("-" * 50)
    else:
        print(f"\n💾 LIVE IMPORT MODE - Data will be written to database")
        print("-" * 50)
    
    success_count = 0
    error_count = 0
    missing_artists = set()
    missing_stages = set()
    
    for i, perf_data in enumerate(performance_data_list, 1):
        try:
            print(f"\n{i}. Processing: {perf_data.get('title', 'Unknown Performance')}")
            
            # Validate required fields
            artist_name = perf_data.get('artist_name')
            stage_name = perf_data.get('stage_name')
            start_time = perf_data.get('start_time')
            end_time = perf_data.get('end_time')
            
            if not all([artist_name, stage_name, start_time, end_time]):
                print(f"   ❌ Skipping - missing required fields")
                error_count += 1
                continue
            
            # Find artist and stage IDs
            artist_id = artist_lookup.get(artist_name)
            stage_id = stage_lookup.get(stage_name)
            
            if not artist_id:
                print(f"   ❌ Artist '{artist_name}' not found in database")
                missing_artists.add(artist_name)
                error_count += 1
                continue
            
            if not stage_id:
                print(f"   ❌ Stage '{stage_name}' not found in database")
                missing_stages.add(stage_name)
                error_count += 1
                continue
            
            # Parse datetime strings
            try:
                start_datetime = datetime.fromisoformat(start_time)
                end_datetime = datetime.fromisoformat(end_time)
            except ValueError as e:
                print(f"   ❌ Invalid datetime format: {e}")
                error_count += 1
                continue
            
            # Create performance create object
            performance_create = PerformanceCreate(
                artist_id=artist_id,
                stage_id=stage_id,
                start_time=start_datetime,
                end_time=end_datetime,
                title=perf_data.get('title'),
                description=perf_data.get('description'),
                set_type=perf_data.get('set_type'),
                special_notes=perf_data.get('special_notes'),
                ticket_required=perf_data.get('ticket_required', False),
                vip_only=perf_data.get('vip_only', False),
                age_restriction=perf_data.get('age_restriction'),
                expected_attendance=perf_data.get('expected_attendance')
            )
            
            if dry_run:
                print(f"   ✅ Would create performance: {performance_create.title}")
                print(f"      Artist: {artist_name} (ID: {artist_id})")
                print(f"      Stage: {stage_name} (ID: {stage_id})")
                print(f"      Time: {start_datetime.strftime('%m/%d %I:%M %p')} - {end_datetime.strftime('%I:%M %p')}")
                print(f"      Expected attendance: {performance_create.expected_attendance or 'Not specified'}")
                success_count += 1
            else:
                # Actually create the performance
                created_performance = performance_service.create_performance(performance_create)
                
                if created_performance:
                    print(f"   ✅ Created performance: {created_performance.title}")
                    print(f"      Performance ID: {created_performance.performance_id}")
                    print(f"      Artist: {created_performance.artist.name if created_performance.artist else 'Unknown'}")
                    print(f"      Stage: {created_performance.stage.name if created_performance.stage else 'Unknown'}")
                    print(f"      Time: {created_performance.start_time.strftime('%m/%d %I:%M %p')} - {created_performance.end_time.strftime('%I:%M %p')}")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to create performance in database")
                    error_count += 1
                    
        except Exception as e:
            print(f"   ❌ Error processing performance: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 IMPORT SUMMARY")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {len(performance_data_list)}")
    
    if missing_artists:
        print(f"\n⚠️  MISSING ARTISTS ({len(missing_artists)}):")
        for artist in sorted(missing_artists):
            print(f"   - {artist}")
        print("   💡 Import artists first using: pipenv run python data_management/manual_data_entry/artists/import_artists.py --live")
    
    if missing_stages:
        print(f"\n⚠️  MISSING STAGES ({len(missing_stages)}):")
        for stage in sorted(missing_stages):
            print(f"   - {stage}")
        print("   💡 Import stages first using: pipenv run python data_management/manual_data_entry/stage_locations/import_stages.py --live")
    
    if dry_run:
        print("\n💡 This was a dry run. To actually import data, run:")
        print("   pipenv run python data_management/manual_data_entry/performances/import_performances.py --live")
    else:
        print(f"\n🎉 Import completed! {success_count} performances added to database.")
    
    return success_count > 0

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import performances from JSON to database')
    parser.add_argument('--live', action='store_true', help='Actually import to database (default is dry run)')
    parser.add_argument('--file', default=None, help='Path to JSON file (default: performances.json in same directory)')
    
    args = parser.parse_args()
    
    # Determine JSON file path
    if args.file:
        json_file_path = args.file
    else:
        # Default to performances.json in same directory as this script
        script_dir = Path(__file__).parent
        json_file_path = script_dir / 'performances.json'
    
    # Run import
    dry_run = not args.live
    success = import_performances(str(json_file_path), dry_run=dry_run)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()