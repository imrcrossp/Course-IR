# IR Homework
## New Features 

> - Zipf Distribution computation
> - Matching (or partial matching) process

##### Overview 
> ###### v2.
>  - Zipf Distribution computation, matching (or partial matching) process.
> ###### v1.
> - calculate the document statistics ( number of characters, number of words, number of sentences(EOS))

## How
> - javascript 負責處理動態的資訊，python 負責後端資料處理
> - javascript 為主，用動態方式建立表格處理文件、尋找關鍵字。
> - 預先建構資料庫，包含10000資料的相關資訊


## Try!
>>由於 nltk 安裝較麻煩，需要先確認是否有package\
>>>\> pip3 install nltk
>>>\> python3
>>>\>>> import nltk
>>>\>>> nltk.download("popular")
> - 安裝 django
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
