import logging
import threading
import queue
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class AsyncLoggingHandler(logging.Handler):
    """
    An asynchronous logging handler wrapping another logging handler.
    """

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.log_queue = queue.Queue()
        self.thread = threading.Thread(target=self.consume_log)
        self.thread.daemon = True
        self.thread.start()

    def emit(self, record):
        self.log_queue.put(record)

    def consume_log(self):
        while True:
            record = self.log_queue.get()
            self.handler.emit(record)
            self.log_queue.task_done()

    def close(self):
        self.log_queue.join()
        self.handler.close()
        super().close()


class CustomLogger(logging.Logger):
    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Override findCaller to capture the file name and line number of the logging call.
        """
        f = logging.currentframe()
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        return co.co_filename, f.f_lineno, co.co_name, None


logging.setLoggerClass(CustomLogger)


class LogManager:
    def __init__(self, name=__name__, level=logging.DEBUG, log_dir='logs', log_file_prefix='app',
                 maxBytes=5 * 1024 * 1024, backupCount=5):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        log_file = f"{log_file_prefix}_{timestamp}.log"
        log_path = os.path.join(log_dir, log_file)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        file_handler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setFormatter(formatter)
        async_handler = AsyncLoggingHandler(file_handler)
        self.logger.addHandler(async_handler)

    def get_logger(self):
        return self.logger


# Usage
log_manager = LogManager(name=__name__, level=logging.DEBUG)
logger = log_manager.get_logger()
