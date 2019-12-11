"""This class offers the connect to database
"""
import psycopg2
import psycopg2.extras
from lxml import etree


class Connector:

    def __init__(self):

        connection_string = """host='localhost'
                        dbname='project'
                        user='project'
                        password='project' """

        self.conn = psycopg2.connect(connection_string,
                                     cursor_factory=psycopg2.extras.DictCursor)
        xml_file = './xmls/incident_participants.xml'
        parser = etree.XMLParser(ns_clean=True)
        self.tree = etree.parse(xml_file, parser)
