#!/usr/bin/env python3
"""
Local HTTP server for testing GLEIF well-known resources
Serves .well-known directory with proper CORS headers and JSON content types
"""

import argparse
import http.server
import json
import os
import socketserver
import sys
from pathlib import Path


class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        root_dir = Path(__file__).parent.parent.parent
        super().__init__(*args, directory=str(root_dir), **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

        if self.path.endswith('.json'):
            self.send_header('Content-Type', 'application/json; charset=utf-8')

        super().end_headers()

    def do_options(self):
        self.send_response(200)
        self.end_headers()

    def do_get(self):
        print(f"GET {self.path}")

        # Check if the requested file exists
        file_path = self.translate_path(self.path)

        if not os.path.exists(file_path):
            print(f"   [404] Not found: {file_path}")

        return super().do_GET()

    def log_message(self, format, *args):
        sys.stdout.write(f"   [{self.log_date_time_string()}] {format % args}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Serve GLEIF well-known resources locally')
    parser.add_argument('-p', '--port', type=int, default=8080,
                       help='Port to run the server on (default: 8080)')
    parser.add_argument('-b', '--bind', default='127.0.0.1',
                       help='Address to bind to (default: 127.0.0.1)')
    args = parser.parse_args()

    with socketserver.TCPServer((args.bind, args.port),
                                 CORSHTTPRequestHandler) as httpd:
        print(f"\nServer running at http://{args.bind}:{args.port}")
        print(f"Main index: http://{args.bind}:{args.port}/.well-known/index.json")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped")
            sys.exit(0)

if __name__ == '__main__':
    main()
