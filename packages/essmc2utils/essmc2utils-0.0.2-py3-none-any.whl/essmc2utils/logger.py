# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.

import logging
import sys

from .file_systems import FS


def get_logger(name="essmc2"):
    logger = logging.getLogger(name)
    logger.propagate = False
    if len(logger.handlers) == 0:
        std_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        std_handler.setFormatter(formatter)
        std_handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(std_handler)
    return logger


def init_logger(in_logger, log_file=None, rank=0, main_log_level=logging.INFO, other_log_level=logging.ERROR):
    """ Add file handler to logger on rank 0 and set log level by dist_launcher

    Args:
        in_logger (logging.Logger):
        log_file (str, None): if not None, a file handler will be add to in_logger
        rank (int): default is 0
        main_log_level (int): log level for rank 0
        other_log_level (int): log level for other workers

    """
    if rank == 0:
        if log_file is not None:
            file_handler = FS.get_fs_client(log_file).get_logging_handler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            in_logger.addHandler(file_handler)
            in_logger.info(f"Running task with log file: {log_file}")
        in_logger.setLevel(main_log_level)
    else:
        in_logger.setLevel(other_log_level)
