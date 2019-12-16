-- 2 issue
SELECT COUNT(*)
FROM
    (SELECT playerid
    FROM MASTER
    WHERE height < 72) HIGHT
JOIN(
    SELECT playerid, sum(h)/(sum(ab) * 1.0) as BA
    FROM(
        (SELECT playerid, ab, h, teamid
         FROM batting
         WHERE yearid = 2006)) PLAYER_STAT
    GROUP BY playerid, teamid
    HAVING (sum(ab) >0 AND sum(h)/(sum(ab) * 1.0) > .3)
    OR (sum(ab) = 0 AND sum(h) > 0)) ABSTAT
ON HIGHT.playerid = ABSTAT.playerid;

