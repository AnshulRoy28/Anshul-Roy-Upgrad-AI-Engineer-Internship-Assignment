#!/usr/bin/env python3
"""
Unified server launcher for AI Mock Interview Coach.

This script starts the Flask server that serves both:
- The REST API endpoints at /api/v1/*
- The frontend static files at /*

Usage:
    python run_server.py
    
Or with custom port:
    python run_server.py --port 3000
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import config
from api_server import app


def main():
    parser = argparse.ArgumentParser(
        description='AI Mock Interview Coach - Unified Server'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to run the server on (default: 8000)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    # Check API key
    if not config.GOOGLE_API_KEY:
        print("\n❌ Error: GOOGLE_API_KEY not found in environment")
        print("   Please set it in your .env file")
        print("\n   Example .env file:")
        print("   GOOGLE_API_KEY=your_api_key_here\n")
        sys.exit(1)
    
    # Print startup banner
    print("\n" + "=" * 70)
    print("🚀 AI Mock Interview Coach - Unified Server")
    print("=" * 70)
    print(f"\n🌐 Frontend:  http://localhost:{args.port}")
    print(f"📚 API Base:  http://localhost:{args.port}/api/v1")
    print(f"\n📝 Features:")
    print(f"   • Landing page at /")
    print(f"   • Interview app at /interview.html")
    print(f"   • REST API at /api/v1/*")
    print(f"\n✅ Server starting...\n")
    
    # Run server
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
