#!/usr/bin/env python3
"""
Script to run two batches of campsite searches with a 5-minute delay between them.
Batch 1: Tomorrow to 3 months from now
Batch 2: 3 months from now to 6 months from now
Results are merged into a single results.json file.
"""

import subprocess
import datetime
import time
import json
import os
from dateutil.relativedelta import relativedelta

def run_batch(start_date, end_date, batch_name, append=False):
    """Run a single batch of the search."""
    print(f"\n{'='*60}")
    print(f"Starting {batch_name}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'='*60}")
    
    # Build command
    cmd = [
        'python3', 'main.py',
        '--start-date', start_date.strftime('%Y-%m-%d'),
        '--end-date', end_date.strftime('%Y-%m-%d'),
        '--batch-name', batch_name
    ]
    
    try:
        # Run the search
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 minute timeout
        
        if result.returncode == 0:
            print(f"✅ {batch_name} completed successfully")
            print("STDOUT:", result.stdout)
            return True
        else:
            print(f"❌ {batch_name} failed with return code {result.returncode}")
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {batch_name} timed out after 30 minutes")
        return False
    except Exception as e:
        print(f"💥 {batch_name} failed with exception: {e}")
        return False

def merge_results():
    """Merge results from both batches if they exist."""
    batch1_file = 'results_batch1.json'
    batch2_file = 'results_batch2.json'
    
    if not os.path.exists(batch1_file) and not os.path.exists(batch2_file):
        print("No batch results found to merge")
        return
    
    merged_results = []
    total_results = 0
    
    # Load batch 1 results
    if os.path.exists(batch1_file):
        with open(batch1_file, 'r') as f:
            batch1_data = json.load(f)
            batch1_results = batch1_data.get('results', [])
            merged_results.extend(batch1_results)
            total_results += len(batch1_results)
            print(f"Loaded {len(batch1_results)} results from batch 1")
    
    # Load batch 2 results
    if os.path.exists(batch2_file):
        with open(batch2_file, 'r') as f:
            batch2_data = json.load(f)
            batch2_results = batch2_data.get('results', [])
            merged_results.extend(batch2_results)
            total_results += len(batch2_results)
            print(f"Loaded {len(batch2_results)} results from batch 2")
    
    # Create merged results file
    from dateutil import tz
    pacific_tz = tz.gettz('US/Pacific')
    pacific_time = datetime.datetime.now(pacific_tz)
    
    merged_data = {
        "last_updated": pacific_time.isoformat(),
        "last_updated_pst": pacific_time.strftime('%Y-%m-%d %I:%M %p %Z'),
        "total_results": total_results,
        "search_criteria": {
            "batch1": "Tomorrow to 3 months",
            "batch2": "3 months to 6 months",
            "consecutive_nights": 2,
            "weekends_only": True
        },
        "batch_info": {
            "batch1_results": len(batch1_data.get('results', [])) if os.path.exists(batch1_file) else 0,
            "batch2_results": len(batch2_data.get('results', [])) if os.path.exists(batch2_file) else 0
        },
        "results": merged_results
    }
    
    with open('results.json', 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    print(f"\n✅ Merged results saved to results.json")
    print(f"Total campsites found: {total_results}")
    print(f"Batch 1: {merged_data['batch_info']['batch1_results']} results")
    print(f"Batch 2: {merged_data['batch_info']['batch2_results']} results")

def main():
    """Main function to run both batches."""
    print("🚀 Starting two-batch campsite search")
    
    # Calculate dates
    tomorrow = datetime.date.today() + relativedelta(days=1)
    three_months = tomorrow + relativedelta(months=3)
    six_months = tomorrow + relativedelta(months=6)
    
    print(f"Batch 1: {tomorrow} to {three_months}")
    print(f"Batch 2: {three_months} to {six_months}")
    
    # Run batch 1
    success1 = run_batch(tomorrow, three_months, "batch1", append=False)
    
    if success1:
        # Rename results.json to results_batch1.json
        if os.path.exists('results.json'):
            os.rename('results.json', 'results_batch1.json')
            print("✅ Batch 1 results saved to results_batch1.json")
    
    # Wait 5 minutes between batches
    print(f"\n⏰ Waiting 5 minutes before starting batch 2...")
    time.sleep(300)  # 5 minutes
    
    # Run batch 2
    success2 = run_batch(three_months, six_months, "batch2", append=False)
    
    if success2:
        # Rename results.json to results_batch2.json
        if os.path.exists('results.json'):
            os.rename('results.json', 'results_batch2.json')
            print("✅ Batch 2 results saved to results_batch2.json")
    
    # Merge results
    print(f"\n🔄 Merging results from both batches...")
    merge_results()
    
    # Clean up temporary files
    for temp_file in ['results_batch1.json', 'results_batch2.json']:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"🗑️ Cleaned up {temp_file}")
    
    print(f"\n🎉 Two-batch search completed!")
    print(f"Final results saved to results.json")

if __name__ == "__main__":
    main()
