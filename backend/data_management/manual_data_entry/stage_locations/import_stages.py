#!/usr/bin/env python3
"""
Stage Locations Import Script
Imports stage location data from JSON file into Firestore database
"""

import os
import sys
import json
from pathlib import Path

# Add the backend root to Python path to import our modules
backend_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(backend_root))

from models.festival import StageCreate, GPSCoordinate, StageType
from services.festival_service import stage_service

def load_stage_data(json_file_path: str):
    """Load stage data from JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return data.get('stages', [])
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return []

def convert_stage_type(stage_type_str: str) -> StageType:
    """Convert string to StageType enum"""
    try:
        return StageType(stage_type_str)
    except ValueError:
        print(f"⚠️  Unknown stage type: {stage_type_str}, defaulting to 'outdoor'")
        return StageType.OUTDOOR

def import_stages(json_file_path: str, dry_run: bool = False):
    """Import stages from JSON file to database"""
    
    print("🎪 Stage Locations Import Script")
    print("=" * 50)
    
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return False
    
    print(f"📂 Loading data from: {json_file_path}")
    
    # Load stage data
    stage_data_list = load_stage_data(json_file_path)
    
    if not stage_data_list:
        print("❌ No stage data found in JSON file")
        return False
    
    print(f"📊 Found {len(stage_data_list)} stages to import")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No data will be written to database")
        print("-" * 50)
    else:
        print(f"\n💾 LIVE IMPORT MODE - Data will be written to database")
        print("-" * 50)
    
    success_count = 0
    error_count = 0
    
    for i, stage_data in enumerate(stage_data_list, 1):
        try:
            print(f"\n{i}. Processing: {stage_data.get('name', 'Unknown Stage')}")
            
            # Validate required fields
            if not stage_data.get('name'):
                print(f"   ❌ Skipping - missing name")
                error_count += 1
                continue
            
            if not stage_data.get('location'):
                print(f"   ❌ Skipping - missing location data")
                error_count += 1
                continue
            
            # Create GPS coordinate object
            location_data = stage_data['location']
            gps_coord = GPSCoordinate(
                lat=location_data['lat'],
                lng=location_data['lng'],
                altitude=location_data.get('altitude'),
                accuracy=location_data.get('accuracy')
            )
            
            # Convert stage type
            stage_type = convert_stage_type(stage_data.get('stage_type', 'outdoor'))
            
            # Create stage create object
            stage_create = StageCreate(
                name=stage_data['name'],
                stage_type=stage_type,
                location=gps_coord,
                capacity=stage_data.get('capacity'),
                description=stage_data.get('description'),
                amenities=stage_data.get('amenities', []),
                accessibility=stage_data.get('accessibility'),
                sound_system=stage_data.get('sound_system'),
                lighting=stage_data.get('lighting'),
                backstage_facilities=stage_data.get('backstage_facilities')
            )
            
            if dry_run:
                print(f"   ✅ Would create stage: {stage_create.name}")
                print(f"      Type: {stage_type.value}")
                print(f"      Location: {gps_coord.lat}, {gps_coord.lng}")
                print(f"      Capacity: {stage_create.capacity or 'Not specified'}")
                success_count += 1
            else:
                # Actually create the stage
                created_stage = stage_service.create_stage(stage_create)
                
                if created_stage:
                    print(f"   ✅ Created stage: {created_stage.name}")
                    print(f"      Stage ID: {created_stage.stage_id}")
                    print(f"      Type: {created_stage.stage_type.value}")
                    print(f"      Location: {created_stage.location.lat}, {created_stage.location.lng}")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to create stage in database")
                    error_count += 1
                    
        except Exception as e:
            print(f"   ❌ Error processing stage: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 IMPORT SUMMARY")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {len(stage_data_list)}")
    
    if dry_run:
        print("\n💡 This was a dry run. To actually import data, run:")
        print("   pipenv run python data_management/manual_data_entry/stage_locations/import_stages.py --live")
    else:
        print(f"\n🎉 Import completed! {success_count} stages added to database.")
    
    return success_count > 0

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import stage locations from JSON to database')
    parser.add_argument('--live', action='store_true', help='Actually import to database (default is dry run)')
    parser.add_argument('--file', default=None, help='Path to JSON file (default: stage_locations.json in same directory)')
    
    args = parser.parse_args()
    
    # Determine JSON file path
    if args.file:
        json_file_path = args.file
    else:
        # Default to stage_locations.json in same directory as this script
        script_dir = Path(__file__).parent
        json_file_path = script_dir / 'stage_locations.json'
    
    # Run import
    dry_run = not args.live
    success = import_stages(str(json_file_path), dry_run=dry_run)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()