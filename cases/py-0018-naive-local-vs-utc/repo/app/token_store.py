from datetime import datetime, timedelta


def new_token_expiry(ttl_minutes: int = 30) -> datetime:
    """Stored in the tokens table as a naive datetime in UTC."""
    return datetime.utcnow() + timedelta(minutes=ttl_minutes)
