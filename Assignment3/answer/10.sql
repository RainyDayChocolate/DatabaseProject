-- 10 issue

SELECT name_full AS school_name,
       player_num AS count
FROM
    (SELECT schoolid,
        COUNT(collegeplaying_unique.playerid) AS player_num
    FROM
        (SELECT DISTINCT playerid
        FROM allstarfull) UNIQUE_ALLSTAR
    JOIN
        (SELECT distinct playerid, schoolid
        FROM
        collegeplaying) collegeplaying_unique
    ON UNIQUE_ALLSTAR.playerid = collegeplaying_unique.playerid
    GROUP BY schoolid
    ORDER BY player_num DESC) IDNUM
JOIN
    schools
ON IDNUM.schoolid = schools.schoolid
ORDER BY player_num DESC, school_name
LIMIT 10 ;
