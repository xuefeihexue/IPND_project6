#!/usr/bin/env python2.7.12
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
    select articles_view.title,articles_view.views
    from articles_view
    order by articles_view.views DESC
    limit 3;
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
    select authors.name,sum(articles_view.views) as views
    from authors join articles_view
    on articles_view.author=authors.id
    group by authors.id
    order by views DESC;
    '''
    result = connect_db_and_return_result(query2)
    print 'Author Popularity: '
    for element in result:
        print '"', element[0], '"'+'--', element[1]
    print '\n'


def error_log():
    query3 = '''
    select total_error.days,
    round(total_error.errors*100.0/total_request.requests,1) as rate
    from total_error,total_request
    where total_error.days=total_request.days
    and round(total_error.errors*100.0/total_request.requests,1)>1.0
    order by total_error.days;
    '''
    result = connect_db_and_return_result(query3)
    print 'Days with errors > 1% are: '
    for element in result:
        print '"', element[0], '"'+'--', element[1], '%'
    print '\n'


popular_article()
popular_author()
error_log()
