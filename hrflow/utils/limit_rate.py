from functools import wraps
from time import sleep, time

DEFAULT_MAX_REQUESTS_PER_MINUTE = None
DEFAULT_MIN_SLEEP_PER_REQUEST = 0
SECONDS_IN_MINUTE = 60


def rate_limiter(func):
    """
    Decorator that applies rate limiting to a function.

    Parameters in the decorated function:
        max_requests_per_minute: <int> The maximum number of requests that can be made
            in a minute. If None, there is no limit.
        min_sleep_per_request: <float> The minimum time to wait between requests.

    Usage:
    >>> @rate_limiter()
    ... def my_function(param1, param2):
    ...    pass
    ... my_function(1, 2, max_requests_per_minute=10, min_sleep_per_request=0.1)
    ... # The function will be called at most 10 times per minute
    ... # with at least 0.1 seconds between each call
    """
    requests_per_minute = 0
    last_reset_time = time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        max_requests_per_minute = kwargs.pop(
            "max_requests_per_minute", DEFAULT_MAX_REQUESTS_PER_MINUTE
        )
        min_sleep_per_request = kwargs.pop(
            "min_sleep_per_request", DEFAULT_MIN_SLEEP_PER_REQUEST
        )
        nonlocal requests_per_minute, last_reset_time

        current_time = time()
        elapsed_time = current_time - last_reset_time

        if elapsed_time < SECONDS_IN_MINUTE:
            requests_per_minute += 1
            if (
                max_requests_per_minute is not None
                and requests_per_minute > max_requests_per_minute
            ):

                sleep(SECONDS_IN_MINUTE - elapsed_time)
                requests_per_minute = 0
                last_reset_time = time()
        else:
            requests_per_minute = 0
            last_reset_time = current_time

        sleep(min_sleep_per_request)
        return func(*args, **kwargs)

    return wrapper
