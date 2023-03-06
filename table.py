class Table:

    @staticmethod
    def main(soup):
        price_table = soup.find_all(class_='p-tile product_tile')
        variants = []
        for variant in price_table:
            variant_ = {
                'msrp': variant['data-msrp'],
                'price': variant['data-price'],
                'product_name': variant['data-product-name']
            }
            variants.append(variant_)
        return variants
