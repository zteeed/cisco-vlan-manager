import redis
from structlog import get_logger

redis_app = redis.Redis(host='redis', port=6379, db=0)
log = get_logger()
