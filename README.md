# backend-task-profil-software

The script fills example movie data from OMDb API. Data source contains only titles of movies.

If you want to fill in the empty columns, use the script:
 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded files by typing:
```
$ python insert_to_db.py
```

### Scripts 'movies.py'
Use the script:
 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded files by typing:
```
$ python movies --example_function.py
```

- Sorting Movies by every column (bonus points for sorting by multiple columns).
  
  Example input:
  ```
  $ python movies.py --sort_by year
  ```
  
- Filtering Movies by column and value.
 
  Example input:
   ```
  $ python movies.py --filter_by language spanish
   ```
   
- Comparison by column of two titles.
 
  Example input:
   ```
  $ python movies.py --compare  runtime "Seven Pounds" "Memento"
   ```
   
- Adding a new movie to the table 'movies'.
 
  Exampe input:
  
  ```
  $ python movies.py --add 'Kac Wawa'
  ```
  
- Showing current highscores in :
    - Runtime
    - Box office earnings
    - Most awards won
    - Most nominations
    - Most Oscars
    - Highest IMDB Rating
    
  Example input:
  
  ```
  $ python movies.py --highscores
  ```
