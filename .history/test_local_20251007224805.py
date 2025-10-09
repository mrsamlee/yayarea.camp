#!/usr/bin/env python3
"""
Local testing script for the campsite search and web interface.
This simulates what GitHub Actions will do.
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("🏕️ Testing Bay Area Campsite Search Locally")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("new_main.py").exists():
        print("❌ Error: new_main.py not found. Make sure you're in the project directory.")
        return
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt not found.")
        return
    
    print("1. Installing dependencies...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return
    
    print("\n2. Checking for existing results...")
    if Path("results.json").exists():
        print("✅ Found existing results.json - using saved results")
        print("   (Skipping search to save time)")
    else:
        print("Running campsite search...")
        try:
            # Import and run the search function
            from new_main import run_search_and_save
            run_search_and_save()
            print("✅ Search completed successfully")
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return
    
    # Check if results.json was created
    if not Path("results.json").exists():
        print("❌ Error: results.json not created")
        return
    
    print("\n3. Checking web files...")
    required_files = ["index.html", "results.json"]
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return
    
    # Display results summary
    try:
        import json
        with open("results.json", "r") as f:
            data = json.load(f)
        print(f"\n📊 Results Summary:")
        print(f"   Total campsites: {data['total_results']}")
        print(f"   Last updated: {data['last_updated']}")
        print(f"   Search criteria: {data['search_criteria']['consecutive_nights']} nights, weekends only: {data['search_criteria']['weekends_only']}")
        
        if data['results']:
            # Show unique facilities
            facilities = set()
            for result in data['results']:
                facilities.add(f"{result['recreation_area']} - {result['facility_name']}")
            print(f"   Unique facilities: {len(facilities)}")
            
            # Show closest sites
            sorted_results = sorted(data['results'], key=lambda x: x['miles'])
            closest_sites = sorted_results[:3]
            print(f"   Closest sites:")
            for i, site in enumerate(closest_sites, 1):
                print(f"     {i}. {site['recreation_area']} ({site['miles']} miles)")
    except Exception as e:
        print(f"   Could not parse results summary: {e}")
    
    print("\n4. Starting local server...")
    try:
        print("   Starting HTTP server to avoid CORS issues...")
        print("   The server will open automatically in your browser")
        print("   Press Ctrl+C to stop the server when done testing")
        print("")
        
        # Import and run the local server
        from serve_local import main as serve_main
        serve_main()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print(f"   You can manually open: {Path('index.html').absolute()}")
        print(f"   Note: Direct file opening may show 'loading' due to CORS restrictions")
    
    print("\n🎉 Local test completed!")
    print("\nNext steps:")
    print("1. Verify the web interface shows your results correctly")
    print("2. Upload all files to your GitHub repository")
    print("3. Enable GitHub Pages and Actions as described in README.md")
    print("4. Your site will be live at: https://yourusername.github.io/your-repo-name")

if __name__ == "__main__":
    main()
