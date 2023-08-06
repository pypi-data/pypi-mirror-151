# coding: utf-8
import logging
import redis
from ._compat import json

from .formatters import JSONFormatter


class RedisHandler(logging.Handler):
  def __init__(self, container, redis_client=None,
               formatter=JSONFormatter(),
               level=logging.NOTSET, **redis_kwargs):
    logging.Handler.__init__(self, level)
    self.container = container
    self.redis_client = redis_client or redis.Redis(**redis_kwargs)
    self.formatter = formatter

  def emit(self, record):
    try:
      self.redis_client.lpush(self.container, self.format(record))
    except redis.RedisError:
      pass


class RedisListHandler(logging.Handler):

  def __init__(self, key, max_messages=None, redis_client=None,
               formatter=JSONFormatter(), ttl=None,
               options=None,
               level=logging.NOTSET, **redis_kwargs):
    logging.Handler.__init__(self, level)
    self.key = key
    self.redis_client = redis_client or redis.Redis(**redis_kwargs)
    self.formatter = formatter
    self.max_messages = max_messages
    self.ttl = ttl
    self.options = options

  def emit(self, record):
    label = []
    label.append(str(self.options.DTX_DOMAIN_ID))
    label.append(str(record.project_id))
    label.append(self.options.DTX_SERVICE_NAME)
    label.append(self.options.DTX_OS_ENV)
    label.append(self.options.REDIS_LOG_CONTAINER)
    msg = {
      "level": "debug",
      "message": record.msg,
      "meta": {
        "label": label,
        "timestamp": int(record.created)
      }
    }

    try:
      if self.max_messages:
        p = self.redis_client.pipeline()
        p.lpush(self.key, self.format(record))
        p.ltrim(self.key, -self.max_messages, -1)
        p.execute()
      else:
        self.redis_client.lpush(self.key, json.dumps(msg))
      if self.ttl:
        self.redis_client.expire(self.key, self.ttl)
    except redis.RedisError:
      pass
