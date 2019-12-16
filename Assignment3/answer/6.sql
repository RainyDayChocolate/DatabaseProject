-- 6

SELECT master.namefirst AS first,
       master.namelast  AS last,
       APPEAR.appearance AS appearances
FROM((
    SELECT playerid, count(yearid) AS appearance
    FROM allstarfull
    WHERE playerid in(
        SELECT playerid
        FROM halloffame
        WHERE yearid = 2000
        AND category = 'Player')
    GROUP BY playerid) APPEAR
    JOIN
    master
    ON (master.playerid = APPEAR.playerid)
    )
ORDER BY APPEAR.appearance DESC, LAST
LIMIT 10;
