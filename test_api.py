#!/usr/bin/env python3
"""
Simple script to test if recreation.gov API is accessible from GitHub Actions
"""
import requests
import sys
from datetime import datetime

def test_api_access():
    """Test basic API access"""
    print(f"Testing API access at {datetime.now()}")
    
    # Test the base URL that's failing
    test_url = "https://calirdr.usedirect.com/rdr/rdr/search/filters"
    
    try:
        # Make a simple GET request
        response = requests.get(test_url, timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 403:
            print("❌ API is blocking requests (403 Forbidden)")
            print("This confirms GitHub Actions IPs are blocked")
            return False
        elif response.status_code == 200:
            print("✅ API is accessible")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def test_user_agent():
    """Test with different user agents"""
    print("\nTesting with different user agents...")
    
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Python/3.9 requests/2.28.1",
        "GitHub-Actions/1.0"
    ]
    
    test_url = "https://calirdr.usedirect.com/rdr/rdr/search/filters"
    
    for ua in user_agents:
        try:
            headers = {"User-Agent": ua}
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"User-Agent: {ua[:50]}... -> Status: {response.status_code}")
        except Exception as e:
            print(f"User-Agent: {ua[:50]}... -> Error: {e}")

if __name__ == "__main__":
    print("=== Recreation.gov API Access Test ===")
    
    # Test basic access
    success = test_api_access()
    
    # Test user agents
    test_user_agent()
    
    print(f"\n=== Test Complete ===")
    if not success:
        print("Recommendation: Use fallback data or different API approach")
        sys.exit(1)
    else:
        print("API appears to be working")
        sys.exit(0)
