import random
from redis import Redis
from settings import REDIS_HOST, REDIS_PORT, REDIS_DB


class ProxyRedis:
    def __init__(self):
        self.redis = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

    def add_proxy_ip(self, ip):
        if not self.redis.zscore('proxy_ip', ip):
            self.redis.zadd('proxy_ip', {ip: 10})

    def get_all_proxy_ip(self):
        return self.redis.zrange('proxy_ip', 0, -1)

    def set_max_score(self, ip):
        self.redis.zadd('proxy_ip', {ip: 100})

    def desc_increase(self, ip):
        score = self.redis.zscore('proxy_ip', ip)
        if score and score > 0:
            self.redis.zincrby('proxy_ip', -1, ip)
        else:
            self.redis.zrem('proxy_ip', ip)

    def get_alive_proxy_ip(self):
        ips = self.redis.zrangebyscore('proxy_ip', 100, 100, 0, -1)
        if not ips:
            ips = self.redis.zrangebyscore('proxy_ip', 11, 99, 0, -1)
            if not ips:
                return None
        return random.choice(ips)
