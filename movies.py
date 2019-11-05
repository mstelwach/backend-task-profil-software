import sqlite3
import sys
# from tabulate import tabulate


class Database(object):

    def __init__(self):
        self._conn = sqlite3.connect('movies.sqlite')
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql):
        self.cursor.execute(sql)

    def query_db(self, sql):
        self.execute(sql)
        query = self.cursor.fetchall()
        return query


class Movies(Database):

    # @staticmethod
    # def get_headers_table(*args):
    #     """
    #     Create headers columns for the array.
    #     All parameters - string format.
    #     :param args: name, e.g -> 'Year'. Multiple arguments.
    #     :return: List of headers columns
    #     """
    #     headers = ['Title']
    #     if args:
    #         headers += [column.replace('_', ' ').title() for column in args]
    #     return headers
    #
    # @staticmethod
    # def get_table(query, headers):
    #     """
    #     Create table
    #     :param query: List of rows, each row format - > tuple, e.g -> [('Memento, 2000)]
    #     :param headers: List of headers, each header format -> string, e.g -> ['Title', 'Year']
    #     :return: Format a fixed width table for pretty printing
    #         ╒═══════════╤═══════════╕
    #         │ Title     │   Year    │
    #         ╞═══════════╪═══════════╡
    #         │ Memento   │   2000    │
    #         ╘═══════════╧═══════════╛
    #     """
    #     table = tabulate(query, headers, tablefmt='fancy_grid')
    #     return table

    def sort_by(self, *args):
        """
        Sorting Movies by every column (bonus points for sorting by multiple columns).
        All parameters - string format.
        :param args: optional(year, runtime, genre, director, actors, language, country, awards, imdb_rating,
        imdb_votes, box_office). Multiple arguments, e.g -> runtime, genre
        :return: List of sorted movies.
        """
        # headers = self.get_headers_table(*args)
        sql = """SELECT TITLE FROM MOVIES ORDER BY TITLE ASC"""

        if args:
            length_columns = len(args)
            number_braces = ', {}' * length_columns
            sql = 'SELECT TITLE' + number_braces.format(*args) + ' FROM MOVIES ORDER BY'

        columns_order = []
        for column in args:
            column = column.upper()
            if column in ['YEAR', 'IMDB_RATING', 'IMDB_VOTES', 'BOX_OFFICE']:
                columns_order.append(' {} DESC'.format(column))
            elif column == 'RUNTIME':
                columns_order.append(' RUNTIME + 0 DESC')
            else:
                columns_order.append(' {} ASC'.format(column))

        sql += ','.join(columns_order)
        query = self.query_db(sql)
        # print(self.get_table(query, headers))
        return query

    def filter_by(self, column, value):
        """
        Filtering Movies by column and value.
        All parameters - string format.
        :param column: optional(director, actors, awards, box_office, language)
        :param value: optional(
            director: name, e.g -> 'Fincher'
            actors: name, e.g -> 'DiCaprio'
            awards: percentage (Movies that won more than 80% of nominations), e.g -> '80' -
                or 'nominated' (Movies that was nominated  for Oscar but did not win any)
            box_office: number (Movies that earned more than 100,000,000 $), e.g -> '100000000'
            language: name (Only movies in certain Language), e.g -> 'spanish'
        :return: List of filtered movies.
        """
        # headers = self.get_headers_table(column)
        column = column.upper()

        if column == 'AWARDS' and value.isdigit():
            query = []
            percentage_rate = int(value)
            sql = """SELECT TITLE, AWARDS FROM MOVIES WHERE AWARDS NOT NULL"""
            for title, awards in self.query_db(sql):
                number_awards = [int(char) for char in awards.split() if char.isdigit()]
                if len(number_awards) != 3:
                    number_awards = [0] * (3-len(number_awards)) + number_awards

                _, number_awards_won, number_nominations = number_awards
                percentage_won = int("{0:.0%}".format(number_awards_won / number_nominations).rstrip('%'))
                if percentage_won > percentage_rate:
                    query.append((title, awards))

        elif column == 'AWARDS' and value.upper() == 'NOMINATED':
            sql = """SELECT TITLE, AWARDS FROM MOVIES WHERE AWARDS LIKE '%Nominated%Oscar%'"""
            query = self.query_db(sql)

        elif column == 'BOX_OFFICE' and value.isdigit():
            sql = """SELECT TITLE, BOX_OFFICE FROM MOVIES where BOX_OFFICE > {}""".format(int(value))
            query = self.query_db(sql)

        else:
            sql = """SELECT TITLE, {} FROM MOVIES WHERE {} LIKE '%{}%'""".format(column, column, value)
            query = self.query_db(sql)

        # print(self.get_table(query, headers))
        return query

    def compare(self, column, title_one, title_two):
        """
        Comparison by column of two titles.
        All parameters - string format.
        :param column: optional(imdb_rating, box_office, awards, runtime)
        :param title_one: name, e.g -> 'Seven Pounds'
        :param title_two: name, e.g -> 'Memento
        :return: Movie won with column value
        """
        # headers = self.get_headers_table(column)
        sql = """SELECT TITLE, {} FROM MOVIES WHERE TITLE='{}' or TITLE='{}'""".format(column,
                                                                                       title_one,
                                                                                       title_two)

        if not title_one and not title_two:
            sql = """SELECT TITLE, {} FROM MOVIES""".format(column)

        column = column.upper()
        if column == 'AWARDS':
            query = []
            for title, awards in self.query_db(sql):
                number_awards = [int(char) for char in awards.split() if char.isdigit()]
                if len(number_awards) != 3:
                    number_awards = [0] * (3-len(number_awards)) + number_awards

                _, number_awards_won, _ = number_awards
                query.append((title, number_awards_won))

        elif column == 'RUNTIME':
            query = [(title, int(runtime.rstrip(' min'))) for title, runtime in self.query_db(sql) if runtime]
        else:
            query = [(title, column_value) for title, column_value in self.query_db(sql) if column_value]

        won_movie = max(query, key=lambda movie: movie[1])
        # print(self.get_table([won_movie], headers))
        return won_movie

    def add(self, movie):
        """
        Adding a new movie to the table 'movies'.
        All parameters - string format.
        :param movie: name, e.g - > 'Kac Wawa'
        :return:
        """
        try:
            print("Successfully Connected to SQLite DB - movies")
            insert_sql = """INSERT INTO MOVIES (TITLE) VALUES ('{}')""".format(movie)
            self.execute(insert_sql)
            self.commit()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if self.connection:
                self.connection.close()
                print("The SQLite connection is closed")

    def highscores(self):
        """
        Showing current highscores in :
            - Runtime
            - Box office earnings
            - Most awards won
            - Most nominations
            - Most Oscars
            - Highest IMDB Rating
        :return: List of highest column values
        """
        queryset = []
        headers = ['Column', 'Movie', 'Value']

        # GET HIGHEST RUNTIME
        sql = """SELECT TITLE, RUNTIME FROM MOVIES WHERE RUNTIME NOT NULL"""
        query = [(title, int(runtime.rstrip(' min'))) for title, runtime in self.query_db(sql)]
        title, max_runtime = max(query, key=lambda movie: movie[1])
        queryset.append(('Runtime', title, '{}h{}m'.format(max_runtime // 60, max_runtime % 60)))

        # GET BOX OFFICE AND IMDB RATING
        sqls = [('Box Office', """SELECT TITLE, BOX_OFFICE FROM MOVIES WHERE BOX_OFFICE NOT NULL """),
                ('IMDB Rating', """SELECT TITLE, IMDb_Rating FROM MOVIES WHERE  IMDb_Rating NOT NULL""")]

        for column, sql in sqls:
            title, value = max(self.query_db(sql), key=lambda movie: movie[1])
            if column == 'Box Office':
                value = '${:,}'.format(value)
            queryset.append((column, title, value))

        # GET HIGHEST WON OSCARS, AWARDS AND NOMINATIONS
        awards_sql = """SELECT TITLE, AWARDS FROM MOVIES WHERE AWARDS NOT NULL"""
        d = {}
        for title, awards in self.query_db(awards_sql):
            number_awards = [int(char) for char in awards.split() if char.isdigit()]
            if len(number_awards) != 3:
                number_awards = [0] * (3-len(number_awards)) + number_awards

            if any(char in awards for char in ['Nominated', 'Golden']):
                number_awards[0] = 0

            d[title] = number_awards

        for index, column in enumerate(['Oscars', 'Awards Won', 'Nominations']):
            title, values = max(d.items(), key=lambda kv: kv[1][index])
            queryset.append((column, title, values[index]))

        # table = tabulate(queryset, headers=headers, tablefmt='fancy_grid')
        # print(table)
        return queryset


if __name__ == '__main__':
    m = Movies()
    method = sys.argv[1].lstrip('-')
    args = sys.argv[2:]
    print(getattr(m, method)(*args))
