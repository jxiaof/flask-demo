import redis

# 获取redis数据库连接
r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
print("连接redis成功!")
# redis存入键值对
r.set(name="key", value="value")
# 读取键值对
print(r.get("key"))
# 删除
print(r.delete("key"))

# redis存入Hash值
r.hset(name="name", key="key1", value="value1")
r.hset(name="name", key="key2", value="value2")
# 获取所有哈希表中的字段
print(r.hgetall("name"))
# 获取所有给定字段的值
print(r.hmget("name", "key1", "key2"))
# 获取存储在哈希表中指定字段的值。
print(r.hmget("name", "key1"))
# 删除一个或多个哈希表字段
print(r.hdel("name", "key1"))

# 过期时间
r.expire("name", 60)  # 60秒后过期
