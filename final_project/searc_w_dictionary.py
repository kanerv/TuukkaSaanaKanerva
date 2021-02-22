from flask import Flask, render_template, request
import re, fileinput, mmap, nltk
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib as mlp
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer
import os

documents = []
file_variable = open("enwiki-20181001-corpus.100-articles.txt", encoding="utf8")
text_string = file_variable.read()
