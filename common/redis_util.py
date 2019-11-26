import redis


# 默认连测试环境redis
def get_conn(host='10.60.7.253', port=6379):
    return redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)


def get_str(key, conn=get_conn()):
    return conn.get(key)


def get_list(key, conn=get_conn()):
    return conn.lrange(key, 0, -1)


def get_hash(key, conn=get_conn()):
    return conn.hget(key)


def get_set(key, conn=get_conn()):
    return conn.smembers(key)


def get_zset(key, conn=get_conn()):
    return conn.zrangebyscore(key, 0, 100)
