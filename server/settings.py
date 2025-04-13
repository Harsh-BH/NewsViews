"""
This module is an alias to config.py for backward compatibility.
New code should import directly from config.py instead.
"""

from config import settings, APP_NAME, DEBUG, DATABASE_URL

# Re-export everything from config
__all__ = ['settings', 'APP_NAME', 'DEBUG', 'DATABASE_URL']
