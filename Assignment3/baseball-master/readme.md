# Readme

## Summary

The file `baseball-postgres.sql` is a Postgres version of the 2016 version of [Sean Lahman's Baseball Archive](http://www.seanlahman.com/baseball-archive/statistics/).

Both the file and this readme are licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.  For details see: [http://creativecommons.org/licenses/by-sa/3.0/](http://creativecommons.org/licenses/by-sa/3.0/)

## Process

I started by taking the [SQL Version](http://seanlahman.com/files/database/lahman2016-sql.zip) of the baseball archive and loading it into a MariaDB instance on my local system.

I then used [Pgloader](https://github.com/dimitri/pgloader) to load the database into Postgres, after which I used `pg_dump` to extract the SQL file.

## Setup

You need to create a `baseball` user in Postgres. You can run the `database-setup.sql` file to do that (or copy and paste the single line into a psql prompt). Then you need to run the `baseball-postgres.sql` file.

Something like:

```
psql -U postgres postgres < database-setup.sql
psql -U postgres postgres < baseball-postgres.sql

```

## Docker

I've added a basic Dockerfile which can be built (or extended) as needed. This image is not intended to be used in any sort of production capacity, only for testing/experimentation.

Once you've installed Docker, run:
```
docker pull samuelbjohnson/baseball-postgres

docker run --name baseball-post -e POSTGRES_PASSWORD=postgres -d samuelbjohnson/baseball-postgres
```

Then you can use `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' baseball-post` to find the IP address of the running container.

Connect to that container with psql: `psql -h <ip> -U baseball baseball`

There's also a read-only user (with only `SELECT` privileges): `baseball_reader` (with the password `baseball_reader`).

