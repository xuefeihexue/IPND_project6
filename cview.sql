CREATE OR REPLACE VIEW articles_view AS
SELECT articles.title,articles.author,count(*) AS views
FROM articles JOIN log
ON log.path LIKE CONCAT('%',articles.slug,'%')
GROUP BY articles.id;

CREATE OR REPLACE VIEW total_error AS
SELECT date(time) AS days, count(status) AS errors
FROM log
WHERE status='404 NOT FOUND'
GROUP BY days;

CREATE OR REPLACE VIEW total_request AS
SELECT date(time) AS days, count(id) AS requests
FROM log
GROUP BY days;
