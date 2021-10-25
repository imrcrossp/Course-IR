from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter
import sqlite3
import pandas as pd
import numpy as np
import os
import math
import string
import json
import ast
import nltk
# Create your models here.

info = {}
cwd = os.getcwd()
fp = open(cwd+"/hw/static/assets/docs/info_woptr", "r")
strr = fp.read()
fp.close()
print(strr)


