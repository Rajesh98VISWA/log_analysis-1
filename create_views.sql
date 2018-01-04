-- Create view of most popular articles.
CREATE OR REPLACE VIEW favorite_articles as
    SELECT distinct(count(log.path)) as page_views, log.path
    FROM log
    WHERE log.status = '200 OK'
    and log.path like '/article/%'
    GROUP BY log.path
    ORDER BY page_views desc;

-- Create a view of total calls per day.
CREATE OR REPLACE VIEW total_calls_per_day as
    SELECT COUNT(*) as all_calls, date_trunc('day', log.time) as date
    FROM log
    GROUP BY date;

-- Create a view of failed calls per day.
CREATE OR REPLACE VIEW failed_calls_per_day as
    SELECT COUNT(*) as failed_calls, date_trunc('day', log.time) as date
    FROM log
    WHERE status != '200 OK'
    GROUP BY date;

-- Create a view of the percentage of failed calls per day.
CREATE OR REPLACE VIEW percent_failed_calls as
    SELECT round((f.failed_calls/t.all_calls*1.0)*100, 1)
    as per_failed_calls, f.date
    FROM failed_calls_per_day as f, total_calls_per_day as t
    WHERE f.date=t.date;
