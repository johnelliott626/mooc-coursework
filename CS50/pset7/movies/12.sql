SELECT title FROM (movies JOIN stars ON movies.id = stars.movie_id) join people ON stars.person_id = people.id
WHERE name = 'Johnny Depp' 
AND title IN 
(SELECT title FROM (movies JOIN stars ON movies.id = stars.movie_id) join people ON stars.person_id = people.id
WHERE name = 'Helena Bonham Carter' );
