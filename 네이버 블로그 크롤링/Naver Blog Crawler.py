#import csv
#import requests
#import time
import urllib.parse
from bs4 import BeautifulSoup
import re
from konlpy.tag import Okt
from wordcloud import WordCloud
#import nltk
from konlpy.tag import Twitter
import matplotlib.pyplot as plt
from collections import Counter


def searchOnePage(page_num,key,selct,self):
    blog_list=[]
    url = 'https://search.naver.com/search.naver?where=post&query='
    temp_url = url + urllib.parse.quote(key)+'&sm=tab_opt&data_option=4&start='+str(page_num)
    #req = urllib.request.Request(temp_url)
    sourcecode = urllib.request.urlopen(temp_url).read()
    soup = BeautifulSoup(sourcecode, 'html.parser')
    #'dd', 'sh_blog_passage' 내용
    # 'dt' 제목https://search.naver.com/search.naver?where=article&sm=tab_jum&query=
    
    for n in soup.find_all(selct):
        blog_list.append(n.get_text())
    return blog_list
    

def makeAllList():
    global key
    key=input('*검색할 대상을 입력해 주세요: ')
    nm = int(input('*검색 시작할 페이지를 입력해 주세요: '))
    if nm != 1:
        num = (nm*10)+1
    else:
        num = 1
    last_n=int(input('*검색 종료할 마지막 페이지를 입력해주세요: '))
    last_num= (last_n*10)+1
    num_list = [a for a in range(num,last_num,10)]
    new_list = []

    want2=input('*제목을 검색하고 싶으시면[제목] 내용을 검색하고 싶으시면[내용]을 입력하세요: ')
    if want2 == '제목':
        for a in num_list:
            new_list.append(searchOnePage(a,key,'dt',None))
    elif want2 == '내용':
        for a in num_list:
            new_list.append(searchOnePage(a,key,'dd', 'sh_blog_passage'))
    else:
        print('정확한 철자를 입력해주세요!')
        

    # 모든페이지 토큰화 리스트 llist 
    llist=[]
    for i in new_list:
        # 각 페이지별 토큰화 리스트 listt
        listt=[]
        for n in i:
            n = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','',n)
            okt =Okt()
            new=okt.nouns(n)
            new=okt.morphs(n)
            listt.append(new)
        stop_words=[key,'이','에','을','가','도','와','1','다','를','들','은','과','그','의','및']
        # 각페이지별로 스탑 워드로 토큰화된 리스트 nlist
        nlist = [each_word for each_word in listt if each_word not in stop_words]
        nlist.pop(0)
        nlist.pop(0)
        nlist.pop(-1)
        llist.append(nlist)
    
    # 모든 단어 집합 할 리스트
    for_all_list=[]
    # j=각 페이지별 리스트
    for j in llist:
        # i=페이지 내 각 게시물 리스트
        for i in j:
            # a=각 게시물 내 단어
            for a in i:
                for_all_list.append(a)

    for n, i in enumerate(for_all_list):
        if i == '대행':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '배달':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '이':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '를':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '은':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '의':
            for_all_list.pop(n)
    for n, i in enumerate(for_all_list):
        if i == '입니다':
            for_all_list.pop(n)
    return for_all_list




def make_wordcloud(word_count,f_list):
    twitter = Twitter()
    
    sentences_tag=[]
    for sentence in f_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
    
    noun_adj_list=[]
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun','Adjective']:
                noun_adj_list.append(word)
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    stwd=['은', '이' ,'를','의','등',key,'입니다',key[0],key[1]]
    print(dict(tags))
    wc = WordCloud(stopwords=stwd)
    wc = WordCloud(font_path='C:/Users/SAMSUNG/Downloads/Nanumsquare_ac_TTF/NanumSquare_acB.ttf',
                   background_color='white',
                   width=1000,
                   height=900).generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(wc)
    plt.show()
    
while True:
    print('='*60)
    print()
    print('안녕하세요 크롤링 시스템입니다.')
    ff_list=makeAllList()
    print('{}의 크롤링 결과입니다.'.format(key))
    make_wordcloud(100,ff_list)
    print()
    print('크롤링을 완료하였습니다.')
    print()
    print('='*60)
    want= input('*크롤링을 계속하시겠습니까?[네/아니오]: ')
    print()
    if want=='아니오':
        print('이용해주셔서 감사합니다. 시스템을 종료합니다.')
        break
    elif want == '네':
        continue
    else:
        print('정확한 철자를 입력해주세요!')


'''
wordcloud = WordCloud(
        width = 320,
        height=240,
        scale=2.0,
        background_color='white',
        max_words=20).generate(' '.join(for_all_list))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()'''