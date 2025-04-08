import os
import mylib.myTextMining as tm
import mylib.NaverNewsCrawler as NNC
from konlpy.tag import Okt

keyword = NNC.setNewsSearchKeyword()
start=1
display=10
resultJSON = NNC.searchNaverNews(keyword, start, display)
resultAll = []

while (resultJSON != None) and (resultJSON['display'] > 0):
    NNC.setNewsSearchResult(resultAll, resultJSON)
    start += resultJSON['display']

    resultJSON = NNC.searchNaverNews(keyword, start, display)

    if start > 99:
        break

    if resultJSON != None:
        print(f"{keyword} [{start}] : Search Request Success")
    else:
        print(f"{keyword} [{start}] : Error ~~~~")

filename = f"./data/{keyword}_naver_news.csv"
NNC.saveSearchResult_CSV(resultAll, filename)

# 코퍼스 로딩
input_filename = os.path.basename(filename)
corpus_list = tm.load_corpus_from_csv("./data/" + input_filename, "description")

# 빈도수 추출
my_tokenizer = Okt().pos
my_tags = ['Noun', 'Adjective', 'Verb']

# my_tokenizer = Komoran().pos
# my_tags = ['NNG', 'NNP', 'VV', 'VA']

my_stopwords = []
counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)
print(list(counter.items())[:20])
#tm.visualize_barchart(counter, "다음 영화 리뷰 키워드 분석", "빈도수", "키워드")
tm.visualize_wordcloud(counter)