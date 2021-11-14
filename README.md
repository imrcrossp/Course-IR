# IR Homework
## New Features 

> - Add a button for the new site about statistics.
> - In that site, including CBOW and some graphs, showing the cosine similarity of words.

##### Overview
> ###### v3.
>  - CBOW and some graphs, showing the cosine similarity of words.
> ###### v2.
>  - Zipf Distribution computation, matching (or partial matching) process.
> ###### v1.
> - calculate the document statistics ( number of characters, number of words, number of sentences(EOS))

## How
> - javascript 負責處理動態的資訊，python 負責後端資料處理。
> - javascript 為主，用動態方式建立表格處理文件、尋找關鍵字。
> - 預先建構資料庫，包含10000資料的相關資訊。
> - 透過 CBOW 將1000文件中的句子分析，建立 Model 方便查詢。


## Try!
>>由於 nltk 安裝較麻煩，需要先確認是否有package
>>>\> pip3 install nltk <br>
>>>\> python3 <br>
>>>\>>> import nltk <br>
>>>\>>> nltk.download("popular")<br>
>>>\> pip install -r requirements.txt
> - 安裝 django
> - ./init_key
> -  python manage.py migrate 
> -  python manage.py runserver [ip:port]

## Problems? Bugs?
> Only edit distance and substring matching can't deal with the partial matching problem well.
>
>
> No Bugs, Only Features.

## History Bug
> ##### v1.
> - 測試中 Chrome 無法正常運作 oninput，故用 change 代替。
> >Solution : oninput結束後，focus回物件。
