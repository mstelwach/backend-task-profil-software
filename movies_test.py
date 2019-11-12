import unittest

from movies import Movies


class MoviesTest(unittest.TestCase):

    def setUp(self):
        self.m = Movies()

    def test_movies_sort_by_one_column_year(self):
        sql = """SELECT TITLE, YEAR FROM MOVIES ORDER BY YEAR DESC """
        query = self.m.query_db(sql)
        self.assertEqual(self.m.sort_by('Year'), query)

    def test_movies_sort_by_two_columns(self):
        sql = """SELECT TITLE, GENRE, BOX_OFFICE FROM MOVIES 
        ORDER BY GENRE ASC, BOX_OFFICE DESC"""
        query = self.m.query_db(sql)
        self.assertEqual(self.m.sort_by('Genre', 'box_office'), query)

    def test_movies_filter_by_director(self):
        query = self.m.filter_by('director', 'Fincher')
        self.assertEqual(len(query), 3)

    def test_movies_filter_by_actor(self):
        query = self.m.filter_by('actors', 'DiCaprio')
        self.assertEqual(len(query), 5)

    def test_movies_filter_by_oscar_only_nominated(self):
        query = self.m.filter_by('awards', 'nominated')
        self.assertEqual(len(query), 30)

    def test_movies_filter_by_awards_won_more_than_percent_nominations(self):
        query = self.m.filter_by('awards', '80')
        self.assertEqual(len(query), 41)

    def test_movies_filter_by_language(self):
        query = self.m.filter_by('language', 'spanish')
        self.assertEqual(len(query), 17)

    def test_movies_compare_by_rating(self):
        query = self.m.compare('imdb_rating', 'Seven Pounds', 'Memento')
        self.assertEqual(query, ('Memento', 8.4))

    def test_movies_compare_by_box_office(self):
        query = self.m.compare('box_office', 'Seven Pounds', 'Memento')
        self.assertEqual(query, ('Seven Pounds', 69951824))

    def test_movies_compare_by_numbers_awards_won(self):
        query = self.m.compare('awards', 'Seven Pounds', 'Memento')
        self.assertEqual(query, ('Memento', 56))

    def test_movies_compare_by_runtime(self):
        query = self.m.compare('runtime', 'Seven Pounds', 'memento')
        self.assertEqual(query, ('Seven Pounds', 123))

    def test_highsores(self):
        highscore_query = [
            ('Runtime', 'Gone with the Wind', '3h58m'),
            ('Box Office', 'The Dark Knight', '$533,316,061'),
            ('IMDB Rating', 'The Shawshank Redemption', 9.3),
            ('Oscars', 'Ben Hur', 11),
            ('Awards Won', 'Boyhood', 171),
            ('Nominations', 'Boyhood', 209),
        ]
        self.assertEqual(self.m.highscores(), highscore_query)


if __name__ == '__main__':
    unittest.main()