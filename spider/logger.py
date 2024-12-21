import logging
from colorama import Fore, Style, init # type: ignore


# 自定义一个带颜色的formatter


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_no = record.levelno
        if level_no >= 50:  # CRITICAL
            color = Fore.RED + Style.BRIGHT
        elif level_no >= 40:  # ERROR
            color = Fore.RED
        elif level_no >= 30:  # WARNING
            color = Fore.YELLOW
        elif level_no >= 20:  # INFO
            color = Fore.GREEN
        elif level_no >= 10:  # DEBUG
            color = Fore.CYAN
        else:
            color = Fore.WHITE
        record.msg = color + record.msg + Style.RESET_ALL
        return super().format(record)


def get_logger(name, level=None):
    init(autoreset=True)  # 初始化colorama，设置自动重置颜色

    # 创建一个logger
    logger = logging.getLogger(name)
    logger.setLevel(level or logging.DEBUG)

    # 创建一个handler，用于写入到控制台
    handler = logging.StreamHandler()
    handler.setLevel(level or logging.DEBUG)

    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    logger = get_logger('a')
    # 使用logger
    logger.debug("这是一个debug信息")
    logger.info("这是一个info信息")
    logger.warning("这是一个warning信息")
    logger.error("这是一个error信息")
