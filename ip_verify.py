import time
from proxy_redis import ProxyRedis
import asyncio
import aiohttp


async def verify_one(ip, sem, rds):
    timeout = aiohttp.ClientTimeout(total=10)
    async with sem:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.baidu.com/", proxy="http://" + ip, timeout=timeout) as resp:
                    await resp.text()
                    if resp.status in [200, 302]:
                        rds.set_max_score(ip)
                        print("{} is ok".format(ip))
                    else:
                        rds.desc_increase(ip)
                        print("{} is fail".format(ip))
        except Exception as e:
            rds.desc_increase(ip)
            print("{} is error, {}".format(ip, e))


async def main(rds):
    all_proxy_ip = rds.get_all_proxy_ip()
    sem = asyncio.Semaphore(30)
    tasks = []
    for ip in all_proxy_ip:
        tasks.append(asyncio.create_task(verify_one(ip, sem, rds)))
    if tasks:
        await asyncio.wait(tasks)


def run():
    rds = ProxyRedis()
    time.sleep(10)
    while 1:
        try:
            asyncio.run(main(rds))
        except Exception as e:
            print(e)
        time.sleep(120)


if __name__ == '__main__':
    run()
