# Log Analysis Project (IPND)

### Project instruction
>The task is  to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

>In the project, you have to write a `python` code to connect to a `postgresql` database and get result as plain text of the reporting questions.

**Three questions:**
1. What are the most popular three articles of all time? Which articles have been accessed the most?
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

### Request Pre-installation:
* [The Virtual Machine](https://www.virtualbox.org/)  
* [Vagrant](https://www.vagrantup.com/)
* [Python2.7](https://www.python.org/)  

For setting up the environment and troubleshooting, check the link [How to install VM](https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/303a271d-bc69-4eba-ae38-e9875f841604/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0).

### Start the Project

##### 1. Lunching the Virtual Machine
This project makes use of the same Linux-based virtual machine (VM)
* From your terminal, inside the vagrant subdirectory, run the command `vagrant up`
* you can run `vagrant ssh` to log in

##### 2. Download the data
Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql` to connect to the database.

Here's what this command does:

* `psql` — the PostgreSQL command line program
* `-d news` — connect to the database named news which has been set up for you
* `-f` newsdata.sql — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

##### 3. Explore the Data
* `\dt` — display tables — lists the tables that are available in the database.
* `\d table` — (replace table with the name of a table) — shows the database schema for that particular table.

##### 4. Create the following Views
 ```sql
CREATE OR REPLACE VIEW articles_view AS
SELECT articles.title,articles.author,count(*) AS views
FROM articles JOIN log
ON log.path LIKE CONCAT('%',articles.slug,'%')
GROUP BY articles.id;
  ```
  ```sql
CREATE OR REPLACE VIEW total_error AS
SELECT date(time) AS days, count(status) AS errors
FROM log
WHERE status='404 NOT FOUND'
GROUP BY days;
 ```
 ```sql
CREATE OR REPLACE VIEW total_request AS
SELECT date(time) AS days, count(id) AS requests
FROM log
GROUP BY days;
 ```
##### 5. Running the Python code
* By using the SQL file `cview.sql` to create the views in database
```
psql -f cview.sql news
```
* After the Views have been created, inside the virtual machine run [`results.py`](https://github.com/xuefeihexue/IPND_project6/blob/master/results.py) with
 ```python
 python results.py
 ```
* The output result is in the text file [output.txt](https://github.com/xuefeihexue/IPND_project6/blob/master/output.txt)
