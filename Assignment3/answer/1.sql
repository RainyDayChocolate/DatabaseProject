-- 1
SELECT COUNT(DISTINCT(playerid))
FROM(
    SELECT yearid, playerid
    FROM pitching
    WHERE yearid >= 1975
    GROUP BY yearid, playerid
    HAVING sum(sv) > 40) PLAYER;










