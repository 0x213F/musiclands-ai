#!/usr/bin/env python3
"""
Artists Import Script
Imports artist data from JSON file into Firestore database
"""

import os
import sys
import json
from pathlib import Path

# Add the backend root to Python path to import our modules
backend_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(backend_root))

from models.festival import ArtistCreate, Genre
from services.festival_service import artist_service

def load_artist_data(json_file_path: str):
    """Load artist data from JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return data.get('artists', [])
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return []

def convert_genres(genre_strings: list) -> list:
    """Convert genre strings to Genre enums"""
    genres = []
    for genre_str in genre_strings:
        try:
            # Convert string to Genre enum
            genre = Genre(genre_str.replace('-', '_'))  # Handle hyphenated genres
            genres.append(genre)
        except ValueError:
            print(f"⚠️  Unknown genre: {genre_str}, skipping")
    return genres

def import_artists(json_file_path: str, dry_run: bool = False):
    """Import artists from JSON file to database"""
    
    print("🎤 Artists Import Script")
    print("=" * 50)
    
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return False
    
    print(f"📂 Loading data from: {json_file_path}")
    
    # Load artist data
    artist_data_list = load_artist_data(json_file_path)
    
    if not artist_data_list:
        print("❌ No artist data found in JSON file")
        return False
    
    print(f"📊 Found {len(artist_data_list)} artists to import")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No data will be written to database")
        print("-" * 50)
    else:
        print(f"\n💾 LIVE IMPORT MODE - Data will be written to database")
        print("-" * 50)
    
    success_count = 0
    error_count = 0
    
    for i, artist_data in enumerate(artist_data_list, 1):
        try:
            print(f"\n{i}. Processing: {artist_data.get('name', 'Unknown Artist')}")
            
            # Validate required fields
            if not artist_data.get('name'):
                print(f"   ❌ Skipping - missing name")
                error_count += 1
                continue
            
            # Convert genres
            genre_strings = artist_data.get('genres', [])
            genres = convert_genres(genre_strings)
            
            if not genres and genre_strings:
                print(f"   ⚠️  No valid genres found from: {genre_strings}")
            
            # Create artist create object
            artist_create = ArtistCreate(
                name=artist_data['name'],
                genres=genres,
                bio=artist_data.get('bio'),
                image_url=artist_data.get('image_url'),
                website=artist_data.get('website'),
                spotify_url=artist_data.get('spotify_url'),
                instagram=artist_data.get('instagram'),
                twitter=artist_data.get('twitter'),
                popularity_score=artist_data.get('popularity_score')
            )
            
            if dry_run:
                print(f"   ✅ Would create artist: {artist_create.name}")
                print(f"      Genres: {[g.value for g in genres]}")
                print(f"      Popularity: {artist_create.popularity_score or 'Not specified'}")
                print(f"      Bio: {(artist_create.bio or '')[:100]}{'...' if artist_create.bio and len(artist_create.bio) > 100 else ''}")
                success_count += 1
            else:
                # Actually create the artist
                created_artist = artist_service.create_artist(artist_create)
                
                if created_artist:
                    print(f"   ✅ Created artist: {created_artist.name}")
                    print(f"      Artist ID: {created_artist.artist_id}")
                    print(f"      Genres: {[g.value for g in created_artist.genres]}")
                    print(f"      Popularity: {created_artist.popularity_score or 'Not specified'}")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to create artist in database")
                    error_count += 1
                    
        except Exception as e:
            print(f"   ❌ Error processing artist: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 IMPORT SUMMARY")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {len(artist_data_list)}")
    
    if dry_run:
        print("\n💡 This was a dry run. To actually import data, run:")
        print("   pipenv run python data_management/manual_data_entry/artists/import_artists.py --live")
    else:
        print(f"\n🎉 Import completed! {success_count} artists added to database.")
    
    return success_count > 0

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import artists from JSON to database')
    parser.add_argument('--live', action='store_true', help='Actually import to database (default is dry run)')
    parser.add_argument('--file', default=None, help='Path to JSON file (default: artists.json in same directory)')
    
    args = parser.parse_args()
    
    # Determine JSON file path
    if args.file:
        json_file_path = args.file
    else:
        # Default to artists.json in same directory as this script
        script_dir = Path(__file__).parent
        json_file_path = script_dir / 'artists.json'
    
    # Run import
    dry_run = not args.live
    success = import_artists(str(json_file_path), dry_run=dry_run)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()