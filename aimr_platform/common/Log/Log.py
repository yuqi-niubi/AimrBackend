"""
@author: chenxd
@software: PyCharm
@file: Log.py
@time: 2020/10/15 11:25
"""

import logging
import os
from logging import handlers


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'default': logging.logProcesses,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self,
                 filename,
                 level='info',
                 when='midnight',
                 back_count=5,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        f_dir, f_name = os.path.split(filename)
        os.makedirs(f_dir, exist_ok=True)  # 当前目录新建log文件夹
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count,
                                               encoding='utf-8')  # 往文件里写入指定间隔时间自动生成文件的Handler
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时
        # D 天
        # 'W0'-'W6' 每星期（interval=0时代表星期一：W0）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(th)

