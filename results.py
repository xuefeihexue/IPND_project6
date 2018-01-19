#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module connect to postgresql and print results of three quesions.

The three questions are defined in the README.md.

Before running this module,run the cview.sql first to create views in database.

"""


import psycopg2  # Use psycoppg2 DBI to connect to postgresql database


# Connect to the database first,then parse the query and return the result


def connect_db_and_return_result(query):
    """Connect to the postgresql database and return the result of query."""
    try:
        connection = psycopg2.connect('dbname=news')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_result(result_list, question):
    """Print the results in a format way."""
    print question+'\n'+'-'*len(question)
    longest_length_i1 = 0  # Longest length of the first element in result
    longest_length_i2 = 0  # Longest length of the second element in result
    for i in result_list:
        if len(i[0]) > longest_length_i1:
            longest_length_i1 = len(i[0])
        if len(str(i[1])) > longest_length_i2:
            longest_length_i2 = len(str(i[1]))
    for element in result_list:
        print '"', element[0], '"',\
         ' ' * (longest_length_i1 - len(element[0])), '--', element[1],\
         ' '*(longest_length_i2 - len(str(element[1]))), ' views'
    print
    print '\n'


# What are the most popular three articles of all time?
# Which articles have been accessed the most?

def popular_article():
    """Print the most three popular articles with title and numbers."""
    query1 = '''
    SELECT articles_view.title,articles_view.views
    FROM articles_view
    ORDER BY articles_view.views DESC
    LIMIT 3;
    '''
    result = connect_db_and_return_result(query1)
    question1 = '1. What are the most popular three articles of all time?'
    print_result(result, question1)

# Who are the most popular article authors of all time? That is,
# when you sum up all of the articles each author has written,
# which authors get the most page views?


def popular_author():
    """Print the most popular authors with names and numbers."""
    query2 = '''
    SELECT authors.name,sum(articles_view.views) AS views
    FROM authors JOIN articles_view
    ON articles_view.author=authors.id
    GROUP BY authors.id
    ORDER BY views DESC;
    '''
    result = connect_db_and_return_result(query2)
    question2 = '2. Who are the most popular authors?'
    print_result(result, question2)

# On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP
# status code that the news site sent to the user's browser.


def error_log():
    """Print out the days have more than 1% of HTTP request errors."""
    query3 = '''
    SELECT total_error.days,
    round(total_error.errors*100.0/total_request.requests,1) AS rate
    FROM total_error,total_request
    WHERE total_error.days=total_request.days
    AND round(total_error.errors*100.0/total_request.requests,1)>1.0
    ORDER BY total_error.days;
    '''
    result = connect_db_and_return_result(query3)
    question3 = '3. Days with errors > 1% are: '
    if result == []:
        print 'Thses is no day having connecting error >1%.'
    else:
        print question3+'\n'+'-'*len(question3)
        for element in result:
            print '"', element[0], '"'+'--', element[1], '%'
            print '\n'

# Check if it is the main module and run the module

if __name__ == '__main__':
    popular_article()
    popular_author()
    error_log()
