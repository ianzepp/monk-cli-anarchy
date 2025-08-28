"""
Session Timer Utility
Live countdown for JWT token expiration
"""

from datetime import datetime
import time
from typing import Optional


class SessionTimer:
    """Manages JWT session countdown display"""
    
    @staticmethod
    def parse_expires_output(expires_text: str) -> Optional[datetime]:
        """Parse monk auth expires output to datetime"""
        try:
            # Handle different possible formats
            expires_text = expires_text.strip()
            
            # Try parsing the format we saw: "Thu Jan 18 20:30:22 EST 2018"
            formats_to_try = [
                "%a %b %d %H:%M:%S %Z %Y",  # Thu Jan 18 20:30:22 EST 2018
                "%Y-%m-%d %H:%M:%S",        # ISO-like format
                "%Y-%m-%dT%H:%M:%SZ",       # ISO format
            ]
            
            for fmt in formats_to_try:
                try:
                    return datetime.strptime(expires_text, fmt)
                except ValueError:
                    continue
                    
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def format_time_remaining(expires_at: datetime) -> str:
        """Format time remaining until expiration"""
        try:
            now = datetime.now()
            
            # Handle timezone-naive comparison (assumes same timezone)
            if expires_at.tzinfo is None and now.tzinfo is None:
                time_remaining = expires_at - now
            else:
                # For now, just use naive comparison
                time_remaining = expires_at.replace(tzinfo=None) - now
            
            if time_remaining.total_seconds() <= 0:
                # Calculate how long ago it expired
                expired_seconds = abs(int(time_remaining.total_seconds()))
                if expired_seconds < 3600:  # Less than 1 hour
                    mins = expired_seconds // 60
                    return f"🔴 EXPIRED {mins}m ago"
                elif expired_seconds < 86400:  # Less than 1 day
                    hours = expired_seconds // 3600
                    return f"🔴 EXPIRED {hours}h ago"
                else:  # More than a day
                    days = expired_seconds // 86400
                    return f"🔴 EXPIRED {days}d ago"
                
            total_seconds = int(time_remaining.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            if hours > 0:
                return f"{hours}h {minutes}m remaining"
            elif minutes > 0:
                return f"{minutes}m {seconds}s remaining"
            else:
                return f"{seconds}s remaining"
                
        except Exception:
            return "Unknown expiration"
    
    @staticmethod
    def get_session_display(expires_text: str) -> str:
        """Get formatted session display string"""
        expires_at = SessionTimer.parse_expires_output(expires_text)
        
        if expires_at:
            remaining = SessionTimer.format_time_remaining(expires_at)
            return f"Session: {remaining}"
        else:
            return f"Session: {expires_text}"  # Fallback to raw text