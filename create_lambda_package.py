#!/usr/bin/env python3
"""
Script to create a deployment package for AWS Lambda
"""
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

def create_lambda_package():
    """Create a Lambda deployment package"""
    print("📦 Creating Lambda deployment package...")
    
    # Create temporary directory for packaging
    package_dir = "lambda_package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy Python files
    python_files = [
        "main.py",
        "campsites_map.py", 
        "lambda_function.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✅ Copied {file}")
        else:
            print(f"⚠️  {file} not found")
    
    # Install dependencies
    print("📥 Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "-r", "requirements.txt", 
        "-t", package_dir
    ], check=True)
    
    # Install GitPython for git operations
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "GitPython", 
        "-t", package_dir
    ], check=True)
    
    # Create zip file
    zip_file = "lambda_deployment.zip"
    if os.path.exists(zip_file):
        os.remove(zip_file)
    
    print(f"🗜️  Creating {zip_file}...")
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    # Clean up
    shutil.rmtree(package_dir)
    
    print(f"✅ Created {zip_file}")
    print(f"📊 Package size: {os.path.getsize(zip_file) / 1024 / 1024:.1f} MB")
    
    return zip_file

def create_deployment_instructions():
    """Create deployment instructions"""
    instructions = """
# AWS Lambda Deployment Instructions

## 1. Create Lambda Function
- Go to AWS Lambda Console
- Create new function: "campsite-search-scheduler"
- Runtime: Python 3.9
- Upload the lambda_deployment.zip file

## 2. Set Environment Variables
- GITHUB_TOKEN: Your GitHub Personal Access Token (with repo permissions)
- PYTHONPATH: /var/task

## 3. Set Function Configuration
- Memory: 512 MB
- Timeout: 10 minutes
- VPC: Not needed (unless you want to restrict internet access)

## 4. Create CloudWatch Event (EventBridge)
- Create rule: "campsite-search-schedule"
- Schedule expression: rate(1 hour)
- Target: Your Lambda function

## 5. Test the Function
- Test with empty event: {}
- Check CloudWatch logs for execution

## 6. Monitor
- CloudWatch logs will show execution results
- GitHub repository will be updated automatically
- GitHub Pages will redeploy when repo changes

## Required IAM Permissions
Your Lambda execution role needs:
- CloudWatch Logs (usually included by default)
- No additional permissions needed for basic operation
"""
    
    with open("LAMBDA_DEPLOYMENT.md", "w") as f:
        f.write(instructions)
    
    print("✅ Created LAMBDA_DEPLOYMENT.md with instructions")

if __name__ == "__main__":
    try:
        zip_file = create_lambda_package()
        create_deployment_instructions()
        print(f"\n🎉 Ready to deploy!")
        print(f"📁 Upload {zip_file} to AWS Lambda")
        print(f"📖 Follow instructions in LAMBDA_DEPLOYMENT.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
