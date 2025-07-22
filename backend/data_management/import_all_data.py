#!/usr/bin/env python3
"""
Master Import Script
Imports all festival data from JSON files into Firestore database
Handles proper import order and dependency management
"""

import os
import sys
import subprocess
from pathlib import Path

def run_import_script(script_path: str, live_mode: bool = False):
    """Run an import script and return success status"""
    try:
        cmd = ["python", str(script_path)]
        if live_mode:
            cmd.append("--live")
        
        print(f"🚀 Running: {script_path}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print(f"✅ Success: {script_path}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed: {script_path}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Exception running {script_path}: {e}")
        return False

def import_all_data(live_mode: bool = False, skip_confirmation: bool = False):
    """Import all festival data with proper dependency order"""
    
    print("🎪 Master Festival Data Import")
    print("=" * 60)
    
    if live_mode and not skip_confirmation:
        print("⚠️  LIVE MODE - This will write data to the database!")
        response = input("Are you sure you want to proceed? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Import cancelled.")
            return False
    elif not live_mode:
        print("🔍 DRY RUN MODE - No data will be written to database")
    
    print("-" * 60)
    
    # Define import order (stages and artists first, then performances)
    import_scripts = [
        {
            "name": "Stage Locations",
            "script": "manual_data_entry/stage_locations/import_stages.py",
            "description": "Import festival stages and venue locations"
        },
        {
            "name": "Artists",
            "script": "manual_data_entry/artists/import_artists.py",
            "description": "Import artist and performer information"
        },
        {
            "name": "Performances",
            "script": "manual_data_entry/performances/import_performances.py",
            "description": "Import performance schedule (requires artists and stages)"
        }
    ]
    
    success_count = 0
    total_count = len(import_scripts)
    
    for i, import_item in enumerate(import_scripts, 1):
        print(f"\n📂 STEP {i}/{total_count}: {import_item['name']}")
        print(f"   {import_item['description']}")
        print("-" * 40)
        
        script_path = Path(__file__).parent / import_item['script']
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            continue
        
        success = run_import_script(script_path, live_mode)
        if success:
            success_count += 1
        else:
            print(f"\n⚠️  Import failed for {import_item['name']}")
            if i < total_count:
                response = input("Continue with remaining imports? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    break
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 MASTER IMPORT SUMMARY")
    print(f"✅ Successful imports: {success_count}/{total_count}")
    print(f"❌ Failed imports: {total_count - success_count}")
    
    if success_count == total_count:
        print("\n🎉 ALL IMPORTS COMPLETED SUCCESSFULLY!")
        if live_mode:
            print("📈 Your festival database is ready!")
            print("\n💡 Next steps:")
            print("   1. Start the API server: pipenv run python start.py")
            print("   2. Check the data: http://localhost:8000/festival/stats")
            print("   3. Browse the API docs: http://localhost:8000/docs")
        else:
            print("\n💡 This was a dry run. To actually import data, run:")
            print("   pipenv run python data_management/import_all_data.py --live")
    else:
        print("\n⚠️  Some imports failed. Check the output above for details.")
        print("💡 You may need to:")
        print("   1. Check your Firestore connection (FIREBASE_JSON_BASE64 env var)")
        print("   2. Review the JSON data files for errors")
        print("   3. Run individual import scripts for debugging")
    
    return success_count == total_count

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import all festival data from JSON files to database')
    parser.add_argument('--live', action='store_true', help='Actually import to database (default is dry run)')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt in live mode')
    
    args = parser.parse_args()
    
    # Run import
    success = import_all_data(live_mode=args.live, skip_confirmation=args.yes)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()