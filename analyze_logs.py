#!/usr/bin/env python2.7

import psycopg2


def connect():
    '''
    Connect to the PostgreSQL database and
    return the database connection.
    '''
    return psycopg2.connect("dbname=news")


def popular_articles_view():
    '''
    Create view of most popular articles.
    '''
    db = connect()
    c = db.cursor()
    query = "CREATE OR REPLACE VIEW favorite_articles as \
    SELECT distinct(count(log.path)) as page_views, log.path \
    FROM log \
    WHERE log.status = '200 OK' \
    and log.path like '/article/%' \
    GROUP BY log.path \
    ORDER BY page_views desc;"

    c.execute(query)
    db.commit()
    db.close()


def favorite_articles():
    '''
    List the top 3 favorite articles.
    '''
    db = connect()
    c = db.cursor()
    query = "SELECT art.title, fa.page_views \
        FROM favorite_articles as fa, articles as art \
        WHERE replace(fa.path, '/article/', '') = art.slug \
        LIMIT 3"
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print top three favorite articles
    print "Top three favorite articles:"
    for i in range(3):
        print "\""+result[i][0]+"\"", '---', result[i][1], "views"


def popular_authors():
    '''
    List the most popular authors of all time.
    '''
    db = connect()
    c = db.cursor()
    query = "SELECT auth.name, SUM(fa.page_views) as sum_page_views \
        FROM authors as auth, articles as art, favorite_articles as fa \
        WHERE auth.id=art.author \
        and replace(fa.path, '/article/', '') = art.slug \
        GROUP BY auth.name \
        ORDER BY sum_page_views desc"
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print authors of most popular articles
    print "\nMost popular article authors:"
    for i in range(len(result)):
        print "\""+result[i][0]+"\"", '---', result[i][1], "views"


def get_total_calls_per_day():
    '''
    Create a view of total calls per day.
    '''
    db = connect()
    c = db.cursor()
    query = "CREATE OR REPLACE VIEW total_calls_per_day as \
    SELECT COUNT(*) as all_calls, date_trunc('day', log.time) as date \
    FROM log \
    GROUP BY date;"
    c.execute(query)
    db.commit()
    db.close()


def get_failed_calls_per_day():
    '''
    Create a view of failed calls per day.
    '''
    db = connect()
    c = db.cursor()
    query = "CREATE OR REPLACE VIEW failed_calls_per_day as \
    SELECT COUNT(*) as failed_calls, date_trunc('day', log.time) as date \
    FROM log \
    WHERE status != '200 OK' \
    GROUP BY date;"
    c.execute(query)
    db.commit()
    db.close()


def get_percentage_of_failed_calls_per_day():
    '''
    Create a view of the percentage of failed calls per day.
    '''
    db = connect()
    c = db.cursor()
    query = "CREATE OR REPLACE VIEW percent_failed_calls as \
    SELECT round((f.failed_calls*1.0/t.all_calls*1.0)*100, 1) \
    as per_failed_calls, f.date \
    FROM failed_calls_per_day as f, total_calls_per_day as t \
    WHERE f.date=t.date;"
    c.execute(query)
    db.commit()
    db.close()


def error_request_threshold():
    '''
    Return day(s) and error rate where
    more than 1% of requests lead to errors.
    '''
    # Select which days had errors
    db = connect()
    c = db.cursor()
    query = "SELECT per_failed_calls, \
    to_char(date, 'FMMonth DD, YYYY') \
    FROM percent_failed_calls \
    WHERE per_failed_calls > 1.0"
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print days with more than 1% error request rate
    print "\nDays where more than 1% of requests lead to errors:"
    for i in range(len(result)):
        print "\""+result[i][1]+' --- '+str(result[i][0])+"% errors\""


if __name__ == '__main__':
    popular_articles_view()
    favorite_articles()
    popular_authors()
    get_total_calls_per_day()
    get_failed_calls_per_day()
    get_percentage_of_failed_calls_per_day()
    error_request_threshold()
