from hrflow.core.rate_limit import rate_limiter
import pytest
from time import time

@pytest.mark.rate_limit
def test_rate_limit_no_params():   
    i = 0
    
    @rate_limiter
    def increment():
        nonlocal i
        i += 1
    
    start_time = time()
    for round in range(5):
        increment()
        assert i == round + 1, ("The sub function wrapper with rate limiting must have",
            "a side effect, but the result is inconsistent with what it should be")
    
    end_time = time()
    duration = end_time - start_time
    
    assert duration < 1, "5 calls should be less than 1 second"

@pytest.mark.rate_limit
def test_rate_limit_no_params_and_with_function_params():   
    i = 0
    memory = None
    
    @rate_limiter
    def increment(round : int):
        nonlocal i
        nonlocal memory
        
        i += 1
        memory = round
        
    
    start_time = time()
    for round in range(5):
        increment(round)
        assert i == round + 1, ("The sub function wrapper with rate limiting must have",
            "a side effect, but the result is inconsistent with what it should be")
        assert memory == round, ("The sub function wrapper with rate limiting must",
            "have a side effect, but the result is inconsistent with what it should be")
        
    end_time = time()
    duration = end_time - start_time
    
    assert duration < 1, "5 calls should be less than 1 second"

@pytest.mark.rate_limit
def test_rate_limit_sleep_per_req_and_with_function_params():
    min_sleep_per_request = 1 # second(s)
    delta_duration = 0.1
    i = 0
    memory = None
    
    @rate_limiter
    def increment(round : int):
        nonlocal i
        nonlocal memory
        
        i += 1
        memory = round
        
    
    global_start_time = time()
    round_count = 5
    for round in range(round_count):
        round_start_time = time()
        increment(round, min_sleep_per_request=min_sleep_per_request)
        assert i == round + 1, ("The sub function wrapper with rate limiting must have",
            "a side effect, but the result is inconsistent with what it should be")
        assert memory == round, ("The sub function wrapper with rate limiting must",
            "have a side effect, but the result is inconsistent with what it should be")
        round_duration = time() - round_start_time
        assert round_duration + delta_duration >= min_sleep_per_request, (
            "function call must be more than {min_sleep_per_request} second"
        )

    end_time = time()
    global_duration = end_time - global_start_time
    
    assert global_duration + delta_duration >= min_sleep_per_request*round_count, (
        "5 calls should be more than 5 seconds"
    )

@pytest.mark.rate_limit
def test_rate_limit_with_rpm():
    SECONDS_IN_MINUTE = 60
    max_requests_per_minute = 5 # second(s)
    num_requests = 8
    delta_duration = 0.1
    i = 0
    
    @rate_limiter
    def increment():
        # less than 0.1 second function
        nonlocal i
        i += 1

    for round in range(num_requests):
        print(round)
        round_start_time = time()
        increment(max_requests_per_minute=max_requests_per_minute)
        assert i == round + 1, ("The sub function wrapper with rate limiting must have",
            "a side effect, but the result is inconsistent with what it should be")
        
        round_duration = time() - round_start_time
        if round != 0 and round % max_requests_per_minute == 0:
            assert round_duration + delta_duration >= SECONDS_IN_MINUTE, (
                f"unexpected more than {max_requests_per_minute} req per minute"
            )
        else:
            assert round_duration <= delta_duration, (
                f"function call must be less than {delta_duration} second(s)"
            )

@pytest.mark.rate_limit
def test_rate_limit_with_rpm_and_sleep_per_req():
    SECONDS_IN_MINUTE = 60
    min_sleep_per_request = 1 # second(s)
    max_requests_per_minute = 5 # second(s)
    num_requests = 8
    delta_duration = 0.1
    i = 0
    
    @rate_limiter
    def increment():
        # less than 0.1 second function
        nonlocal i
        i += 1

    for round in range(num_requests):
        print(round)
        round_start_time = time()
        increment(
            max_requests_per_minute=max_requests_per_minute,
            min_sleep_per_request=min_sleep_per_request
        )
        assert i == round + 1, ("The sub function wrapper with rate limiting must have",
            "a side effect, but the result is inconsistent with what it should be")
        
        round_duration = time() - round_start_time
        if round != 0 and round % max_requests_per_minute == 0:
            normilized_duration = round_duration + delta_duration \
                + min_sleep_per_request*max_requests_per_minute
            assert normilized_duration >= SECONDS_IN_MINUTE, (
                f"unexpected more than {max_requests_per_minute} req per minute"
            )
        else:
            assert round_duration + delta_duration >= min_sleep_per_request, (
                "function call must be more than {min_sleep_per_request} second"
            )