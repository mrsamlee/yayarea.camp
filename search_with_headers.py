#!/usr/bin/env python3
"""
Advanced wrapper script that modifies requests to bypass anti-bot detection
and handles 403 Forbidden errors from Reserve California.
"""

import requests
import time
import random
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# More diverse and current user agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
]

# Common referrers to make requests look more legitimate
REFERRERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://duckduckgo.com/',
    'https://www.reservecalifornia.com/',
    'https://www.parks.ca.gov/',
    'https://www.recreation.gov/'
]

def setup_session():
    """Set up a requests session with advanced anti-bot bypass techniques."""
    session = requests.Session()
    
    # Random user agent and referrer
    user_agent = random.choice(USER_AGENTS)
    referrer = random.choice(REFERRERS)
    
    # More comprehensive and realistic headers
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
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })
    
    # Enhanced retry strategy including 403 errors
    retry_strategy = Retry(
        total=5,
        backoff_factor=3,
        status_forcelist=[403, 429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def monkey_patch_requests():
    """Monkey patch requests to use our custom session with advanced bypass techniques."""
    import requests
    
    # Store original methods
    original_get = requests.get
    original_post = requests.post
    original_session = requests.Session
    
    def patched_get(*args, **kwargs):
        session = setup_session()
        # Longer, more human-like delays
        time.sleep(random.uniform(2, 8))
        return session.get(*args, **kwargs)
    
    def patched_post(*args, **kwargs):
        session = setup_session()
        time.sleep(random.uniform(2, 8))
        return session.post(*args, **kwargs)
    
    def patched_session(*args, **kwargs):
        # Override Session creation to use our enhanced session
        return setup_session()
    
    # Apply patches
    requests.get = patched_get
    requests.post = patched_post
    requests.Session = patched_session

if __name__ == "__main__":
    # Apply the monkey patch
    monkey_patch_requests()
    
    # Now import and run the main script
    import main
    import sys
    
    # Pass through any command line arguments
    if len(sys.argv) > 1:
        # Reconstruct the command line arguments for main.py
        main.sys.argv = sys.argv
    else:
        # Default to reserve_california if no provider specified
        main.sys.argv = ['search_with_headers.py', '--provider', 'reserve_california']
    
    main.main()
