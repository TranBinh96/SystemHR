"""
Timezone utilities for handling datetime with proper timezone support
"""
from datetime import datetime, timezone
import pytz
from config import Config

def get_local_timezone():
    """Get local timezone from config"""
    return pytz.timezone(Config.TIMEZONE)

def get_local_now():
    """Get current datetime in local timezone"""
    local_tz = get_local_timezone()
    return datetime.now(local_tz)

def get_local_today():
    """Get today's date in local timezone"""
    return get_local_now().date()

def utc_to_local(utc_dt):
    """Convert UTC datetime to local timezone"""
    if utc_dt is None:
        return None
    
    if utc_dt.tzinfo is None:
        # Assume it's UTC if no timezone info
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    
    local_tz = get_local_timezone()
    return utc_dt.astimezone(local_tz)

def local_to_utc(local_dt):
    """Convert local datetime to UTC"""
    if local_dt is None:
        return None
    
    local_tz = get_local_timezone()
    
    if local_dt.tzinfo is None:
        # Assume it's local timezone if no timezone info
        local_dt = local_tz.localize(local_dt)
    
    return local_dt.astimezone(timezone.utc)

def format_local_datetime(dt, format_str='%Y-%m-%d %H:%M'):
    """Format datetime in local timezone"""
    if dt is None:
        return ''
    
    # Convert to local timezone if needed
    if dt.tzinfo is not None:
        local_dt = utc_to_local(dt)
    else:
        # Assume it's already local
        local_dt = dt
    
    return local_dt.strftime(format_str)

def format_local_date(date_obj, format_str='%Y-%m-%d'):
    """Format date object"""
    if date_obj is None:
        return ''
    
    return date_obj.strftime(format_str)

def parse_date_string(date_str, format_str='%Y-%m-%d'):
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_str, format_str).date()
    except (ValueError, TypeError):
        return None

def parse_datetime_string(datetime_str, format_str='%Y-%m-%d %H:%M'):
    """Parse datetime string to local datetime object"""
    try:
        dt = datetime.strptime(datetime_str, format_str)
        local_tz = get_local_timezone()
        return local_tz.localize(dt)
    except (ValueError, TypeError):
        return None

# Convenience functions for common operations
def now():
    """Get current local datetime"""
    return get_local_now()

def today():
    """Get today's date"""
    return get_local_today()

def utcnow():
    """Get current UTC datetime (for database storage)"""
    return datetime.utcnow()