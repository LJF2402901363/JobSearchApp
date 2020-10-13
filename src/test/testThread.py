# coding: utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def spider(page):
    time.sleep(page)
    print(f"crawl task{page} finished")
    return page


def main():
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        for page in range(1, 5):
            obj = t.submit(spider, page)
            obj_list.append(obj)

        for future in as_completed(obj_list):
            data = future.result()
            print(f"main: {data}")


if __name__ == '__main__':
    main()
