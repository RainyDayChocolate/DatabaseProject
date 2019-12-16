-- 8
SELECT AL_AVGSA.yearid AS year,
       AL_AVGSA.salary_avg_allstar / CM_AVGSA.salary_avg_cm AS ratio
FROM (
    (SELECT yearid, AVG(salary) AS salary_avg_allstar
    FROM(
        SELECT allstarfull.yearid, salaries.salary
        FROM
            allstarfull
        JOIN
            salaries
        ON salaries.playerid = allstarfull.playerid
        AND salaries.yearid = allstarfull.yearid) ALSA
    GROUP BY yearid) AL_AVGSA
JOIN
    (SELECT yearid,
        AVG(salary) AS salary_avg_cm
    FROM salaries
    GROUP BY yearid) CM_AVGSA
ON AL_AVGSA.yearid = CM_AVGSA.yearid)
ORDER BY yearid;
