DROP DATABASE IF EXISTS project;
CREATE DATABASE project;

DROP USER IF EXISTS project;
CREATE USER project WITH PASSWORD 'project';

GRANT ALL PRIVILEGES ON DATABASE project TO project;
ALTER USER project SET search_path = project;

