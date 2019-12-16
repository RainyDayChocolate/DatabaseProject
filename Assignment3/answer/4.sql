-- 4

SELECT salaries.yearid as year,
       SUM(salary) AS salary
       FROM salaries
       JOIN(
            SELECT yearid, teamid
            FROM teams
            WHERE wswin = 'Y') WSTEAM
        ON salaries.yearid = WSTEAM.yearid
        AND salaries.teamid = WSTEAM.teamid
GROUP BY salaries.yearid, salaries.teamid
ORDER BY salary DESC;
