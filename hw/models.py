from django.db import models
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter
import nltk
import sqlite3
import pandas as pd
import numpy as np
import os
import math
import string
import ast
# Create your models here.

def fromcloud():
	info = {}
	top24pctn = {}
	top24 = {}
	count = 0
	countpctn = 0
	stops = set(nltk.corpus.stopwords.words('english'))
	cwd = os.getcwd()

	fp = open(cwd+"/hw/static/assets/docs/info", "r")
	in4 = fp.read()
	fp.close()
	str_in4 = in4.replace("'", "\"")
	info['rank'] = str_in4
	in4 = ast.literal_eval(in4)
	for i in in4:
		if countpctn < 24:
			top24pctn[i] = in4[i] # i 是一個單字 當dict沒有該word時 會新增 而 in4[word] 為其出現次數
			countpctn = countpctn+1
		tmp = i
		if(count == 24):
			break
		else:
			if tmp in stops:
				continue
			for j in string.punctuation:
				tmp = tmp.replace(j, '')
			if not tmp.isdigit() and tmp != "":
				top24[i] = in4[i]
				count = count+1
	str_top24pctn = str(top24pctn)
	str_top24 = str(top24)
	str_top24pctn = str_top24pctn.replace("'", '"')
	str_top24 = str_top24.replace("'", "\"")
	info['top24_pctn'] = str_top24pctn
	info['top24'] = str_top24
	fp = open(cwd+"/hw/static/assets/docs/info_woptr", "r")
	info['top24_wo'] = fp.read()
	fp.close()
	return info

def mds(s1, s2, n, m, dp):
	if(n == 0):
		return m
	if(m == 0):
		return n
	if(dp[n][m] != -1):
		return dp[n][m]
	if(s1[n-1] == s2[m-1]):
		if(dp[n-1][m-1] == -1):
			dp[n][m] = mds(s1, s2, n-1, m-1, dp)
			return dp[n][m]
		else:
			dp[n][m] = dp[n-1][m-1]
			return dp[n][m]
	else:
		if(dp[n-1][m] != -1):
			m1 = dp[n-1][m]
		else:
			m1 = mds(s1, s2, n-1, m, dp)
		if(dp[n][m-1] != -1):
			m2 = dp[n][m-1]
		else:
			m2 = mds(s1, s2, n, m-1, dp)
		if(dp[n-1][m-1] != -1):
			m3 = dp[n-1][m-1]
		else:
			m3 = mds(s1, s2, n-1, m-1, dp)
		dp[n][m] = 1 + min(m1, min(m2, m3))
		return dp[n][m]

def advancedsearching(key, up, low):
	ps = PorterStemmer()
	info = {}
	cwd = os.getcwd()
	db = sqlite3.connect(cwd+"/hw/static/assets/docs/invbook.db")
	cus = db.cursor()
	cus.execute(''' SELECT * FROM WORDDIC ''')
	rows = cus.fetchall()
	counter = 0
	bound = int(low)
	for row in rows:
		str1 = ps.stem(row[0])
		str2 = ps.stem(key)
		n = len(str1)
		m = len(str2)
		dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
		dist = mds(str1, str2, n, m, dp)
		if(dist <= 1):
			result = row[1]
			result = result.replace("{", "")
			result = result.replace("}", "")
			result = result.replace("'", "")
			resultlist = result.split(",")
			for fn_pg in resultlist:
				if(bound != 0):
					bound = bound-1
					continue
				dtl = fn_pg.replace(" ", "").split("_")
				_data = pd.read_csv(cwd+"/hw/static/assets/docs/1000/"+dtl[0])
				title = _data['title'][int(dtl[1])]
				info[fn_pg.replace(" ", "")] = title
				counter = counter+1
				if counter == 10:
					break
		if counter == 10:
			break
	return info

def showcntxt(fn_pg, key):
	cwd = os.getcwd()
	ps = PorterStemmer()
	stops = set(nltk.corpus.stopwords.words('english'))
	dtl = fn_pg.replace(" ", "").split("_")
	info = {}
	_data = pd.read_csv(cwd+"/hw/static/assets/docs/1000/"+dtl[0])

	cntxt = _data['abstract'][int(dtl[1])]
	title = _data['title'][int(dtl[1])]
	output = []
	dic = []
	total = 0
	tmptxt = nltk.word_tokenize(cntxt)
	found = 0
	for i in tmptxt:
		str1 = ps.stem(key.lower())
		str2 = ps.stem(i.lower())
		n = len(str1)
		m = len(str2)
		total = m + total
		dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]	
		if(mds(str1, str2, n, m, dp) <= 1):
			dic.append("<span style=\"background-color:#008000\">"+i+"</span>")
			found = found+1
		elif (i.lower().find(str1) != -1 or key.lower().find(str2) != -1):
			dic.append("<span style=\"background-color:#008000\">"+i+"</span>")
			found = found+1
		else:
			dic.append(i)
	output.append(" ".join(dic))
	clean = [i for i in nltk.word_tokenize(cntxt.lower()) if i not in stops]
	newset = []
	for j in clean:
		tmp = j
		for k in string.punctuation:
			j = j.replace(k, '')
		if not j.isdigit() and j != '':
			newset.append(tmp)
	counter = 0
	newword = Counter(newset)
	x = dict(newword)
	dict_words = {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}
	if(len(dict_words) > 5):
		leng = 5
	else:
		leng = len(dict_words)
	str_words = str(dict(list(dict_words.items())[:5]))
	info['cntxt'] = output
	info['title'] = title
	info['words'] = str(len(tmptxt))
	info['chars'] = str(total)
	info['sents'] = str(len(sent_tokenize(cntxt)))
	info['top24'] = str_words.replace("'", '"')
	info['found'] = str(found)
	return info

