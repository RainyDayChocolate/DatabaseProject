CREATE USER baseball_reader WITH PASSWORD 'baseball_reader';
\connect baseball
GRANT SELECT ON ALL TABLES IN SCHEMA public TO baseball_reader;