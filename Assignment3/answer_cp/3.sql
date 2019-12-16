-- Select rows from a Table or View 'TableOrViewName' in schema 'SchemaName'
-- 3

SELECT yearid as years
FROM(
    (SELECT teamid, yearid
    FROM managers
    WHERE yearid >= 1975
    AND (yearid, w)
    IN(
        SELECT yearid, max(w) as w
        FROM managers
        GROUP BY yearid))
    INTERSECT
    (SELECT teamid, yearid
    FROM teams
    WHERE lgwin = 'Y')) MAXYEAR
ORDER BY yearid ASC;

