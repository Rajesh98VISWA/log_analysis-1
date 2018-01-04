#!/usr/bin/env python2.7

import psycopg2


DBNAME = "news"

def connect():
    """
    Create a connection to the database, defined by DBNAME,
    and return the database connection and cursor.

    Returns:
    db, c - a tuple. The first element is a connection to the database.
    The second element is a cursor for the database.
    """
    try:
        db = psycopg2.connect(dbname=DBNAME)  # Connect to database
        c = db.cursor()  # Create cursor
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def favorite_articles():
    """
    List the top 3 favorite articles.
    """
    db, c = connect()
    query = """SELECT art.title, fa.page_views
        FROM favorite_articles as fa, articles as art
        WHERE replace(fa.path, '/article/', '') = art.slug
        LIMIT 3"""
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print top three favorite articles
    print "Top three favorite articles:"
    for title, views in result:
        print '"{}" --- {} views'.format(title, views)


def popular_authors():
    """
    List the most popular authors of all time.
    """
    db, c = connect()
    query = """SELECT auth.name, SUM(fa.page_views) as sum_page_views
        FROM authors as auth, articles as art, favorite_articles as fa
        WHERE auth.id=art.author
        and replace(fa.path, '/article/', '') = art.slug
        GROUP BY auth.name
        ORDER BY sum_page_views desc"""
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print authors of most popular articles
    print "\nMost popular article authors:"
    for author, views in result:
        print '"{}" --- {} views'.format(author, views)


def error_request_threshold():
    """
    Return day(s) and error rate where
    more than 1% of requests lead to errors.
    """
    # Select which days had errors
    db, c = connect()
    query = """SELECT to_char(date, 'FMMonth DD, YYYY'),
    per_failed_calls
    FROM percent_failed_calls
    WHERE per_failed_calls > 1.0"""
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print days with more than 1% error request rate
    print "\nDays where more than 1% of requests lead to errors:"
    for date, percent_error in result:
        print '"{}" --- {}% error'.format(date, percent_error)


if __name__ == '__main__':
    favorite_articles()
    popular_authors()
    error_request_threshold()
