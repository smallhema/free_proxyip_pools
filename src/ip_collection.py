import time

from src.proxy_redis import ProxyRedis
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36'
}


def get_kuai_ip(rds):
    url = 'https://www.kuaidaili.com/free/intr/{}/'
    for i in range(1, 3):
        sub_url = url.format(i)
        response = requests.get(sub_url, headers=headers)
        tree = etree.HTML(response.text)
        trs = tree.xpath('//table/tbody/tr')
        for tr in trs:
            ip = tr.xpath('./td[1]/text()')[0]
            port = tr.xpath('./td[2]/text()')[0]
            proxy_ip = '{}:{}'.format(ip, port)
            rds.add_proxy_ip(proxy_ip)
        time.sleep(2)


def get_89_ip(rds):
    url = 'https://www.89ip.cn/index_1.html'
    for i in range(1, 3):
        sub_url = url.format(i)
        response = requests.get(sub_url, headers=headers)
        tree = etree.HTML(response.text)
        trs = tree.xpath('//table//tr')[1:]
        for tr in trs:
            ip = tr.xpath('./td[1]/text()')[0].strip()
            port = tr.xpath('./td[2]/text()')[0].strip()
            proxy_ip = '{}:{}'.format(ip, port)
            rds.add_proxy_ip(proxy_ip)
        time.sleep(2)


def run():
    rds = ProxyRedis()
    while 1:
        try:
            get_kuai_ip(rds)
            get_89_ip(rds)
        except Exception as e:
            print(e)
        time.sleep(60)


if __name__ == '__main__':
    run()
