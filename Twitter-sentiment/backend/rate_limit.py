from time import time

REQUESTS = {}

def is_rate_limited(ip, limit=10):
    now = time()
    REQUESTS.setdefault(ip, [])
    REQUESTS[ip] = [t for t in REQUESTS[ip] if now - t < 60]

    if len(REQUESTS[ip]) >= limit:
        return True

    REQUESTS[ip].append(now)
    return False
