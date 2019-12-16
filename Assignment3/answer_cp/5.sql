-- 5
SELECT franchname, attendance
FROM(
    SELECT franchid, AVG(attendance) AS attendance
    FROM(
        SELECT yearid, franchid, attendance::integer
        FROM teams
        WHERE attendance <> ''
        AND yearid >= 1997) CLEANED
    GROUP BY franchid) ATTID
    JOIN teamsfranchises
    ON (ATTID.franchid = teamsfranchises.franchid);
