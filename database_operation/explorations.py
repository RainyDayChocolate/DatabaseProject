"""Flight Delay Proportion(FROM A(input) ->B(input), Delay Reason-fix)
Carrier(Input) flight delay distribution vs. hour(weekday)
Average distance of each carrier from a certain airport(input)

Accident city top K street and its proportion and Right Side proportion.
Accident The average severity along hours in each weekday along (City, Weekday Input)

Incidents Occurancy Frequency of Each City(Input) in weekdays.
Incident state(input) -> suspect arrested ratio

Crossed Exploration
1.  top 5 weather description ratio for Long delay(Input Int) dep or arr(input)
in different cities.

2.  The avg accident occurancy and incident occurancy in a given city(input city)
    of weekdays.
in (Input rain, snow, cloud) days.

#3.  The flight (arr or dep) number and accident occuracy in weekday(Input city)

#4.  Average incident occurance along with(Input humidity, temperature, pressure)
    in city.
"""

import pandas as pd
from tabulate import tabulate

from .querier import Querier

float_to_percentage = lambda ratio: "{0:.2%}".format(ratio)

class Explorations(Querier):

    def __init__(self, **params):
        super().__init__(**params)

    def get_delay_ratio(self, dep, arr):
        delay_query = """
                        select delay_reason,
                               sum(delay) / sum(sum(delay)) over() as delay_ratio
                        from(
                            select flight_operation_id
                            from flightsoperations
                            where
                                dep = %s and
                                arr = %s and
                                arr_date > crs_arr_date
                            ) flght_dep_arr
                        join
                            delays
                        on flght_dep_arr.flight_operation_id = delays.flight_operation_id
                        group by delay_reason
                        order by delay_ratio;
                      """
        result = self.query_sql(delay_query, (dep, arr))
        for record in result:
            record[1] = float_to_percentage(record[1])
        result = tabulate(result, ['delay_reason', 'delay'])
        return result

    def get_carrier_delay_distribution(self, is_hour, carrier):
        """Time dimension only be restricted within 'Hour and Week'
        time_dimension: ) weekday
                        1 hour
        CARRIER
        """
        time_dimension = 'hour' if is_hour else 'ISODOW'
        distribution_query = \
            """
            select dep_datepart,
                    count(carrier) / sum(count(carrier)) over() as delay_ratio
            from
                (select extract(%s from crs_dep_date) as dep_datepart,
                        carrier
                from
                    flightsoperations
                where
                    carrier = %s) delay_datepart
            group by dep_datepart
            order by dep_datepart ASC;
            """
        result = self.query_sql(distribution_query, (time_dimension,
                                                     carrier))
        for record in result:
            record[1] = float_to_percentage(record[1])
        result = tabulate(result, [time_dimension, 'carrier_delay_ratio'])
        return result

    def get_carrier_avg_distance(self, airport):
        avg_distance = """
                        select carrier, AVG(distance) as avg_distance
                        from
                            flightsoperations
                        where
                            dep = %s
                        group by carrier
                        order by avg_distance;
                       """
        result = self.query_sql(avg_distance, (airport,))
        result = tabulate(result, ['carrier', 'distance'])
        return result

    def get_accident_street(self, city, state, K=5):
        side_ratio_query = """
                            select street,
                                   count(accident_id) as accident_num
                            from
                                accidents
                            where
                                city = %s and
                                state = %s
                            group by street
                            order by accident_num desc
                            limit %s
                           """
        params = (city, state, K)
        result = self.query_sql(side_ratio_query, params)
        result = tabulate(result, ['street', 'accident_num'])
        return result

    def get_avg_severity(self, city, state, weekday='Mon'):
        severity_query = """select hour,
                                   avg(severity) as avg_severity
                            from(
                                select date_part('hour', start_time) as hour,
                                    date_part('ISODOW',  start_time) as dow,
                                    severity
                                from
                                    accidents
                                where
                                    city = %s and
                                    state = %s) accident_distribution
                            where dow = %s
                            group by hour
                         """
        result = self.query_sql(severity_query, (city, state, weekday))
        result = tabulate(result, ['hour', 'avg_severtiy'], floatfmt='.3f')
        return result

    def get_gun_dayofweek_occurance(self, city, state):

        gun_query = """
                    select dow, count(incident_id) as occurance
                    from(
                        select date_part('ISODOW', date) as dow,
                                incident_id
                        from
                            incidents
                        where
                            city = %s and
                            state = %s) incident_dow
                    group by dow
                    order by dow
                    """
        result = self.query_sql(gun_query, (city, state))

        result = tabulate(result, ['dow', 'occurance'])
        return result

    def get_suspect_arrested_ratio(self, state='Texas'):
        incidents = """select incident_id
                       from incidents
                       where state = %s
                    """
        incidents = self.query_sql(incidents, (state,))
        incidents = [str(incident[0]) for incident in incidents]
        incidents = ' '.join(incidents)
        query_suspect = """count(incident
                                    [contains('{}', incident_id)]/
                                 participants/
                                 participant
                                    [type='Subject-Suspect'])""".format(incidents)

        query_suspect_arrested = """count(incident
                                            [contains('{}', incident_id)]/
                                          participants/
                                          participant
                                            [type='Subject-Suspect'
                                             and status/statu='Arrested'])
                                """.format(incidents)
        suspect_count = self.query_xml(query_suspect)
        arrested_suspect_count = self.query_xml(query_suspect_arrested)
        result = [[state, arrested_suspect_count / suspect_count]]
        for record in result:
                    record[1] = float_to_percentage(record[1])
        result = tabulate(result, ['state', 'arrest_ratio'])
        return result

    def get_delay_weather_description(self, airport, is_dep=True,  delay=20):
        dep_or_arr = 'dep' if is_dep else 'arr'
        dep_arr_date = 'dep_date' if is_dep else 'arr_data'
        delay_weather_query = \
            """
            select weather_description,
                    count(weathers.city) / sum(count(weathers.city)) over() as delay_ratio
            from
                (select city, state, date
                from(
                    select flights_delays.flight_operation_id,
                            {0} as airport,
                            date_trunc('hour', {1}) as date
                    from
                        FlightsOperations
                    join
                        (select flight_operation_id,
                                sum(delay) as delay
                        from
                            delays
                        group by flight_operation_id
                        having sum(delay) > %s) flights_delays
                    on flights_delays.flight_operation_id = FlightsOperations.flight_operation_id
                    where {0} = %s) delay_dates
                join
                    airports
                on airports.airport = delay_dates.airport) delay_city_dates
            join
                weathers
            on weathers.date = delay_city_dates.date and
                weathers.city = delay_city_dates.city and
                weathers.state = delay_city_dates.state
            group by weather_description
            order by delay_ratio desc;
            """.format(dep_or_arr, dep_arr_date)

        result = self.query_sql(delay_weather_query, (delay, airport))
        for record in result:
            record[1] = float_to_percentage(record[1])
        result = tabulate(result, ['weather_description', 'ratio'])
        return result
