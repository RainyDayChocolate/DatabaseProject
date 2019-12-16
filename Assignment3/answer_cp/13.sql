-- 13

SELECT namefirst as first,
       namelast as last
FROM master
WHERE playerid IN (
    SELECT REC_SEC.playerid
    FROM
        (SELECT yearid, playerid, ab, h
        FROM batting
        WHERE stint = 1) REC_FIR
    JOIN
        (SELECT yearid, playerid, ab, h
        FROM batting
        WHERE stint > 1) REC_SEC
    ON REC_FIR.yearid = REC_SEC.yearid
    AND REC_FIR.playerid = REC_SEC.playerid
    WHERE REC_FIR.ab < REC_SEC.ab
    AND REC_FIR.h > REC_SEC.h);
