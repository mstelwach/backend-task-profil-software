import json
import urllib.request
import sqlite3

COLUMNS = ['Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Awards', 'Year', 'imdbRating',
           'imdbVotes', 'BoxOffice']


def insert_to_db():
    conn = sqlite3.connect('movies.sqlite')
    cursor = conn.cursor()
    sql = """SELECT TITLE FROM MOVIES"""
    cursor.execute(sql)
    query = cursor.fetchall()
    titles = [title[0] for title in query]
    for title in titles:
        url = urllib.request.urlopen(
            'http://www.omdbapi.com/?t={}&type=movie&apikey=e8706d87'.format(title.replace(' ', '+'))
        )
        d = json.loads(url.read().decode())
        movie_data = {key: d[key] if d[key] != 'N/A' else None for key in d if key in COLUMNS}

        # SET STRING YEAR TO INTEGER
        if movie_data['Year']:
            movie_data['Year'] = int(movie_data['Year'])

        # SET STRING IMDB_RATING TO FLOAT
        if movie_data['imdbRating']:
            movie_data['imdbRating'] = float(movie_data['imdbRating'])

        # SET STRING IMDB_VOTES TO INTEGER
        if movie_data['imdbVotes']:
            movie_data['imdbVotes'] = int(movie_data['imdbVotes'].replace(',', ''))

        # SET STRING BOX_OFFICE TO INTEGER
        if movie_data['BoxOffice']:
            movie_data['BoxOffice'] = int(movie_data['BoxOffice'].replace(',', '').replace('$', ''))

        sql = """
            UPDATE MOVIES
            SET YEAR=?,
                RUNTIME=?,
                GENRE=?,
                DIRECTOR=?,
                WRITER=?,
                ACTORS=?,
                LANGUAGE=?,
                COUNTRY=?,
                AWARDS=?,
                IMDb_Rating=?,
                IMDb_votes=?,
                BOX_OFFICE=?
            WHERE TITLE = ?;
        """
        parameters = tuple(movie_data.values()) + (title, )
        cursor.execute(sql, parameters)
        conn.commit()
        print('ADD MOVIE "{}" TO TABLE MOVIES'.format(title))

    conn.close()


if __name__ == '__main__':
    insert_to_db()
