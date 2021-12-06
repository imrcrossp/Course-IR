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
import gensim.models
from gensim import utils
from sklearn.decomposition import IncrementalPCA
from sklearn.manifold import TSNE
import statistics 

## Init
def reduce_dimensions(model):
	num_dimensions = 2  # final num dimensions (2D, 3D, etc)

	# extract the words & their vectors, as numpy arrays
	vectors = np.asarray(model.wv.vectors)
	labels = np.asarray(model.wv.index_to_key)  # fixed-width numpy strings

	# reduce using t-SNE
	tsne = TSNE(n_components=num_dimensions, random_state=0)
	vectors = tsne.fit_transform(vectors)

	x_vals = [v[0] for v in vectors]
	y_vals = [v[1] for v in vectors]
	return x_vals, y_vals, labels

base_path = os.getcwd()
model = gensim.models.Word2Vec.load(base_path+"/hw/static/assets/model/v2c_cbow_s100e25_new.model")
total = 0
for i in model.wv.key_to_index:
  total = total + model.wv.get_vecattr(i, "count")



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

def DashBoard(txt):
	#model is a dict
	ps = PorterStemmer()
	img = ''''''
	lukup = txt
	name = []
	rate = []
	typs = []
	zoom = []
	if txt == '-info' or txt == '-chk' or txt == '-nxt':
		total = 0
		fp = open(base_path+"/hw/static/assets/docs/info", "r")
		in4 = fp.read()
		fp.close()
		in4 = ast.literal_eval(in4)
		for i in model.wv.key_to_index:
			total = total + model.wv.get_vecattr(i, "count")
		ct = 0
		for key, value in in4.items():
			name.append(key)
			rate.append(float("{:.5f}".format((value/total)*100)))
			zoom.append(float("{:.2f}".format(value/total))*100)
			ct = ct + 1
			if ct == 10:
				break;
		lukup = "INFOMATION(%)"
	else:
		try:
			ans = model.wv.most_similar([ps.stem(txt)], topn=10)
			for i in range(10):
				name.append(ans[i][0])
				rate.append(float("{:.5f}".format(ans[i][1])))
				zoom.append(float("{:.2f}".format(ans[i][1]))*100)
		except:
			lukup = txt + " not found in Word2Vec model!"

	for i in rate:
		if i <= 0.4:
			typs.append('bg-danger')
		elif i > 0.4 and i < 0.8:
			typs.append('bg-warning')
		else:
			typs.append('bg-success')
	if txt == '-info':
		img = '''/static/assets/img/all.png'''
	elif txt == "-chk":
		img = '''/static/assets/img/rank.png'''
	elif txt == "-nxt":
		img = ''''''
	else:
		try:
			ans = model.wv.most_similar([ps.stem(txt)], topn=10)
			img = '''/static/assets/img/'''+ps.stem(txt)+'''.png'''
			print(img)
			if not os.path.isfile(base_path+"/hw/"+img):
				img = ""
				print("----"+txt+" img file is not exist.")
		except Exception as e:
			img = ""
			print(e)
	info = zip(name, rate, typs, zoom)
	cntxt = {'txt': lukup, 'img': img, 'info': info}
	return cntxt

def calc_idfmtx(func4idf, idf_count, tw, ts):
	mtx = [0]*tw
	for idx, freq in enumerate(idf_count['_idf']):
		mtx[idx] = abs(func4idf(ts, freq))
	return mtx

def text_prepare(strr):
	import re
	strr = strr.lower()
	REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
	BAD_SYMBOLS_RE = re.compile('[^a-z\ ]')
	STOPWORDS = set(nltk.corpus.stopwords.words('english'))

	strr = REPLACE_BY_SPACE_RE.sub(" ", strr)
	strr = BAD_SYMBOLS_RE.sub("", strr)
	sent = " ".join([w for w in nltk.word_tokenize(strr) if w not in STOPWORDS]) 
	return sent

def calc_tf(func4tf, keys, remtx, text, tw, functype = 0):
	dyfreq = [0]*tw 
	text = text_prepare(text)
	for _old, new_ in zip(remtx['old'], remtx['new']):
		dystr = text.replace(_old, new_)
	dytoken = nltk.word_tokenize(dystr)
	for idx, i in enumerate(dytoken):
		for _old, new_ in zip(remtx['old'], remtx['new']):
			if i == new_:
				dytoken[idx] = _old
	for i in dytoken:
		tmp = keys.index[(keys['keys'] == i)].tolist()
		if len(tmp) == 1:
			dyfreq[tmp[0]] = dyfreq[tmp[0]]+1
		else:
			print(i)
	valy = 0
	if functype == 2:
		for i in dyfreq:
			if i > valy:
				valy = i
			print(valy)
	else:
		valy = len(dytoken)
	for i in range(tw):
		dyfreq[i] = func4tf(dyfreq[i], valy)
	return dyfreq, dytoken

