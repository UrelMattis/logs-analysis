import psycopg2
# query question #1
title_1 = 'What are the most popular three articles of all time?'
search_1 = """
            SELECT title, count(*) as articleviews FROM articles
            JOIN log
            ON articles.slug = substring(log.path, 10)
            GROUP BY title
            ORDER BY articleviews
            DESC LIMIT 3;
        """
# query question #2
title_2 = 'Who are the most popular article authors of all time?'
search_2 = """
            SELECT authors.name, count(*) as authorviews
            FROM articles
            JOIN authors
            ON articles.author = authors.id
            JOIN log
            ON articles.slug = substring(log.path, 10)
            WHERE log.status
            LIKE '200 OK'
            GROUP BY authors.name
            ORDER BY authorviews
            DESC;
            """
# query question #3
title_3 = 'On which days did more than 1% of requests lead to errors?'
search_3 = """
            WITH error_requests AS (
                SELECT time::date AS day, count(*)
                FROM log
                GROUP BY time::date
                ORDER BY time::date
              ), errors AS (
                SELECT time::date AS day, count(*)
                FROM log
                WHERE status != '200 OK'
                GROUP BY time::date
                ORDER BY time::date
              ), rate AS (
                SELECT error_requests.day,
                  errors.count::float / error_requests.count::float * 100
                  AS percentage
                FROM error_requests, errors
                WHERE error_requests.day = errors.day
              )
            SELECT * FROM rate WHERE percentage > 1;
        """


class Logs:
    # create a function to connect to the database and feed query
    def __init__(var):
        try:
            var.db = psycopg2.connect('dbname = news')
            var.cursor = var.db.cursor()
        except:
            print ("Unable to connect")

    def get_Results(var, content):
        var.cursor.execute(content)
        return var.cursor.fetchall()

    # create a function to print query results
    def print_Results(var, title, content, type):
        print title
        output = var.get_Results(content)
        for i in range(len(output)):
            print output[i][0], '-', output[i][1], type
        print ("\n")

if __name__ == '__main__':
    # print query results
    log = Logs()
    log.print_Results(title_1, search_1, 'views')
    log.print_Results(title_2, search_2, 'views')
    log.print_Results(title_3, search_3, '% error')
