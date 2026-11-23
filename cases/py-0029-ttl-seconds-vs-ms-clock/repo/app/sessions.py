import secrets

from app import clock


def create_session(store, user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    store.put(token, {"user_id": user_id, "created_at": clock.now()})
    return token


def get_session(store, token: str):
    return store.get(token)
