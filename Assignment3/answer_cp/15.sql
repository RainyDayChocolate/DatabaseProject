-- 15

SELECT first, last, birthcity AS city
FROM
    (SELECT DISTINCT playerid
    FROM(
        SELECT yearid, playerid, teamid
        FROM appearances) APPEAR
    JOIN(
        SELECT yearid, teamid
        FROM teams
        WHERE franchid='NYY') TEAMNAME
    ON TEAMNAME.yearid = APPEAR.yearid
    AND TEAMNAME.teamid = APPEAR.teamid) PLAYERINFO
JOIN
    (SELECT playerid, birthcity,
            namelast  AS last,
            namefirst AS first
    FROM master
    WHERE birthstate = 'NY') BIRTHINFO
ON PLAYERINFO.playerid = BIRTHINFO.playerid;