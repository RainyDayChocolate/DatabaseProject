from .explorations import Explorations

if __name__ == '__main__':
    explore = Explorations()
    print(explore.get_delay_ratio('ATL', 'DEN'))
    print(explore.get_carrier_delay_distribution('hour', 'DL'))
    print(explore.get_carrier_avg_distance('DEN'))
    print(explore.get_accident_street_side_ratio('San Francisco', 'California'))
    print(explore.get_avg_severity('San Francisco', 'California', weekday=1))
    print(explore.get_gun_dayofweek_occurance('Chicago', 'Illinois'))
    print(explore.get_suspect_arrested_ratio())
    print(explore.get_delay_weather_description('JFK'))
    print(explore.get_avg_accident_with_weather('San Francisco', 'Rain'))