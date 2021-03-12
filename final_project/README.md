### Rotten Linguist search engine for movie reviews

This is a final project for the course _KIK-LG211 Building NLP Applications_ at the University of Helsinki, spring 2021.

Rotten Linguist's search engine searches for film reviews from rottentomatoes.com top 500 movies from 2016-2020 (https://www.rottentomatoes.com/).
The relevance search engine provides options for an exact match and simple wildcard search.
The results are presented in a user interface which is accessed through browser. The program prints snippets with NER (named entity recognition) highlighting and generates plots for most used adjectives and verbs, as well as for the frequency distribution of themes and PoS (Part-of-speech) tags.
The data from RT will only be used for educational purposes as example data for a search engine. All the data will be removed at the end of the KIK-LG211 course.

The program uses the following python libraries which need to be installed in order for the program to work:
flask, nltk, re, matplotlib, matplotlib.pyplot, sklearn.feature_extraction.text, os, ast, pke, spacy.

The program uses Flask, so before running the program, you need to set the following environment variables:

Show flask which file to run:

```
export FLASK_APP=flask_relevance_search.py
```

Enable development environment to activate interactive debugger and reloader:

```
export FLASK_ENV=development
```

Set the port in which to run the application, e.g.:

```
export FLASK_RUN_PORT=8000
```
Run FLASK

```
flask run
```

Go to `localhost:8000/search` in your browser to see the website.
