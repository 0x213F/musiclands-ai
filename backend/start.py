#!/usr/bin/env python3
"""
Startup script for Musiclands AI API server
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    # Import and run the main application
    from main import app
    import uvicorn
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get configuration from environment
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"🚀 Starting Musiclands AI API server...")
    print(f"🌍 Environment: {environment}")
    print(f"🏠 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=environment == "development",
        log_level="info"
    )