def calc_buff(text, keys, remtx, tw):
	mtx = [0]*tw
	text = text_prepare(text)
	for _old, new_ in zip(remtx['old'], remtx['new']):
		dystr = text.replace(_old, new_)
	dytoken = nltk.word_tokenize(dystr)
	for idx, i in enumerate(dytoken):
		for _old, new_ in zip(remtx['old'], remtx['new']):
			if i == new_:
				dytoken[idx] = _old
	for i in dytoken:
		tmp = keys.index[(keys['keys'] == i)].tolist()
		if len(tmp) == 1:
			mtx[tmp[0]] = 2
	tko = nltk.pos_tag(dytoken)
	total = 0
	for i, j in tko:
		idx = keys.index[(keys['keys'] == i)].tolist()
		if len(idx) == 1:
			# if j == "NN" or j == "NNS":
			# 	total = total + 2
			# elif j == "JJ" or j == "JJS" or j == "JJR" or j == "RB " or j == "RBE" or j == "RBS":
			# 	total = total + 10
			# elif j == "VB" or j == "VBN" or j == "VBD":
			# 	total = total + 5
			# else:
			total = total + 1
	for i, j in tko:
		idx = keys.index[(keys['keys'] == i)].tolist()
		if len(idx) == 1:
			# if j == "NN" or j == "NNS":
			# 	mtx[idx[0]] = 2*len(tko)/total
			# elif j == "JJ" or j == "JJS" or j == "JJR" or j == "RB " or j == "RBE" or j == "RBS":
			# 	mtx[idx[0]] = 10*len(tko)/total
			# elif j == "VB" or j == "VBN" or j == "VBD":
			# 	mtx[idx[0]] = 5*len(tko)/total
			# else:
			mtx[idx[0]] = len(tko)/total
			print(i, j)
	q = 0
	for i in mtx:
		q = q + i

	print(q)
	return mtx

def sort_cossim(text, ttf, tidf):
	from numpy import dot
	from numpy.linalg import norm
	result = {}
	cntxt = []
	cossim = []
	varset = []
	tfchecked = ["", "", ""]
	idfchecked = ["", "", ""]

	tf_nat = lambda x, y: x/y
	tf_log = lambda x, y: math.log(1+x)
	tf_aug = lambda x, y: 0.5+0.5*((x)/(y))
	'''------------------------------------'''
	idf_nat = lambda x, y: math.log(x/(1+y))
	idf_smt = lambda x, y: math.log(x/(1+y))+1
	idf_pro = lambda x, y: math.log((x-y)/(1+y))
	if ttf == 1:
		tf_func = tf_log
		tfchecked[1] = "checked"
	elif ttf == 2:
		tf_func = tf_aug
		tfchecked[2] = "checked"
	else:
		tf_func = tf_nat
		tfchecked[0] = "checked"
	if tidf == 1:
		idf_func = idf_smt
		idfchecked[1] = "checked"
	elif tidf == 2:
		idf_func = idf_pro
		idfchecked[2] = "checked"
	else:
		idf_func = idf_nat
		idfchecked[0] = "checked"
	if text_prepare(text) == "":
		return cntxt, cossim, varset, text, tfchecked, idfchecked

	tf = pd.read_csv(base_path+"/hw/static/assets/docs/tfidf/tf.csv")
	dfidf_count = pd.read_csv(base_path+"/hw/static/assets/docs/tfidf/idf_count.csv") 
	dfremtx = pd.read_csv(base_path+"/hw/static/assets/docs/tfidf/dict.csv")
	dfkeys = pd.read_csv(base_path+"/hw/static/assets/docs/tfidf/keys.csv")
	dfbook = pd.read_csv(base_path+"/hw/static/assets/docs/tfidf/book.csv")
	ts = int(tf['freq'][1])
	tw = int(tf['freq'][2])
	idfmtx = calc_idfmtx(idf_func, dfidf_count, tw, ts)
	Amtx, token = calc_tf(tf_func, dfkeys, dfremtx, text,  tw, ttf)

	Awei = np.multiply(Amtx, idfmtx)
	for i, j in enumerate(Awei):
		if j > 0:
			print(i, j)
	#Abuff = calc_buff(text, dfkeys, dfremtx, tw)
	#Awei = np.multiply(Awei, Abuff)
	for i in range(ts):
		sent = dfbook['processed'][i]
		flag = True
		for j in token:
			if sent.find(j) == -1:
				flag = False
				break
		if flag == False:
			continue
		Bmtx, tmp = calc_tf(tf_func, dfkeys, dfremtx, sent, tw, ttf)
		Bwei = np.multiply(Bmtx, idfmtx)
		if norm(Awei) == 0:
			angle = 0
		else:
			angle = dot(Awei, Bwei)/(norm(Awei)*norm(Bwei))
		result[i] = angle
	result = sorted(result.items(), key=lambda x:x[1], reverse = True)
	leng = len(result)
	if leng > 1:
		total = 0
		tmp = [j for i, j in result]
		var = statistics.variance(tmp)
		for i, j in result:
			total = total + j
		total = total/leng
		for idx, val in result:
			cntxt.append(dfbook['nonprocessed'][idx])
			cossim.append(float("{:.5f}".format((val))))
			varset.append(float("{:.5f}".format((val-total)/np.sqrt(var))))
	elif leng == 1:
		for idx, val in result:
			cntxt.append(dfbook['nonprocessed'][idx])
			cossim.append(float("{:.5f}".format((val))))
			varset.append(float("{:.5f}".format(100)))
	sent = text
	return cntxt, cossim, varset, sent, tfchecked, idfchecked