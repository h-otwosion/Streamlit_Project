import streamlit as st
from konlpy.tag import Okt
import os
import mylib.myTextMining as tm
import mylib.NaverNewsCrawler as NNC
import mylib.STVisualizer as STV

# filename 초기화
if "filename" not in st.session_state:
    st.session_state["filename"] = None

# 검색 폼 (사이드바)
with st.sidebar.form("search_form"):
    st.write("**한글키워드 검색**")
    keyword = st.text_input("키워드 입력")
    checkbox_CSV = st.checkbox("CSV 저장하기")
    submitted_search = st.form_submit_button("검색")

    # 검색 로직 처리 및 폼 아래 메시지 출력
    if submitted_search:
        if not keyword.strip():
            st.error("키워드가 입력되지 않았습니다. 검색어를 입력하세요!")
        else:
            start = 1
            display = 10
            resultJSON = NNC.searchNaverNews(keyword, start, display)
            resultAll = []

            # 뉴스 데이터 수집
            while (resultJSON is not None) and (resultJSON['display'] > 0):
                NNC.setNewsSearchResult(resultAll, resultJSON)
                start += resultJSON['display']
                resultJSON = NNC.searchNaverNews(keyword, start, display)
                if start > 99:
                    break
                if resultJSON is not None:
                    print(f"{keyword} [{start}] : Search Request Success")
                else:
                    print(f"{keyword} [{start}] : Error ~~~~")

            st.session_state["filename"] = f"./data/{keyword}_naver_news.csv"

            # CSV 저장 여부 확인
            if checkbox_CSV:
                os.makedirs(os.path.dirname(st.session_state["filename"]), exist_ok=True)
                NNC.saveSearchResult_CSV(resultAll, st.session_state["filename"])
                st.success(f"CSV 파일이 저장되었습니다: {st.session_state['filename']}")
            else:
                st.warning("CSV 저장이 선택되지 않았습니다.")

# 설정 폼 (사이드바)
with st.sidebar.form("settings_form"):
    st.write("**설정**")
    checkbox_grf = st.checkbox("빈도수 그래프")
    slider_wordNumG = st.slider("단어 수 (그래프)", 10, 50, 20)
    checkbox_wordCloud = st.checkbox("워드클라우드")
    slider_wordNumC = st.slider("단어 수 (워드클라우드)", 20, 500, 50)
    submitted_settings = st.form_submit_button("분석 시작")

    # 설정 폼 메시지 처리
    if submitted_settings:
        if st.session_state["filename"] is None:
            st.error("파일이 생성되지 않았습니다. 첫 번째 폼에서 CSV를 저장하세요!")
        else:
            st.success("단어빈도수그래프와 워드클라우드가 생성되었습니다!")

# 분석 및 결과 출력 로직 (메인 화면)
if submitted_settings and st.session_state["filename"] is not None:
    st.write("선택한 옵션:")
    st.write(f"빈도수 그래프: {checkbox_grf}, 단어 수 (그래프): {slider_wordNumG}")
    st.write(f"워드클라우드: {checkbox_wordCloud}, 단어 수 (워드클라우드): {slider_wordNumC}")

    # CSV 파일 로딩
    input_filename = os.path.basename(st.session_state["filename"])
    corpus_list = tm.load_corpus_from_csv("./data/" + input_filename, "description")

    # 단어 빈도수 계산
    my_tokenizer = Okt().pos
    my_tags = ['Noun', 'Adjective', 'Verb']
    my_stopwords = ['입니다', '의', '고', '그', '할', '이', '등', '것', '된', '하지', '전', '라며', '더', '며', '단',
                    '이어', '있다', '매우', '보여진다', '보인다', '했습니다', '있습니다', '이다', '된다', '이번', '통해',
                    '하는', '한', '해', '향', '저', '날', '수', '말', '했다', '출처', '오후', '바로', '모든', '는'
                    '불', '두', '한다', '합니다', '여전히', '도', '은', '때', '말라', '또', '개월', '겪은', '큰', '될'
                    '김', '제', '위', '해야', '그러면서']
    counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)

    # 빈도수 그래프 출력
    if checkbox_grf:
        chart = STV.visualize_barchart_st(counter, "키워드 분석", "빈도수", "키워드", slider_wordNumG)
        st.pyplot(chart)

    # 워드클라우드 출력
    if checkbox_wordCloud:
        wordcloud = STV.visualize_wordcloud_st(counter, slider_wordNumC)
        st.pyplot(wordcloud)