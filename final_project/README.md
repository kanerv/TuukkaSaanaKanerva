### Rotten Linguist search engine for movie reviews

This is a final project for the course _KIK-LG211 Building NLP Applications_.

Rotten Linguist search engine searches for film reviews from rottentomatoes.com top 500 movies from 2016-2020 (https://www.rottentomatoes.com/).
The relevance search engine provides options for an exact match and simple wildcard search.
The results are presented in a user interface. The program print snippets with NER (named entity) highlighting and generates plots for most used adjectives, themes, and x?


The program uses Flask, so before runnign the program, you need to set the following environment variables:

Show flask which file to run:

```
export FLASK_APP=flaskdemo.py
```

Enable development environment to activate interactive debugger and reloader:

```
export FLASK_ENV=development
```

Set the port in which to run the application, e.g.:

```
export FLASK_RUN_PORT=8000
```

Go to `localhost:8000/search` in your browser to see the website.
