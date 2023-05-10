from src.proxy_redis import ProxyRedis

from sanic import Sanic, json
from sanic_cors import CORS

app = Sanic("free_proxyip_pools")
CORS(app)

rds = ProxyRedis()


@app.route("/api/get_proxy_ip", methods=["GET"])
def get_proxy_ip(request):
    return json({"proxy_ip": rds.get_alive_proxy_ip()})


def run():
    app.run(host="0.0.0.0", port=18000)


if __name__ == "__main__":
    run()
