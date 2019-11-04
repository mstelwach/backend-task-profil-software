# backend-task-profil-software

The script fills example movie data from OMDb API. Data source contains only titles of movies.

If you want to fill in the empty columns, use the script:
 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded files by typing:
```
$ python insert_to_db.py
```

### Scripts 'movies.py'

1. Sorting Movies by every column (bonus points for sorting by multiple columns).
  
  Example input:
  ```
  $ python movies.py --sort_by year
  ```
 2 Filtering Movies by column and value.
 
  Example input:
   ```
  $ python movies.py --filter_by language spanish
    ```
 3. Comparison by column of two titles.
 
  Example input:
   ```
  $ python movies.py --compare  runtime "Seven Pounds" "Memento"
    ```
 4. Adding a new movie to the table 'movies'.
    ```
  $ python movies.py --add 'Kac Wawa'
    ```
 5. Showing current highscores in :
            - Runtime
            - Box office earnings
            - Most awards won
            - Most nominations
            - Most Oscars
            - Highest IMDB Rating
    ```
  $ python movies.py --highscores
    ```
