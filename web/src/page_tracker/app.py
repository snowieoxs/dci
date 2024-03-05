# src/page_tracker/app.py

"""
This module defines a simple Flask application that uses Redis to track the
number of page views.

The application defines a single route ("/") that increments a counter in
Redis each time it's accessed and returns a message indicating how many times
the page has been viewed.

The Redis client used by the application is created using the URL specified in
the REDIS_URL environment variable, or "redis://localhost:6379" if REDIS_URL
is not set. The client is cached, so subsequent calls to the `redis` function
will return the same client instance.

This module also handles Redis errors by logging the error and returning an
error message to the client.
"""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """Handle GET requests to the root URL.

    Increments the page view count in Redis and returns a message indicating
    how many times the page has been viewed. If a Redis error occurs, logs the
    error and returns an error message.

    Returns:
        str: A message indicating how many times the page has been viewed, or
            an error message if a Redis error occurs.
    """
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{pensive face}", 500
    return f"This page has been seen {page_views} times."


@cache
def redis():
    """Get a Redis client.

    The client is created using the URL specified in the REDIS_URL environment
    variable, or "redis://localhost:6379" if REDIS_URL is not set. The client
    is cached, so subsequent calls to this function will return the same client
    instance.

    Returns:
        Redis: A Redis client.
    """
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))


# never ever do this
# if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)
