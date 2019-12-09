from app.explorations import Explorations
from app.querier import Querier
from client_query_manager.query_mutex import *
from client_query_manager.specific_queries import Specific_queries

# GUI
from client_query_manager import custom_style_3
from pprint import pprint
from PyInquirer import prompt

'''
Please run with:
python3 -m client_query_manager
'''

if __name__=='__main__':
    print('client_query_manager is launched!!')

    # City, State
    sql_query = """
                SELECT city, state
                FROM locations ;
                """
    inquirer = Querier()
    city_state_tuple = inquirer.query_sql(sql_query)

    city_list = []
    for city, state in city_state_tuple:
        city_list.append( str(city + ', ' + state) )

    city_attrb = 'city'
    city_query = [
        {
            'type': 'list',
            'name': city_attrb,
            'message': 'Select the city to query',
            'choices': city_list,
            'filter': None
        }
    ] # End of questions

    picked_city = prompt( city_query, style = custom_style_3 )

    city_state_tuple = picked_city[ city_attrb ].split()
    city, state = city_state_tuple[0], city_state_tuple[1]
    
    # Choose the type of queries
    type_of_query = ['About the career flights from / to airport in the US',
                     'About US accident occurences',
                     'About US gun violence'
                    ]
    what_is_your_query_type = [
        {
            'type': 'rawlist',
            'name': 'type_of_queries',
            'message': 'What type of querry do you want?',
            'choices': type_of_query
        }
    ]

    picked_query_type = prompt( what_is_your_query_type, style = custom_style_3 )
    query_type = picked_query_type['type_of_queries']

    queryMutex = Query_Mutex()
    if query_type == type_of_query[0]:
        queryMutex.set_query_type(Query_type.CAREER_DEP_ARRV_DELAY_IN_AIRPORT)
    elif query_type == type_of_query[1]:
        queryMutex.set_query_type(Query_type.US_ACCIDENT_OCURRENCE)
    elif query_type == type_of_query[2] :
        queryMutex.set_query_type(Query_type.US_GUN_VIOLENCE)
    
    queryList = queryMutex.getQueryList()

    # Ask for specific query
    what_is_your_query = [
        {
            'type': 'list',
            'name': 'specific_query',
            'message': 'What is your particular query?',
            'choices': queryList
        }
    ]
    selected_query = prompt(what_is_your_query, style = custom_style_3)['specific_query']

    queryMutex.get_query_request(selected_query)
    
    

    

    