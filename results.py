atom --safe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

# Connect to the database first,then parse the query and return the result


def connect_db_and_return_result(query):
    try:
        connection = psycopg2.connect('dbname=news')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    except BaseException:
        print 'Sorry,connection failed'


# What are the most popular three articles of all time?
# Which articles have been accessed the most?

def popular_article():
    query1 = '''
    SELECT articles_view.title,articles_view.views
    FROM articles_view
    ORDER BY articles_view.views DESC
    LIMIT 3;
    '''
    result = connect_db_and_return_result(query1)
    print 'The top 3 articles are: '
    for element in result:
        print '"', element[0], '"'+'--', element[1]
    print '\n'

# Who are the most popular article authors of all time? That is,
# when you sum up all of the articles each author has written,
# which authors get the most page views?


def popular_author():
    query2 = '''
    SELECT authors.name,sum(articles_view.views) AS views
    FROM authors JOIN articles_view
    ON articles_view.author=authors.id
    GROUP BY authors.id
    ORDER BY views DESC;
    '''
    result = connect_db_and_return_result(query2)
    print 'Author Popularity: '
    for element in result:
        print '"', element[0], '"'+'--', element[1]
    print '\n'

# On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP
# status code that the news site sent to the user's browser.


def error_log():
    query3 = '''
    SELECT total_error.days,
    round(total_error.errors*100.0/total_request.requests,1) AS rate
    FROM total_error,total_request
    WHERE total_error.days=total_request.days
    AND round(total_error.errors*100.0/total_request.requests,1)>1.0
    ORDER BY total_error.days;
    '''
    result = connect_db_and_return_result(query3)
    print 'Days with errors > 1% are: '
    for element in result:
        print '"', element[0], '"'+'--', element[1], '%'
    print '\n'


popular_article()
popular_author()
error_log()
