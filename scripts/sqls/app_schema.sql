DROP SCHEMA IF EXISTS project CASCADE;

CREATE SCHEMA project;
-- GRANT ALL PRIVILEGES ON SCHEMA;
-- The most important thing here is. We should modify 
CREATE TABLE Locations(
    city varchar(31),
    state_abr char(2),
    state varchar(31)
    );

CREATE TABLE Accidents(
    accident_id varchar(16),
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
    primary key(accident_id)
    );

CREATE TABLE AccidentAnnotations(
    accident_id varchar(16) references Accidents(accident_id),
    annotation varchar(16)
    );

CREATE TABLE Airports(
    city varchar(31),
    state_abr char(2),
    airport char(3),
    primary key(airport)
    );

CREATE TABLE Flights(
    carrier char(2),
    flight_num varchar(4),
    dep char(3) references Airports (airport),
    arr char(3) references Airports (airport));

CREATE TABLE FlightsOperations(
    flight_operation_id int  ,
    carrier char(2),
    flight_num varchar(4),
    crs_dep_date timestamp,
    dep_date timestamp,
    crs_arr_date timestamp,
    arr_date timestamp,
    crs_elapsed_time decimal(5),
    actual_elapsed_time decimal(5),
    air_time decimal(5),
    distance decimal(5),
    primary key (flight_operation_id));

CREATE TABLE Delays(
    flight_operation_id int references FlightsOperations(flight_operation_id),
    delay_reason varchar(15),
    delay decimal(5));

CREATE TABLE Incidents(
    incident_id int,
    date timestamp,
    city varchar(31),
    state varchar(31),
    address text,
    state_house_district int,
    killed_num int,
    injured_num int,
    n_guns_involved int,
    participants json);

CREATE TABLE Weathers(
    city varchar(31),
    state varchar(31),
    date timestamp,
    humidity float,
    pressure float,
    temperature float,
    wind_speed float,
    wind_direction float,
    weather_description text);

