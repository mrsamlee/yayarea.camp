"""
AWS Lambda function to run campsite search and push results to GitHub
"""
import json
import os
import boto3
import subprocess
import tempfile
import shutil
from datetime import datetime
from git import Repo
import base64

def lambda_handler(event, context):
    """
    Lambda function to search for campsites and push results to GitHub
    """
    print(f"Starting campsite search at {datetime.now()}")
    
    try:
        # Run the campsite search
        results = run_campsite_search()
        
        # Push results to GitHub
        success = push_to_github(results)
        
        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Campsite search completed and pushed to GitHub',
                    'timestamp': datetime.now().isoformat(),
                    'results_count': len(results.get('results', []))
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Failed to push to GitHub',
                    'timestamp': datetime.now().isoformat()
                })
            }
            
    except Exception as e:
        print(f"Lambda error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Lambda execution failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
        }

def run_campsite_search():
    """Run the campsite search and return results"""
    # Import your existing search logic
    import sys
    sys.path.append('/tmp')
    
    # Copy your modules to /tmp (Lambda's writable directory)
    # Note: You'll need to package these with your Lambda deployment
    
    try:
        from main import run_search_and_save
        
        # Run the search
        run_search_and_save()
        
        # Read the results
        with open('/tmp/results.json', 'r') as f:
            results = json.load(f)
            
        return results
        
    except Exception as e:
        print(f"Search error: {e}")
        # Return empty results on error
        return {
            'last_updated': datetime.now().isoformat(),
            'total_results': 0,
            'results': [],
            'error': str(e)
        }

def push_to_github(results):
    """Push results to GitHub repository"""
    try:
        # GitHub repository details
        repo_url = "https://github.com/mrsamlee/yayarea.camp.git"
        branch = "main"
        
        # GitHub token from environment variable
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            raise Exception("GITHUB_TOKEN environment variable not set")
        
        # Create authenticated URL
        auth_url = repo_url.replace('https://', f'https://{github_token}@')
        
        # Clone repository to /tmp
        repo_dir = '/tmp/yayarea-camp'
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        
        repo = Repo.clone_from(auth_url, repo_dir, branch=branch)
        
        # Update results.json
        results_file = os.path.join(repo_dir, 'results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Commit and push
        repo.index.add(['results.json'])
        repo.index.commit(f"Auto-update campsite results - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        origin = repo.remote('origin')
        origin.push(branch)
        
        print("✅ Successfully pushed to GitHub")
        return True
        
    except Exception as e:
        print(f"❌ Failed to push to GitHub: {e}")
        return False
