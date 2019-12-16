-- 9
SELECT yearid as year, AVG(salary) as salary
FROM (
    SELECT yearid, teamid, SUM(salary) as salary
    FROM salaries
    GROUP BY yearid, teamid) SUM_SALARY
GROUP BY yearid
ORDER BY yearid;

