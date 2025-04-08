import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# wordcloud 웹페이지에
# 
# #bar chart 웹페이지지

def visualize_barchart_st(counter, title, xlabel, ylabel, slider_wordNumG):
    
# 한글 폰트 설정
    font_path = "c:/Windows/Fonts/malgun.ttf"  # 폰트 경로
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    # 데이터 준비
    most_common = counter.most_common()  # 전체 단어 빈도 리스트 반환
    most_common = most_common[:slider_wordNumG]  # 슬라이더로 지정한 개수만큼 가져오기
    word_list = [word for word, _ in most_common]  # 단어 추출
    count_list = [count for _, count in most_common]  # 빈도수 추출

    # 막대그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.barh(word_list[::-1], count_list[::-1])  # 역순으로 정렬하여 수평 막대그래프 생성
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    return plt



def visualize_wordcloud_st(counter, slider_wordNumC):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # 한글 폰트 path 지정
    font_path = "c:/Windows/fonts/malgun.ttf"

    # WordCloud 객체 생성
    wordcloud = WordCloud(font_path,
                      width=600,
                      height=400,
                      max_words=slider_wordNumC,
                      background_color='ivory')
    
    # 빈도 데이터로 워드클라우드 시각화
    wordcloud = wordcloud.generate_from_frequencies(counter)
    plt.imshow(wordcloud)
    plt.axis('off')

    return plt