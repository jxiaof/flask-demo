import os
import time

from flask import Flask, request, redirect, jsonify, abort

from allow_list import allow_ip
from db.base_db import redis_con

app = Flask(__name__)

rds = redis_con.redis_0
rds_1 = redis_con.redis_1
rds_2 = redis_con.redis_2
rds.set('foo', 200)
print("PID %d: initializing redis pool..." % os.getpid())
print(rds.get('foo'))
s = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
con = {v: k for k, v in enumerate(s)}

dump64 = lambda x: s[x % 64] if x // 64 == 0 else dump64(x // 64) + s[x % 64]
load64 = lambda x: sum([con[j] * 64 ** i for i, j in enumerate(x[::-1])])


def get_request_ip():
    '''获取请求方的ip'''
    try:
        ip = request.remote_addr
        print('------ ip = %s ------' % ip)
        return ip
    except Exception as e:
        print(e)


@app.route('/demo/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/demo/index')
def index_home():
    return '<h1>Hello Felix!</h1>'


@app.route('/demo/time')
def current_time():
    s = f"time: {time.time()}"
    return '<h1>' + s + '</h1>'


@app.route("/demo/index.html")
def index_html():
    return redirect("https://www.baidu.com/", code=301)


@app.route('/demo/dump', methods=['POST'])
def test_redis_write():
    """
    测试redis
    """
    url = ''
    short_url = ''
    try:
        url = request.json.pop("url", None)
        if url is None:
            abort(400, "error")
        if rds_1.exists(url):
            short_url = rds_1.get(url)
            msg = f"url already in use !"
            status_code = 200
        else:
            remote_ip = request.remote_addr if request.remote_addr else "anonymous"
            print(remote_ip)
            limit = rds_2.incr(str(remote_ip))
            if str(remote_ip) not in allow_ip and limit > 50:
                abort(403, "request too many times, has been denied access! ")
            count = rds.incr("count")
            print(f"total generate {count} short url !")
            data = dump64(count)
            rds.set(data, url)
           # short_url = f"http://127.0.0.1:5000/{data}/"
            short_url = f"http://{request.host}/{data}/"
            rds_1.set(url, short_url)
            status_code = 201
            msg = f"success"
    except Exception as e:
        print(e)
        msg = f"{e}"
        status_code = 400

    return jsonify({"msg": msg, "status_code": status_code,
                    "data": {"raw_url": url, "short_url": short_url}})


@app.route('/demo/load', methods=['GET'])
def test_redis_read():
    """
    测试redis
    """
    data = ''
    return data


@app.route('/<url>/', methods=['GET'])
def red(url):
    print("short url is : ", url)
    if rds.exists(url):
        return redirect(rds.get(url), code=301)
    else:
        return "<h1>failure !</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
