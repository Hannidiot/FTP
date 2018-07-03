import logging
import time

from src.Settings import WorkDir

__all__ = ["logger"]

# -----------------------------------------
#          Set Logging Config
# -----------------------------------------
format_str = "%(asctime)-15s | %(levelname)-8s | %(user)s %(ip)s> %(message)s"

logging.basicConfig(level=logging.INFO,
                    format=format_str)

logger = logging.getLogger()

logtime = time.strftime('%Y%m%d', time.localtime(time.time()))
log_path = WorkDir + '/Logs/'
log_name = log_path + logtime + '.log'
log_file = log_name

# -----------------------------------------
#           Config file handler
# -----------------------------------------
fileHandler = logging.FileHandler(log_file, mode='a')
fmt = logging.Formatter(format_str)
fileHandler.setFormatter(fmt)
fileHandler.setLevel(logging.DEBUG)

# -----------------------------------------
#          Add handler to logger
# -----------------------------------------
logger.addHandler(fileHandler)

"""
    Unit test PASS
"""
if __name__ == '__main__':
    test = {'user': 'Hanniko', 'ip': '127.0.0.1'}
    logger.warning("Test Warn", extra=test)
    logger.info("Test Info", extra=test)
    logger.critical("Test Critical", extra=test)
    logger.error("Test Error", extra=test)
    with open(log_file, 'r') as f:
        a = f.read()
        print(a)
