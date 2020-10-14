import redis

RDSPW = 'admin798'


class Model(dict):
    """模型基类"""

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


redis_info = {
    'redis_0': redis.StrictRedis(
        connection_pool=redis.ConnectionPool(host="106.54.227.26", port=6379, db=0, password=RDSPW, decode_responses=True)),
    "redis_1": redis.StrictRedis(
        connection_pool=redis.ConnectionPool(host="106.54.227.26", port=6379, db=1, password=RDSPW, decode_responses=True)),
    'redis_2': redis.StrictRedis(
        connection_pool=redis.ConnectionPool(host="106.54.227.26", port=6379, db=2, password=RDSPW, decode_responses=True)),
    'redis_3': redis.StrictRedis(
        connection_pool=redis.ConnectionPool(host="106.54.227.26", port=6379, db=3, password=RDSPW, decode_responses=True)),
}

redis_con = Model(redis_info)


def connRedis():
    pool = redis.ConnectionPool(host='106.54.227.26', password=RDSPW, port=6379)
    # r=redis.Redis(connection_pool=pool)
    r = redis.StrictRedis(connection_pool=pool)
    r.set("name", "caoji")
    print(r.get('name'))


if __name__ == '__main__':
    """---test redis connection !---"""
    connRedis()
