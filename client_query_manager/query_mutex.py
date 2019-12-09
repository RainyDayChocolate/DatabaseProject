#! /usr/bin/env python3

from client_query_manager.query_list import Query_list
from client_query_manager.specific_queries import Specific_queries
from client_query_manager.query_type import Query_type

class Query_Mutex:
    '''
    This interface receives the requested state to change the 
    state of the query in run-time.
    '''
    queryType = None
    queryDict = dict()
    queryListInquirer = Query_list()
    query_inq = Specific_queries()

    def set_query_type(self, queryType):
        '''
        set the query type for subsequent logic selection
        '''
        self.queryType = queryType
    
    def getQueryList(self, queryType = None):
        if queryType is None:
            queryType = self.queryType

        self.queryListInquirer.create_query_set(queryType)
        return self.queryListInquirer.getQueryList()

    def get_query_request(self, request):
        '''
        Get the request phrase, so to activate the corresponding query action.
        @request: The selected phrase by the user. Format: String()
        '''
        self.query_inq.import_query_table( self.queryDict )
        self.query_inq.setQueryReq(request)
        return self.query_inq.getQueryResp()

    def __str__(self):
        if self.queryType is Query_type.CAREER_DEP_ARRV_DELAY_IN_AIRPORT:
            return 'About the career flights from / to airport in the US'
        elif self.queryType is Query_type.US_ACCIDENT_OCURRENCE:
            return 'About US accident occurences'
        elif self.queryType is Query_type.US_GUN_VIOLENCE:
            return 'About US gun violence'
        else:
            return 'Not in any query type'