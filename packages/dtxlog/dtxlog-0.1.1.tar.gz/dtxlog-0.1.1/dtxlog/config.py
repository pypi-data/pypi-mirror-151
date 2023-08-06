import logging

from pydantic import BaseSettings


class LogOptions(BaseSettings):
  LOG_LEVEL: int = logging.DEBUG
  DTX_DOMAIN_ID: int = 0
  DTX_SERVICE_NAME: str = ''
  DTX_OS_ENV: str = 'dev'
  DTX_OWNER: str = 'U01G32UDG2J'
  REDIS_LOG_HOST: str = ''
  REDIS_LOG_PASSWORD: str = ''
  REDIS_LOG_PORT: int = 6379
  REDIS_LOG_CONTAINER: str = "logContainer"

  class Config:
    env_file = '.env'
