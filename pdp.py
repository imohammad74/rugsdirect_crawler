import requests
from bs4 import BeautifulSoup

from db import DBManagement as db
from pdp_elements import PDPElements
from table import PriceTable


class PDP:
    @staticmethod
    def main(url: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # features = list(PDPElements().features(soup).keys())
        # feature_values = PDPElements.feature_value(soup)
        variants = PriceTable.main(soup)
        brand = PDPElements.brand(soup)
        title = PDPElements.title(soup)
        description = PDPElements.description(soup)
        design_id = PDPElements().design_id(soup)
        # image_urls = PDPElements.images_product(url, soup, download_image=False)
        for variant in variants:
            size = PDPElements.shape_size(soup)[variants.index(variant)][0]
            msrp = variant['msrp']
            sale_price = variant['price']
            all_columns = [
                {'column': 'title', 'value': title},
                {'column': 'description', 'value': description},
                {'column': 'url', 'value': url},
                {'column': 'size', 'value': size},
                {'column': 'brand', 'value': brand},
                {'column': 'msrp', 'value': msrp},
                {'column': 'design_id', 'value': design_id},
                {'column': 'sale_price', 'value': sale_price}
            ]
            try:
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2], columns=all_columns)
            except:
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                               columns=[{'column': 'url', 'value': url}])
        print(f'"{title}" finish!')

    def __init__(self, url: str):
        self.main(url)
