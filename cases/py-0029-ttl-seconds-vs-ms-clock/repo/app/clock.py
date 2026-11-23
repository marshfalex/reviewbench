import time


def now() -> int:
    """Current Unix time in milliseconds. All stored timestamps in this app use milliseconds."""
    return int(time.time() * 1000)
