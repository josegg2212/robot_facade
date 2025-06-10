import logging
import colorlog


class Logger:
    _instance = None  # Singleton instance

    @staticmethod
    def get_logger():
        """Return the singleton logger instance."""
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            # Prevent multiple instances
            raise Exception("Logger is a singleton! Use get_logger() instead.")
        
        # Configure Logger
        Logger._instance = logging.getLogger("Logger")
        
        if not Logger._instance.hasHandlers():  # Avoid duplicate handlers
            # Set level
            Logger._instance.setLevel(logging.INFO)
            
            # Stream handler (console output)
            console_handler = logging.StreamHandler()
            formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s - %(asctime)s - %(pathname)s:%(lineno)d - %(module)s - %(funcName)s - %(message)s',
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red,bg_white',
                },
                reset=True,
                style='%'
            )
            console_handler.setFormatter(formatter)
            Logger._instance.addHandler(console_handler)

