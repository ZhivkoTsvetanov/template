from __future__ import print_function
# Responsible for extensive logging of all related steps
from builtins import str
import datetime


def dump_log_to_console(log):
    print('\n'.join(log))


def log_current_def_name(def_name, log, log_level=' [INFO] '):
    __log_message(log, log_level, '\t <<<< %s >>>>' % def_name)


def info(log, message):
    __log_message(log, ' [INFO] \t\t\t', message)


def debug(log, message):
    __log_message(log, ' [DEBUG] \t\t\t', message)


def warn(log, message):
    __log_message(log, ' [WARN] \t\t\t', message)


def error(log, message):
    __log_message(log, ' [ERROR] \t\t\t', message)


def __log_message(log, log_level, message):
    now = datetime.datetime.now()
    stamp = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
    log.append(stamp + log_level + message)
