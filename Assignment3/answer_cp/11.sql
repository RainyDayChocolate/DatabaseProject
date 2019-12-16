-- 11 issue

SELECT DISTINCT park
FROM
    (SELECT *
    FROM seriespost
    WHERE round like '%DS%') seriespost_CS
JOIN
    (SELECT yearid, teamid, park
    FROM teams
    WHERE park NOT LIKE '%Field%'
    AND park NOT LIKE '%field%'
    AND park NOT LIKE '%Park%'
    AND park NOT LIKE '%park%'
    AND park not LIKE '%stadium%'
    AND park NOT LIKE '%Stadium%') CONDITION_PARK
ON seriespost_CS.teamidwinner = CONDITION_PARK.teamid
AND seriespost_CS.yearid = CONDITION_PARK.yearid;
