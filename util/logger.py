# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2020/11/18 16:45

import logging
import time

# 使用方法：
#   logger = log.create_logger(config.LOG_LEVEL, config.LOG_PATH, LOG_NAME)
#   例如：
#         logger = log.create_logger(config.LOG_LEVEL,
#           config.LOG_ROOT+"\\database_connect_log", "database_connect_log")
#         logger.debug(MESSAGE) 即可向指定log进行记录


# 创建一个级别为level的logger debug打印到文件和控制台 info及以上打到文件
def create_logger(level, log_file_path, logger_name, print_stream_cmd=False):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    print_file = logging.FileHandler(log_file_path, encoding='utf-8')
    print_stream = logging.StreamHandler()
    print_file.setFormatter(formatter)
    print_stream.setFormatter(formatter)
    if level == logging.DEBUG or print_stream_cmd:
        logger.addHandler(print_stream)
    logger.addHandler(print_file)
    logger.setLevel(level)
    return logger


# 函数装饰器，输出函数运行时间
def log(func):
    def wrapper(*args, **kwatgs):
        start_time = time.time()
        logging.info('start %s()' % func.__name__)
        ret = func(*args, **kwatgs)
        end_time = time.time()
        logging.info('end {}()\ncost {:.5f} seconds'.format(func.__name__, end_time - start_time))
        return ret

    return wrapper
