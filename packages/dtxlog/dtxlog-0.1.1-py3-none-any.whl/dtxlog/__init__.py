# coding: utf-8
import logging

from dtxlog.handlers import RedisListHandler

from dtxlog.config import LogOptions


def init(options=None):
  if options is None:
    options = LogOptions()
  logger = logging.getLogger()

  if options.LOG_LEVEL == "CRITICAL":
    logging.basicConfig(level=logging.CRITICAL)
  elif options.LOG_LEVEL == "ERROR":
    logging.basicConfig(level=logging.ERROR)
  elif options.LOG_LEVEL == "WARNING":
    logging.basicConfig(level=logging.WARNING)
  elif options.LOG_LEVEL == "INFO":
    logging.basicConfig(level=logging.INFO)
  else:
    logging.basicConfig(level=logging.DEBUG)

  logger.addHandler(RedisListHandler(
    key=options.REDIS_LOG_CONTAINER,
    host=options.REDIS_LOG_HOST,
    port=options.REDIS_LOG_PORT,
    password=options.REDIS_LOG_PASSWORD,
    level=options.LOG_LEVEL,
    options=options,
    # ssl=True
  ))

# Fatal
def f(msg, project_id=0):
  logger = logging.getLogger()
  _extra = {
    'project_id': project_id
  }
  logger.critical(msg, extra=_extra)
  pass


# Error
def e(msg, project_id=0):
  logger = logging.getLogger()
  _extra = {
    'project_id': project_id
  }
  logger.error(msg, extra=_extra)
  pass


# Warning
def w(msg, project_id=0):
  logger = logging.getLogger()
  _extra = {
    'project_id': project_id
  }
  logger.warning(msg, extra=_extra)
  pass


# Info
def i(msg, project_id=0):
  logger = logging.getLogger()
  _extra = {
    'project_id': project_id
  }
  logger.info(msg, extra=_extra)
  pass


# Debug
def d(msg, project_id=0):
  logger = logging.getLogger()
  _extra = {
    'project_id': project_id
  }
  logger.debug(msg, extra=_extra)
  pass
