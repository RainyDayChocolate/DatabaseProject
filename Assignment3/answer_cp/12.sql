-- 12
SELECT name
FROM (
    SELECT TEAMNAME.teamid, TEAMNAME.yearid, name
    FROM
        (SELECT teamid, yearid, name
        FROM teams) TEAMNAME
    JOIN(
        SELECT teamidloser AS teamid,
                yearid
        FROM seriespost
        WHERE round like '%CS') LOSER
    ON TEAMNAME.teamid = LOSER.teamid
    AND TEAMNAME.yearid = LOSER.yearid) LOSE_RECORD
GROUP BY name
HAVING count(yearid) > 2;


