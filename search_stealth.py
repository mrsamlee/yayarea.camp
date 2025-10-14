#!/usr/bin/env python3
"""
Ultra-stealth search script with maximum anti-bot bypass techniques.
This is the most aggressive approach to bypass Reserve California's blocking.
"""

import requests
import time
import random
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Most current and diverse user agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/117.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/117.0.0.0'
]

# Realistic referrers and origins
REFERRERS = [
    'https://www.google.com/search?q=california+camping+reservations',
    'https://www.bing.com/search?q=reserve+california+camping',
    'https://duckduckgo.com/?q=california+state+parks+camping',
    'https://www.reservecalifornia.com/',
    'https://www.parks.ca.gov/',
    'https://www.recreation.gov/',
    'https://www.google.com/',
    'https://www.bing.com/'
]

def setup_stealth_session():
    """Set up an ultra-stealth session with maximum bypass techniques."""
    # Use the original Session class to avoid recursion
    if hasattr(requests, '_original_session_stealth'):
        session = requests._original_session_stealth()
    else:
        session = requests.Session()
    
    # Random selection for each request
    user_agent = random.choice(USER_AGENTS)
    referrer = random.choice(REFERRERS)
    
    # Ultra-realistic headers that match modern browsers exactly
    session.headers.update({
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': referrer,
        'Origin': 'https://www.reservecalifornia.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Ch-Ua-Platform-Version': '"14.0.0"',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    # Maximum retry strategy
    retry_strategy = Retry(
        total=7,
        backoff_factor=5,
        status_forcelist=[403, 429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def monkey_patch_requests_stealth():
    """Ultra-stealth monkey patch with maximum human-like behavior."""
    import requests
    
    # Store original methods to avoid recursion
    if not hasattr(requests, '_original_get_stealth'):
        requests._original_get_stealth = requests.get
        requests._original_post_stealth = requests.post
        requests._original_session_stealth = requests.Session
    
    def patched_get(*args, **kwargs):
        session = setup_stealth_session()
        # Very long, human-like delays
        time.sleep(random.uniform(5, 15))
        return session.get(*args, **kwargs)
    
    def patched_post(*args, **kwargs):
        session = setup_stealth_session()
        time.sleep(random.uniform(5, 15))
        return session.post(*args, **kwargs)
    
    def patched_session(*args, **kwargs):
        return setup_stealth_session()
    
    # Apply patches only if not already patched
    if requests.get != patched_get:
        requests.get = patched_get
        requests.post = patched_post
        requests.Session = patched_session

if __name__ == "__main__":
    # Apply the ultra-stealth monkey patch
    monkey_patch_requests_stealth()
    
    # Now import and run the main script
    import main
    import sys
    
    # Pass through any command line arguments
    if len(sys.argv) > 1:
        # Reconstruct the command line arguments for main.py
        main.sys.argv = sys.argv
    else:
        # Default to reserve_california if no provider specified
        main.sys.argv = ['search_stealth.py', '--provider', 'reserve_california']
    
    main.main()
