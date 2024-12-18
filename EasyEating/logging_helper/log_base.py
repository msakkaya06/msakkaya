from abc import ABC, abstractmethod
from datetime import datetime
from .elasticsearch_logger import ElasticsearchLogger  # Elasticsearch'e veri gönderecek sınıfı dahil ediyoruz

class Log(ABC):
    @abstractmethod
    def prepare_log(self):
        pass

    @abstractmethod
    def send(self):
        pass

class GeneralLog(Log):
    def __init__(self, message, level, extra_data=None):
        self.message = message
        self.level = level
        self.timestamp = datetime.now()
        self.extra_data = extra_data or {}

    def prepare_log(self):
        return {
            'message': self.message,
            'level': self.level,
            'timestamp': self.timestamp,
            'extra_data': self.extra_data
        }

    def send(self):
        es_logger = ElasticsearchLogger()
        log_data = self.prepare_log()
        es_logger.log('general_logs', log_data)

class UserActivityLog(Log):
    def __init__(self, user, action, metadata=None):
        self.user = user
        self.action = action
        self.timestamp = datetime.now()
        self.metadata = metadata or {}

    def prepare_log(self):
        return {
            'user': self.user,
            'action': self.action,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }

    def send(self):
        es_logger = ElasticsearchLogger()
        log_data = self.prepare_log()
        es_logger.log('user_activity_logs', log_data)

class PerformanceLog(Log):
    def __init__(self, action_name, execution_time, extra_data=None):
        self.action_name = action_name
        self.execution_time = execution_time
        self.timestamp = datetime.now()
        self.extra_data = extra_data or {}

    def prepare_log(self):
        return {
            'action_name': self.action_name,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp,
            'extra_data': self.extra_data
        }

    def send(self):
        es_logger = ElasticsearchLogger()
        log_data = self.prepare_log()
        es_logger.log('performance_logs', log_data)
