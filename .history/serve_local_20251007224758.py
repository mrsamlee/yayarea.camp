#!/usr/bin/env python3
"""
Simple local HTTP server to serve the campsite search results.
This solves CORS issues when testing locally.
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

def main():
    PORT = 8000
    
    # Check if required files exist
    required_files = ['index.html', 'results.json']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Error: {file} not found")
            print("Make sure you're in the project directory and have run the search.")
            return
    
    print(f"🏕️ Starting local server for Bay Area Camping Tracker")
    print(f"📍 Server running at: http://localhost:{PORT}")
    print(f"🌐 Opening browser...")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Create custom handler to serve files with correct MIME types
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers to allow local file access
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def guess_type(self, path):
            # Ensure JSON files are served with correct MIME type
            if path.endswith('.json'):
                return 'application/json'
            return super().guess_type(path)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            # Open browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use. Try closing other applications or use a different port.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
