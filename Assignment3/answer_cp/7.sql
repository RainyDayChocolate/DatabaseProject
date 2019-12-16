-- 7

SELECT playerid, career_avg
FROM(
    SELECT playerid,
            SUM(h)           AS SH,
            SUM(ab)          AS SAB,
            SUM(h) / SUM(ab) AS career_avg
    FROM batting
    GROUP BY playerid) STAT
where SAB > 100 and playerid in(
    SELECT playerid
    FROM master
    WHERE birthyear = 1972)
ORDER BY career_avg DESC;
