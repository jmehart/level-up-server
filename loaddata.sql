SELECT * FROM levelupapi_gametype;
SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;



-- "Seeding the database" is a term that developers use to describe the process is inserting some boilerplate data into their databases during development. It gives them some valid data to work with quickly while they try to build new features, or fix bugs.

-- With Django, you can do that with something called fixtures. A fixture is a file that has JSON formatted data in it. That JSON data is then read by Django, converted into INSERT INTO SQL statements, and then executed to get some rows into your database tables.