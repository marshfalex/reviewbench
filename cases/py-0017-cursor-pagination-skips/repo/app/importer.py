from datetime import datetime, timezone


def import_posts(db, author_id: int, bodies: list[str]) -> None:
    """Bulk-import posts from a partner feed in one transaction."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    db.executemany(
        "INSERT INTO posts (author_id, created_at, body) VALUES (?, ?, ?)",
        [(author_id, now, body) for body in bodies],
    )
    db.commit()
