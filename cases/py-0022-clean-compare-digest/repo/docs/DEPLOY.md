# Deployment

All secrets (`WEBHOOK_SECRET`, `DATABASE_URL`) are required. The app must
refuse to start when one is missing: modules read them with `os.environ[...]`
at import time on purpose, so a misconfigured deploy fails its health check
instead of running with an empty secret.
