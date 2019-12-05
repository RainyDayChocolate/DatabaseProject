
from .loads_data import Loader


class Querier(Loader):

    def __init__(self, **params):
        super().__init__(**params)

    def query_sql(self, query, parameters=()):
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    def query_xml(self, query):
        return self.tree.xpath(query)