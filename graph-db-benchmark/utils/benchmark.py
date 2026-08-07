import time


def measure_execution_time(function, *args, **kwargs):
    """
    Measures execution time of any function.

    Returns:
        result, execution_time_ms
    """

    start = time.perf_counter()

    result = function(*args, **kwargs)

    end = time.perf_counter()

    execution_time = (end - start) * 1000

    return result, execution_time