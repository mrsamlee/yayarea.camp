#!/usr/bin/env python3
"""
Wrapper script that modifies requests to look more like a real browser
and handles the 403 Forbidden errors from Reserve California.
"""

import requests
import time
import random
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Real browser user agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def setup_session():
    """Set up a requests session with realistic browser headers and retry logic."""
    session = requests.Session()
    
    # Add realistic headers
    session.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    })
    
    # Set up retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def monkey_patch_requests():
    """Monkey patch requests to use our custom session."""
    import requests
    
    # Store original methods
    original_get = requests.get
    original_post = requests.post
    
    def patched_get(*args, **kwargs):
        session = setup_session()
        # Add random delay to look more human
        time.sleep(random.uniform(1, 3))
        return session.get(*args, **kwargs)
    
    def patched_post(*args, **kwargs):
        session = setup_session()
        time.sleep(random.uniform(1, 3))
        return session.post(*args, **kwargs)
    
    # Apply patches
    requests.get = patched_get
    requests.post = patched_post

if __name__ == "__main__":
    # Apply the monkey patch
    monkey_patch_requests()
    
    # Now import and run the main script
    import main
    main.main()
