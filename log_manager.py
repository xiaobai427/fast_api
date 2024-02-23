import logging
from logging.handlers import RotatingFileHandler
import threading
import queue
import os
from datetime import datetime


class AsyncLoggingHandler(logging.Handler):
    """
    An asynchronous logging handler wrapping another logging handler.
    """

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.log_queue = queue.Queue()
        self.thread = threading.Thread(target=self.consume_log)
        self.thread.daemon = True  # Daemon thread exits when the main thread exits
        self.thread.start()

    def emit(self, record):
        """
        Emit a record.
        Queue the record and let the thread write it when it's possible.
        """
        self.log_queue.put(record)

    def consume_log(self):
        """
        Consume the log.
        This runs on a separate thread and continuously consumes log records from the queue.
        """
        while True:
            record = self.log_queue.get()
            self.handler.emit(record)
            self.log_queue.task_done()

    def close(self):
        """
        Wait until the log queue is empty and close the underlying handler.
        """
        self.log_queue.join()
        self.handler.close()
        super().close()


class LogManager:
    """
    A LogManager class for easy logging setup with timestamped log files.
    """

    def __init__(self, name='app', level=logging.INFO, log_dir='logs', log_file_prefix='app', maxBytes=10 * 1024 * 1024,
                 backupCount=5):
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate a timestamped log file name
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        log_file = f"{log_file_prefix}_{timestamp}.log"
        log_path = os.path.join(log_dir, log_file)

        # Setup the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Define the formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

        # Create a rotating file handler with a custom namer to include timestamp
        file_handler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setFormatter(formatter)

        # Define a custom namer for the log files
        def namer(name):
            return name.replace(".log", f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

        file_handler.namer = namer

        # Wrap the file handler with an asynchronous handler
        async_handler = AsyncLoggingHandler(file_handler)
        self.logger.addHandler(async_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def close(self):
        """
        Close the LogManager and its underlying handlers.
        """
        # This calls the close method of all handlers.
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)


log_manager = LogManager(name=__name__, level=logging.DEBUG, log_dir='logs')