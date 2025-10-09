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
    
    print("\n2. Running campsite search...")
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
    
    print("\n4. Opening web interface...")
    try:
        # Get absolute path to index.html
        html_path = Path("index.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print(f"✅ Web interface opened in browser")
        print(f"   File: {html_path}")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"   Please manually open: {Path('index.html').absolute()}")
    
    print("\n🎉 Local test completed!")
    print("\nNext steps:")
    print("1. Verify the web interface shows your results correctly")
    print("2. Upload all files to your GitHub repository")
    print("3. Enable GitHub Pages and Actions as described in README.md")
    print("4. Your site will be live at: https://yourusername.github.io/your-repo-name")

if __name__ == "__main__":
    main()
