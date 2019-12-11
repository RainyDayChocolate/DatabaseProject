
--TODO CREATE INDEX for tables
DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;

CREATE TABLE Locations( -- add unneccsary information.
    city varchar(31),
    state_abr char(2),
    state varchar(31),
    unique (city, state)
    );

CREATE TABLE Carriers(
    carrier char(2),
    carrier_name varchar(31),
    unique (carrier)
    );

CREATE INDEX city_name
ON Locations(city);

CREATE TABLE Accidents(
    accident_id varchar(16) primary key,
    city varchar(31),
    state varchar(31),
    street text,
    severity int,
    start_time timestamp,
    end_time timestamp,
    distance decimal(3),
    side char(1),
    visibility decimal(3),
    weather_condition text,
    sunrise_sunset varchar(5),
    foreign key (city, state)
        references Locations(city, state)
    );

CREATE INDEX idx_city
on Accidents(city);

CREATE TABLE AccidentAnnotations(
    accident_id varchar(16)
        references Accidents(accident_id),
    annotation varchar(16)
    );

CREATE INDEX idx_annotation
ON AccidentAnnotations(annotation);

CREATE TABLE Airports(
    city varchar(31),
    state varchar(31),
    airport char(3),
    primary key (airport),
    foreign key (city, state)
        references Locations (city, state)
    );


CREATE TABLE FlightsOperations(
    flight_operation_id int primary key,
    carrier char(2) references Carriers(carrier),
    flight_num varchar(4),
    dep char(3) references Airports(airport),
    arr char(3) references Airports(airport),
    crs_dep_date timestamp,
    dep_date timestamp,
    crs_arr_date timestamp,
    arr_date timestamp,
    crs_elapsed_time decimal(5),
    actual_elapsed_time decimal(5),
    air_time decimal(5) check(air_time >= 0),
    distance decimal(5) check(distance > 0)
    );

CREATE INDEX idx_dep_arr
ON FlightsOperations(dep, arr);

CREATE TABLE Delays(
    flight_operation_id int
        references FlightsOperations(flight_operation_id),
    delay_reason varchar(15),
    delay decimal(5) check(delay > 0)
    );

CREATE INDEX reason_idx
ON Delays(delay_reason);

CREATE TABLE Incidents(
    incident_id int,
    date timestamp,
    city varchar(31),
    state varchar(31),
    address text,
    state_house_district int,
    killed_num int check(killed_num >=0 ),
    injured_num int check(injured_num >= 0),
    n_guns_involved int check(n_guns_involved >= 0),
    foreign key(city, state)
        references Locations(city, state)
    );

CREATE INDEX idx_city_date_incidents
ON Incidents(date, city);

CREATE TABLE Weathers(
    city varchar(31),
    state varchar(31),
    date timestamp,
    humidity float,
    pressure float,
    temperature decimal(3),
    wind_speed float,
    wind_direction float,
    weather_description text,
    foreign key(city, state)
        references Locations(city, state)
);

CREATE INDEX idx_city_date_weather
ON Weathers(date, city);

GRANT ALL PRIVILEGES ON Locations, Accidents, AccidentAnnotations,
Airports, FlightsOperations, Delays, Incidents, Weathers,Carriers TO project;