-- 13

SELECT namefirst,
       namelast
FROM
    master
RIGHT JOIN
    (SELECT REC_SEC.playerid
    FROM
        (SELECT yearid, playerid, ab, h
        FROM batting
        WHERE stint = 1) REC_FIR
    JOIN
        (SELECT yearid, playerid, ab, h
        FROM batting
        WHERE stint = 2) REC_SEC
    ON REC_FIR.yearid = REC_SEC.yearid
    AND REC_FIR.playerid = REC_SEC.playerid
    WHERE REC_FIR.ab < REC_SEC.ab
    AND REC_FIR.h > REC_SEC.h) MANY_RECORD
ON master.playerid=MANY_RECORD.playerid
ORDER BY substring(namelast, 1, 4), substring(namelast, 5, 7) ASC, namefirst ASC;
