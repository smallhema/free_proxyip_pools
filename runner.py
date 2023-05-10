from ip_api import run as api_run
from ip_collection import run as collection_run
from ip_verify import run as verify_run
from multiprocessing import Process


def run():
    p1 = Process(target=api_run)
    p2 = Process(target=collection_run)
    p3 = Process(target=verify_run)
    p1.start()
    p2.start()
    p3.start()


if __name__ == '__main__':
    run()
