#Create the articles_view View to return a table of title,author,and count

'''
create view articles_view as
select articles.title,articles.author,count(*) as views
from articles join log
on log.path like CONCAT('%',articles.slug,'%')
group by articles.id;
'''

#Create the total_error View to return a table of days,count of errors days
'''
Create view total_error as
select date(time) as days, count(status) as errors
from log
where status='404 NOT FOUND'
group by days;
'''

#Create the total_request View to return a table of days,count of request days
'''
Create view total_request as
select date(time) as days, count(id) as requests
from log
group by days;
'''
