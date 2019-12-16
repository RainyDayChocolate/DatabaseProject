-- 14

SELECT DISTINCT a1.awardid as awardid
FROM awardsplayers a1, awardsplayers a2, awardsplayers a3
WHERE a1.playerid = a2.playerid
AND a3.playerid = a2.playerid
AND a1.awardid = a2.awardid
AND a3.awardid = a2.awardid
AND a1.yearid + 1 = a2.yearid
AND a2.yearid + 1 = a3.yearid
AND a1.yearid >= 1950
AND a1.yearid <= 1957;
