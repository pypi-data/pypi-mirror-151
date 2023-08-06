import logging
import logging.handlers
import time
from util.global_var import *

# log_path是日志存放路径地址
get_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(os.path.dirname(get_path),'log')


# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):os.mkdir(log_path)
# 日志配置初始化
# def log_config_ini():
#     # 初始化日志对象
#     logger = logging.getLogger()
#
#     # 设置日志级别
#     logger.setLevel(logging.INFO)
#
#     # 创建控制台日志处理器
#     sh = logging.StreamHandler()
#
#     # 创建文件日志处理器
#     # 创建每日的日志文件
#     filename_day = PROJECT_ROOT_DIR + "/log/" + "interface_auto_test.%s.log" % time.strftime("%Y-%m-%d")
#     fh_day = logging.handlers.TimedRotatingFileHandler(filename_day, when='MIDNIGHT', interval=1, backupCount=3, encoding='utf-8')
#     # when: 时间单位， 可选参数
#     # interval: 时间间隔
#     # backupCount: 日志文件备份数量。 如果backupCount大于0， 那么当生成新的日志文件时，将只保留backupCount个文件， 删除最老的文件。
#
#     # 创建汇总日志文件
#     filename_all = PROJECT_ROOT_DIR + "/log/" + "interface_auto_test.log"
#     fh_all = logging.handlers.TimedRotatingFileHandler(filename_all, when='MIDNIGHT', interval=1, backupCount=3, encoding='utf-8')
#
#     # 设置日志格式，创建格式化器
#     fmt = '%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
#     formatter = logging.Formatter(fmt)
#
#     # 将格式化器设置到日志器中
#     sh.setFormatter(formatter)
#     fh_day.setFormatter(formatter)
#     fh_all.setFormatter(formatter)
#
#     # 6、将日志处理器添加到日志对象
#     logger.addHandler(sh)
#     logger.addHandler(fh_day)
#     logger.addHandler(fh_all)

class Log():
    def __init__(self):
        # 文件的命名
        self.now = time.strftime('%Y-%m-%d %H-%M-%S')
        self.logname = os.path.join(log_path,'{0}.log' .format(self.now))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self,level,message):

    # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname,"a",encoding='utf-8') # 追加模式
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == "info":
            self.logger.info(message)
        elif level == "debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)

        # 关闭打开的文件
        fh.close()

    def debug(self,message):
        self.__console("debug",message)

    def info(self,message):
        self.__console("info",message)
    def warning(self,message):
        self.__console("warning",message)
    def error(self,message):
        self.__console("error",message)

if __name__ == "__main__":
    logging.info("This is hippop man")

