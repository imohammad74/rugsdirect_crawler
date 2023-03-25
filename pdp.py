import time
import requests
from bs4 import BeautifulSoup
from db import DBManagement as db
from pdp_elements import PDPElements
from table import PriceTable
from common import Common


class PDP:
    @staticmethod
    def main(data):
        url = data[0]
        print(url)
        brand = data[1]
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if PDPElements.is_in_stock(soup):
            features = Common.remove_quotes(PDPElements().features_title(soup))
            feature_values = Common.remove_quotes(PDPElements.feature_value(soup))
            variants = PriceTable.main(soup)
            title = Common.remove_quotes(PDPElements.title(soup))
            collection = Common.remove_quotes(PDPElements().collection(soup))
            description = Common.remove_quotes(PDPElements.description(soup))
            design_id = Common.remove_quotes(PDPElements().design_id(soup))
            construction = Common.remove_quotes(feature_values[(features.index('Construction'))])
            material = Common.remove_quotes(feature_values[(features.index('Material'))])
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
                    {'column': 'weave', 'value': construction},
                    {'column': 'material', 'value': material},
                    {'column': 'msrp', 'value': msrp},
                    {'column': 'collection', 'value': collection},
                    {'column': 'design_id', 'value': design_id},
                    {'column': 'sale_price', 'value': sale_price}
                ]
                try:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2], columns=all_columns)
                    # print(all_columns)
                except:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                   columns=[{'column': 'url', 'value': url}])
                    # print('error')
            print(f'"{title}" finish!')
        else:
            print('Product is out of stock')
            query = f'''INSERT INTO NoData (URLAddress, ErrorMsg) VALUES ('{url}', 'Out of stock')'''
            db.custom_query(db_file=db.db_file(), query=query)

    def __init__(self, data):
        time.sleep(2)
        self.main(data)
