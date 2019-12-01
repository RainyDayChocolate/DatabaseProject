"""This script connect basic"""
import csv
import os

import pandas as pd
import psycopg2
import psycopg2.extras


class App():

    def __init__(self):
        """Parent class that
            i) Initialize schema
            ii) Loading data to that schem
        """
        connection_string = """host='localhost'
                               dbname='project'
                               user='project'
                               password='project' """

        self.conn = psycopg2.connect(connection_string,
                                     cursor_factory=psycopg2.extras.DictCursor)

        with self.conn.cursor() as cursor:
            with open('./sqls/app_schema.sql', 'r') as project_schema:
                setup_queries = project_schema.read()
                cursor.execute(setup_queries)

            self.conn.commit()

    def load_data(self, path='../normalized_dataset'):
        # The sequence of this table should be determined by
        # constraints of all relations
        csv_tables = ['locations',
                      'accidents',
                      'accidentannotations',
                      'airports',
                      'flights',
                      'flightsoperations',
                      'delays',
                      'incidents',
                      'weathers']

        cur = self.conn.cursor()
        for csv_table in csv_tables:
            csv_table_path = os.path.join(path, csv_table)
            if csv_table == 'incidents':
                incidents = pd.read_csv(csv_table_path)
         #       incidents['participants'] = \
         #           incidents['participants'].apply(lambda s: eval(s))
                query = "insert into incidents values(" \
                            + "%s, " * 9 + "%s)"
                for _, record in incidents.iterrows():
                    cur.execute(query, record.values)
            else:
                with open(csv_table_path, 'r') as f:
                    next(f) # Skip the header row.
                    cur.copy_from(f, csv_table, sep=',')
            self.conn.commit()

    def query(self, query, parameters=()):
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

app = App()
app.load_data()
