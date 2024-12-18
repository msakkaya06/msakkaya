import time
from .log_base import PerformanceLog

# Decorator fonksiyonunu closure yapısı ile düzeltme
def log_performance(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            performance_log = PerformanceLog(action_name, execution_time)
            performance_log.send()
            return result
        return wrapper
    return decorator
