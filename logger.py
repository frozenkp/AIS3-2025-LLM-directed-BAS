import logging
import sys
import textwrap

CRITICAL    = logging.CRITICAL
ERROR       = logging.ERROR
WARNING     = logging.WARNING
INFO        = logging.INFO
DEBUG       = logging.DEBUG

class ModuleFilter(logging.Filter):
    def __init__(self):
        super().__init__()

        self.module = 'MODULE'

    def set_module(self, module):
        self.module = module

    def filter(self, record: logging.LogRecord) -> bool:
        record.module = self.module
        return True

class Logger():
    def __init__(self, name, stderr=True, log_file=None, level=DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # formatter
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s][%(module)s] %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # filter
        self.module_filter = ModuleFilter()
        self.logger.addFilter(self.module_filter)

        # handler
        if not self.logger.hasHandlers() and stderr:
            # incomplete but acceptable solution
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if log_file is not None:
            handler = logging.FileHandler(log_file)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def module(self, name):
        self.module_filter.set_module(name)
        return self

    def log(self, level, message, *args):
        self.logger.log(level, str(message), *args)

    def critical(self, message, *args):
        self.logger.critical(str(message), *args)
    
    def error(self, message, *args):
        self.logger.error(str(message), *args)

    def warning(self, message, *args):
        self.logger.warning(str(message), *args)

    def info(self, message, *args):
        self.logger.info(str(message), *args)

    def debug(self, message, *args):
        self.logger.debug(str(message), *args)

COLOR_RESET     = '\033[0m'
COLOR_BLACK     = '\033[30m'
COLOR_RED       = '\033[31m'
COLOR_GREEN     = '\033[32m'
COLOR_YELLOW    = '\033[33m'
COLOR_BLUE      = '\033[34m'
COLOR_MAGENTA   = '\033[35m'
COLOR_CYAN      = '\033[36m'
COLOR_WHITE     = '\033[37m'

class Msg():
    def __init__(self, title, data, color='white'):
        self.message = self.build_message(title, data, color)

    def build_message(self, title, data, color):
        # format data
        data_str = self.format_data(data)

        # color
        color_pad = {
            'black':    COLOR_BLACK,
            'red':      COLOR_RED,
            'green':    COLOR_GREEN,
            'yellow':   COLOR_YELLOW,
            'blue':     COLOR_BLUE,
            'magenta':  COLOR_MAGENTA,
            'cyan':     COLOR_CYAN,
            'white':    COLOR_WHITE,
        }

        # message
        color_str = color_pad[color.strip().lower()]
        message = f'{title}: {color_str}{data_str}{COLOR_RESET}'

        return message

    def format_data(self, data):
        data_str = ''
        match data:
            case dict():
                if len(data.keys()) != 0:
                    max_length = len(max(data.keys(), key=len))
                    data_str = '\n'.join([f'{key:{max_length}s}: {value}' for key, value in data.items()])
            
            case list():
                if len(data) != 0:
                    max_length = len(str(len(data) - 1))
                    data_str = '\n'.join([f'{idx:{max_length}d}: {value}' for idx, value in enumerate(data)])

            case _:
                data_str = str(data)

        data_lines = data_str.split('\n')
        if len(data_lines) > 1 or len(data_lines[0]) > 60: 
            data_str = '\n' + data_str

        return data_str

    def __str__(self):
        return self.message
