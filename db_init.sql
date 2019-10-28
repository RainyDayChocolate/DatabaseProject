CREATE TABLE IF NOT EXISTS weather (
    Date TIMESTAMP,
    City VARCHAR(63),
    humidity FLOAT,
    pressure FLOAT,
    temperature FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    weather_description VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS gunviolence (
    Date TIMESTAMP,
    State CHAR(2),
    City VARCHAR(63),
    Address VARCHAR(63),
    N_killed INT,
    N_injured INT,
    Congressional_district INT,
    N_guns_involved INT,
    State_house_district INT,
    State_senate_district INT
);
