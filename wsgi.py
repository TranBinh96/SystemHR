"""
WSGI entry point for production deployment
"""
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app
    logger.info("App imported successfully")
    logger.info(f"Database URI configured: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')[:50]}...")
except Exception as e:
    logger.error(f"Failed to import app: {e}")
    raise

if __name__ == "__main__":
    app.run()
