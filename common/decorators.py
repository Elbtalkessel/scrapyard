def retry(attempts=10, callback=None, exc=(Exception,)):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exc as e:
                    if callback is not None:
                        callback(e, i)
            return func(*args, **kwargs)
        return func_wrapper
    return decorator


def noexception(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return func_wrapper
