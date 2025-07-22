# Festival Data Management System

This directory contains tools for manually managing festival data through JSON files and import scripts.

## 📁 Directory Structure

```
data_management/
├── import_all_data.py              # Master import script
├── manual_data_entry/              # Manual data entry folder
│   ├── stage_locations/            # Stage and venue data
│   │   ├── stage_locations.json    # Stage data JSON
│   │   └── import_stages.py        # Stage import script
│   ├── artists/                    # Artist and performer data
│   │   ├── artists.json            # Artist data JSON
│   │   └── import_artists.py       # Artist import script
│   └── performances/               # Performance schedule data
│       ├── performances.json       # Performance data JSON
│       └── import_performances.py  # Performance import script
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Import All Data (Recommended)
```bash
# Dry run (preview what will be imported)
pipenv run python data_management/import_all_data.py

# Actually import to database
pipenv run python data_management/import_all_data.py --live

# Import without confirmation prompt
pipenv run python data_management/import_all_data.py --live --yes
```

### 2. Import Individual Datasets
```bash
# Import stages
pipenv run python data_management/manual_data_entry/stage_locations/import_stages.py --live

# Import artists  
pipenv run python data_management/manual_data_entry/artists/import_artists.py --live

# Import performances (requires stages and artists to exist first)
pipenv run python data_management/manual_data_entry/performances/import_performances.py --live
```

## 📝 Data Files Overview

### Stage Locations (`stage_locations.json`)
Defines festival venues and stages with:
- **Location Data**: GPS coordinates, capacity, accessibility
- **Technical Specs**: Sound systems, lighting, backstage facilities  
- **Amenities**: Available services and features
- **Types**: Main stage, tent, outdoor, pavilion, silent disco, etc.

**Sample structure:**
```json
{
  "stages": [
    {
      "name": "Main Stage",
      "stage_type": "main_stage",
      "location": {"lat": 40.7589, "lng": -73.9851},
      "capacity": 15000,
      "description": "The main performance stage...",
      "amenities": ["VIP viewing area", "Food vendors"],
      "sound_system": "Meyer Sound LEO Family",
      "accessibility": "Wheelchair accessible"
    }
  ]
}
```

### Artists (`artists.json`)
Defines performers and artists with:
- **Basic Info**: Name, bio, genres, popularity score
- **Media**: Image URLs, website, social media links
- **Music**: Spotify URLs, genre classifications

**Sample structure:**
```json
{
  "artists": [
    {
      "name": "Electric Dreams",
      "genres": ["electronic", "house", "techno"],
      "bio": "Berlin-based electronic duo...",
      "popularity_score": 85,
      "spotify_url": "https://open.spotify.com/artist/...",
      "instagram": "@electricdreamsberlin"
    }
  ]
}
```

### Performances (`performances.json`)
Defines the performance schedule linking artists to stages:
- **Relationships**: Artist name and stage name (resolved to IDs during import)
- **Timing**: Start and end times with timezone support
- **Event Details**: Titles, descriptions, special notes
- **Audience Info**: Age restrictions, expected attendance, VIP status

**Sample structure:**
```json
{
  "performances": [
    {
      "artist_name": "Electric Dreams",
      "stage_name": "Electronic Tent",
      "start_time": "2024-07-20T21:00:00",
      "end_time": "2024-07-20T22:30:00", 
      "title": "Electric Dreams Live Set",
      "description": "High-energy electronic set...",
      "expected_attendance": 7500
    }
  ]
}
```

## 🛠 Import Scripts Features

### Dry Run Mode (Default)
- Validates JSON data without writing to database
- Shows what would be imported
- Identifies missing dependencies and errors
- Safe to run multiple times

### Live Mode (`--live` flag)
- Actually writes data to Firestore database
- Validates relationships (artist/stage existence)
- Handles errors gracefully
- Provides detailed import reports

### Smart Features
- **Dependency Resolution**: Performances script validates that artists and stages exist
- **Conflict Detection**: Identifies scheduling conflicts and missing data
- **Data Validation**: Validates JSON structure, required fields, and data types
- **Progress Reporting**: Detailed success/failure reporting with error descriptions
- **Safe Defaults**: Dry run mode prevents accidental imports

## 📊 Monitoring and Validation

After importing data, verify your import with:

```bash
# Start the API server
pipenv run python start.py

# Check import statistics
curl http://localhost:8000/festival/stats

# Browse the API documentation
open http://localhost:8000/docs
```

## 🔧 Modifying Data

### Adding New Stages
1. Edit `manual_data_entry/stage_locations/stage_locations.json`
2. Add new stage objects to the `stages` array
3. Run: `pipenv run python data_management/manual_data_entry/stage_locations/import_stages.py --live`

### Adding New Artists  
1. Edit `manual_data_entry/artists/artists.json`
2. Add new artist objects to the `artists` array
3. Ensure genres match the available Genre enum values
4. Run: `pipenv run python data_management/manual_data_entry/artists/import_artists.py --live`

### Adding New Performances
1. Edit `manual_data_entry/performances/performances.json`
2. Add new performance objects to the `performances` array
3. Ensure `artist_name` and `stage_name` match existing entries exactly
4. Use ISO 8601 datetime format for start_time and end_time
5. Run: `pipenv run python data_management/manual_data_entry/performances/import_performances.py --live`

## 🚨 Troubleshooting

### Common Issues

**"Artist not found in database"**
- Make sure to import artists before performances
- Check that artist names in performances.json match exactly

**"Stage not found in database"** 
- Make sure to import stages before performances
- Check that stage names in performances.json match exactly

**"Invalid datetime format"**
- Use ISO 8601 format: `2024-07-20T21:00:00`
- Ensure timezone consistency

**"Firebase connection error"**
- Check your `FIREBASE_JSON_BASE64` environment variable
- Verify Firestore database is set up and accessible

### Debugging Steps

1. **Run dry mode first**: Always test with dry run before live import
2. **Check individual scripts**: Run stage and artist imports individually
3. **Validate JSON**: Use JSON validators to check file syntax
4. **Check logs**: Import scripts provide detailed error messages
5. **Verify dependencies**: Ensure stages and artists exist before importing performances

## 💡 Best Practices

1. **Always dry run first**: Test imports before writing to database
2. **Import in order**: Stages → Artists → Performances  
3. **Backup data**: Keep JSON files in version control
4. **Validate relationships**: Ensure artist/stage names match exactly
5. **Test incrementally**: Import small batches when testing changes
6. **Monitor results**: Check API endpoints after imports to verify data

## 🎯 Integration with Location Intelligence

The imported data integrates seamlessly with the Location Intelligence system:
- **Stage GPS coordinates** enable location-based recommendations
- **Performance schedules** power "what's happening now" queries  
- **Artist genres and popularity** enhance music discovery
- **Venue amenities and capacity** inform crowd management suggestions

Your festival data becomes the foundation for intelligent, context-aware AI responses!