#!/usr/bin/env python3
"""
Script to run campsite search locally and deploy to GitHub Pages
"""
import subprocess
import sys
import os
from datetime import datetime

def run_search():
    """Run the campsite search locally"""
    print(f"🔍 Running campsite search at {datetime.now()}")
    try:
        # Run the search
        result = subprocess.run([
            sys.executable, "-c", 
            "from main import run_search_and_save; run_search_and_save()"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Search completed successfully")
            return True
        else:
            print("❌ Search failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running search: {e}")
        return False

def commit_and_deploy():
    """Commit the results and push to trigger deployment"""
    print("📤 Committing and pushing results...")
    
    try:
        # Add the results file
        subprocess.run(["git", "add", "results.json"], check=True)
        
        # Commit with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_message = f"Update campsite search results - {timestamp}"
        
        subprocess.run([
            "git", "commit", "-m", commit_message
        ], check=True)
        
        # Push to trigger GitHub Pages deployment
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ Successfully pushed to GitHub!")
        print("🌐 Your site will update at: https://mrsamlee.github.io/yayarea.camp/")
        print("⏱️  GitHub Pages deployment usually takes 2-5 minutes")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False

def main():
    """Main workflow"""
    print("🚀 Bay Area Camping - Local Search & Deploy")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not in a git repository. Please run this from your project directory.")
        return 1
    
    # Check if results.json exists
    if not os.path.exists("results.json"):
        print("❌ results.json not found. Please run the search first.")
        return 1
    
    # Run the search
    if not run_search():
        print("❌ Search failed. Check your internet connection and try again.")
        return 1
    
    # Deploy
    if not commit_and_deploy():
        print("❌ Deployment failed.")
        return 1
    
    print("\n🎉 All done! Your campsite search results are now live!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
