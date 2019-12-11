from client_query_manager.query_mutex import *
from client_query_manager.helper_class import Helper_class

'''
Please run with:
python3 -m client_query_manager
'''


def start_a_query():
    print('client_query_manager is launched!!')
    # Choose the type of queries
    type_of_query = ['About the career flights from / to airport in the US',
                     'About US accident occurences',
                     'About US gun violence'
                    ]
    helper = Helper_class()
    resp = helper.getAnswersFromQuestionSet([
        {
            'type': 'rawlist',
            'name': 'type_of_queries',
            'message': 'What type of querry do you want?',
            'choices': type_of_query
        }
    ])

    query_type = resp['type_of_queries']

    queryMutex = Query_Mutex()
    if query_type == type_of_query[0]:
        queryMutex.set_query_type(Query_type.CAREER_DEP_ARRV_DELAY_IN_AIRPORT)
    elif query_type == type_of_query[1]:
        queryMutex.set_query_type(Query_type.US_ACCIDENT_OCURRENCE)
    elif query_type == type_of_query[2] :
        queryMutex.set_query_type(Query_type.US_GUN_VIOLENCE)

    queryList = queryMutex.getQueryList()

    # Ask for specific query
    resp = helper.getAnswersFromQuestionSet([
        {
            'type': 'list',
            'name': 'specific_query',
            'message': 'What is your particular query?',
            'choices': queryList
        }
    ])
    queryMutex.get_query_request( resp['specific_query'] )


if __name__=='__main__':
    while True:
        start_a_query()


