#! /usr/bin/env python3

from client_query_manager.query_list import Query_list
from client_query_manager.specific_queries import Specific_queries
from client_query_manager.query_type import Query_type
from client_query_manager.helper_class import Helper_class

class Query_Mutex:
    '''
    This interface receives the requested state to change the 
    state of the query in run-time.
    '''
    queryType = None
    queryDict = dict()
    queryListInquirer = Query_list()

    def set_query_type(self, queryType = None):
        '''
        set the query type for subsequent logic selection. The queryType is in enum format
        @ queryType : String. 
        '''
        if not queryType:
            raise Exception( 'There is input queryType. queryType must be an enum' )

        self.queryType = queryType
        self.queryListInquirer.create_query_set( self.queryType )
        self.queryDict = self.queryListInquirer.getQueryHashTable()
    
    def getQueryList(self):
        return self.queryListInquirer.getQueryList()

    def get_query_request(self, request):
        '''
        Get the request phrase, so to activate the corresponding query action.
        @request: The selected phrase by the user. Format: String
        '''
        queryKey = Helper_class().getKey_from_dict(self.queryDict, request)

        query_inq = Specific_queries()
        query_inq.import_query_table( self.queryDict )

        query_inq.sendQueryReq(queryKey)

    def __str__(self):
        if self.queryType is Query_type.CAREER_DEP_ARRV_DELAY_IN_AIRPORT:
            return 'About the career flights from / to airport in the US'
        elif self.queryType is Query_type.US_ACCIDENT_OCURRENCE:
            return 'About US accident occurences'
        elif self.queryType is Query_type.US_GUN_VIOLENCE:
            return 'About US gun violence'
        else:
            return 'Not in any query type'