
from .db_connect import Connector


class Querier(Connector):

    def __init__(self, **params):
        super().__init__(**params)

    def query_sql(self, query, parameters=None):
        if not parameters:
            parameters = tuple()
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    def query_xml(self, query):
        return self.tree.xpath(query)