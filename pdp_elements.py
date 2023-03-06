import os

import requests

from common import Common
from table import Table


class PDPElements:

    @staticmethod
    def page_is_exist(soup):
        if soup.find(class_='OneColumn _404'):
            return False
        else:
            return True

    @staticmethod
    def title(soup):
        """get title of pdp"""
        title = soup.find(class_='pdp-title').text
        print(title)
        return title

    @staticmethod
    def description(soup):
        desc = soup.find(class_='product-overview-data').text
        print(desc)
        return desc

    @staticmethod
    def features_title(soup):
        content = soup.find_all(class_='rug-features-left')
        titles = [title.text for title in content]
        print(titles)
        return titles

    @staticmethod
    def feature_value(soup):
        content = soup.find_all(class_='rug-features-right')
        values = [value.text for value in content]
        print(values)
        return values

    def features(self, soup):
        titles = self.features_title(soup)
        values = self.feature_value(soup)
        features = [{'title': titles[i], 'value': values[i]} for i in range(len(titles))]
        return features

    @staticmethod
    def images_product(url: str, soup: str, download_image: bool):
        images = soup.find_all('a', {'class': 'thumbnail'})
        main_url = 'https://www.rugstudio.com'
        image_links = [f'{main_url}{image.get("href")}' for image in images if '.aspx' not in image]
        cnt = 0
        sku = Table.body(url, soup)[0]['Item #'].split('x')[0]
        path = f'{sku}'
        if download_image:
            for image in image_links:
                cnt += 1
                r = requests.get(image, allow_redirects=True, timeout=15)
                is_exist = os.path.exists(path)
                image_size = requests.head(image)
                image_format = image_size.headers.get('content-type').split('/')[-1]
                if not is_exist:
                    os.makedirs(path)
                if '.aspx' not in image:
                    file = open(f'{path}/{sku}-{cnt}.{image_format}', 'wb').write(r.content)
        else:
            return image_links

    @staticmethod
    def find_variant_url(soup: str, main_url: str):
        content = soup.find_all('a', {'data-slide-id': "slide-ac"})
        variant_url = list(set([f'{main_url}{url["href"]}' for url in content]))
        return variant_url

    def design_id(self, soup, pattern_id: str):
        title = self.title(soup)
        collection_name = self.features(soup)['Collection']
        if pattern_id == '1':
            Common.design_id_pattern_i(title)
        elif pattern_id == '2':
            Common.design_id_pattern_ii(title=title, brand=title.split(' ')[0], collection_name=collection_name)
        else:
            return 'Not found'

# todo:design id
