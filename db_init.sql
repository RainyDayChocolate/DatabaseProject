CREATE TABLE IF NOT EXISTS weather (
    Date TIMESTAMP,
    City VARCHAR(31),
    humidity FLOAT,
    pressure FLOAT,
    temperature FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    weather_description VARCHAR(32),
    PRIMARY KEY(Date, City)
);

CREATE TABLE IF NOT EXISTS gunviolence (
    id INT,
    Date TIMESTAMP,
    State CHAR(2),
    City VARCHAR(31),
    Address VARCHAR(63),
    N_killed INT,
    N_injured INT,
    Congressional_district INT,
    N_guns_involved INT,
    State_house_district INT,
    State_senate_district INT,
    PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS flight(
    Date TIMESTAMP,
    Unique_carrier char(2),
    Fl_num INT,
    Dep_airport_id INT,
    Dep_city VARCHAR(31),
    Dep_state CHAR(2),
    Dest_airport_id INT,
    Dest_city VARCHAR(31),
    Dest_state CHAR(2),
    Dep_time TIMESTAMP,
    Dep_delay INT,
    Arr_time TIMESTAMP,
    Arr_delay INT,
    Crs_elapsed_time INT,
    Actual_elapsed_time INT,
    Carrier_delay INT,
    Weather_delay INT,
    Nas_delay INT,
    Security_delay INT,
    Late_aircraft_delay INT,
    PRIMARY KEY(Date, Fl_num)
);

CREATE TABLE IF NOT EXISTS accident(
    Severity INT,
    Start_Time INT,
    City VARCHAR(31),
    State CHAR(2),
    Zipcode CHAR(5),
    Bump BOOLEAN,
    Crossing BOOLEAN,
    Give_Way BOOLEAN,
    Junction BOOLEAN,
    No_Exit BOOLEAN,
    Railway BOOLEAN,
    Roundabout BOOLEAN,
    Station BOOLEAN,
    Stop BOOLEAN,
    Traffic_Calming BOOLEAN,
    Traffic_Signal BOOLEAN,
    Turning_Loop BOOLEAN,
    Sunrise_Sunset CHAR(5),
    PRIMARY KEY(Start_Time, City)
);


