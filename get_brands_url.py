import time

import requests
from bs4 import BeautifulSoup

from common import Common
from db import DBManagement as db
from get_all_brands_url import GetAllBrandsURL
from woker import Worker


class GetBrandsURL:

    @staticmethod
    def main(brand: dict):
        print(f'start crawling {brand["brand"]}')
        url = brand['url_address']
        brand = brand["brand"]
        re = requests.get(url)
        soup = BeautifulSoup(re.content, "html.parser")
        params = {
            'brand': brand,
            'url': url,
            're': re,
            'soup': soup
        }
        GetAllBrandsURL(params=params)

    def __init__(self):
        max_worker = Common.max_worker()
        brands_url = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[1], all_columns=True)
        for i in range(len(brands_url)):
            brand = {'brand': brands_url[i][1], 'url_address': brands_url[i][2]}
            self.main(brand)
            time.sleep(2)
        # Worker(fn=self.main, data=brands, max_worker=max_worker)
