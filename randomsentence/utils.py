import signal


def timeout_function(func, args=(), kwargs={}, timeout_duration=20, default=None):
    class MyTimeoutError(TimeoutError):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except MyTimeoutError:
        result = default
    finally:
        signal.alarm(0)

    return result