#2.  The average delay (dep or arr) who has the most(largest proportion) long-time(input) accidents"

    def get_avg_accident_with_weather(self, city, state, weather):
        accident_weather_query =\
            """
                select hour_weather_acc.hour,
                        cast(weather_accident_number as decimal) / accident_num
                from(
                    select hour,
                            count(accident_id) as weather_accident_number
                    from(
                        select date_part('hour', hour_date) as hour,
                                accident_id
                        from
                            (select accident_id,
                                date_trunc('hour', start_time) as hour_date
                            from
                                accidents
                            where city = %s and
                                  state = %s) city_accident
                        join
                            (select weather_description,
                                date
                            from
                                weathers
                            where city = %s and
                                  state = %s and
                                weather_description ~* %s) certain_weather
                        on city_accident.hour_date = certain_weather.date) city_weather_accidents
                    group by hour) hour_weather_acc
                join
                    (select hour, count(accident_id) as accident_num
                    from
                        (select date_part('hour', start_time) as hour,
                                accident_id
                        from
                            accidents
                        where city = %s and
                              state = %s) hour_accident
                    group by hour) city_accidents
                on hour_weather_acc.hour = city_accidents.hour
                order by hour asc;
                """
        params = (city, state, city, state, weather, city, state)
        result = self.query_sql(accident_weather_query, params)
        for record in result:
            record[1] = float_to_percentage(record[1])
        result = tabulate(result, ['hour', 'ratio'])
        return result

    def  get_accident_incident_severity(self):

        query = """
                select avg_acc_severity.city, avg_acc_severity.state,
                       avg_sev, avg_incident_sev, incident_occurance
                from
                    (select city, state,
                        avg(severity) as avg_sev
                    from
                        accidents
                    group by (city, state)) avg_acc_severity
                join(
                    select city, state,
                        avg(killed_num) + avg(injured_num) as avg_incident_sev,
                        count(incident_id) as incident_occurance
                    from
                        incidents
                    group by (city, state)) avg_inc_severity
                on avg_acc_severity.city = avg_inc_severity.city and
                   avg_acc_severity.state = avg_inc_severity.state
                order by avg_sev
                """
        result = self.query_sql(query)
        result = tabulate(result,
                          ['city', 'state', 'avg_accident_severity',
                           'avg_incident_severity', 'incident_occurance'],
                           floatfmt='.2f')
        return result






