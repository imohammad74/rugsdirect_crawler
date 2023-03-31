from db import DBManagement as db


class PriceCheckWithSource:
    @staticmethod
    def get_source_data() -> list:
        source = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[6],
                                all_columns=False, columns=['CollectionName', 'DesignID', 'Shape', 'Size'])
        for i in range(len(source)):
            my_tuple = source[i]
            for j in range(len(my_tuple)):
                source[i] = tuple(s.lower().replace(' ', '-') for s in my_tuple if s is not None)
        return source

    @staticmethod
    def get_crawl_data() -> list:
        source = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[2],
                                all_columns=False, columns=['collection', 'design_id', 'shape', 'size'])
        for i in range(len(source)):
            my_tuple = source[i]
            for j in range(len(my_tuple)):
                source[i] = tuple(s.lower().replace(' ', '-') for s in my_tuple if s is not None)
        return source
