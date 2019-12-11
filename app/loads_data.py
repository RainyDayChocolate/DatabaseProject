"""This script connect basic"""
import csv
import os

import pandas as pd

from app.db_connect import Connector

class Loader(Connector):

    def __init__(self):
        """Parent class that
            i) Initialize schema
            ii) Loading data to that schem
        """
        super().__init__()

    def create_schema(self):
        with self.conn.cursor() as cursor:
            with open('./sqls/app_schema.sql', 'r') as project_schema:
                setup_queries = project_schema.read()
                cursor.execute(setup_queries)
            self.conn.commit()

    def load_data(self, path='./normalized_dataset'):
        # The sequence of this table should be determined by
        # constraints of all relations
        csv_tables = ['locations',
                      'carriers',
                      'accidents',
                      'accidentannotations',
                      'airports',
                      'flightsoperations',
                      'delays',
                      'incidents',
                      'weathers']

        cur = self.conn.cursor()
        for csv_table in csv_tables:
            csv_table_path = os.path.join(path, csv_table)
            if csv_table == 'incidents':
                incidents = pd.read_csv(csv_table_path)
                incidents = incidents.drop(columns=['participants'])
                query = "insert into incidents values(" \
                            + "%s, " * 8 + "%s)"
                for _, record in incidents.iterrows():
                    cur.execute(query, record.values)

            else:
                with open(csv_table_path, 'r') as f:
                    next(f) # Skip the header row.
                    cur.copy_from(f, csv_table, sep=',')

            self.conn.commit()


if __name__ == '__main__':
    app = Loader()
    app.create_schema()
    app.load_data()
