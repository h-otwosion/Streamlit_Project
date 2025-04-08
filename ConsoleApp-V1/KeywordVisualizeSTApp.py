import os
import streamlit as st
from konlpy.tag import Okt
import mylib.myTextMining as tm
import mylib.NaverNewsCrawler as NNC
import mylib.STVisualizer as STV

# filename not define 문제해결
if "filename" not in st.session_state:
    st.session_state["filename"] = None

with st.form("my_form"):
    st.write("한글키워드 검색")

    # 사용자 입력
    keyword = st.text_input("키워드 입력")
    checkbox_CSV = st.checkbox("CSV 저장하기")
    submitted = st.form_submit_button("검색")

    # 검색 버튼을 눌렀을 때
    if submitted:
        st.write("keyword", keyword, "checkbox", checkbox_CSV)
        start = 1
        display = 10
        resultJSON = NNC.searchNaverNews(keyword, start, display)
        resultAll = []

        # 뉴스 데이터를 수집
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
        
        # CSV 저장 체크박스가 선택되었는지 확인
        if checkbox_CSV:
            os.makedirs(os.path.dirname(st.session_state["filename"]), exist_ok=True)
            NNC.saveSearchResult_CSV(resultAll, st.session_state["filename"])
            st.success(f"CSV 파일이 저장되었습니다: {st.session_state['filename']}")
        else:
            st.warning("CSV 저장이 선택되지 않았습니다.")

        # filename = f"./data/{keyword}_naver_news.csv"
        # if checkbox_CSV:
        #     input_filename = os.path.basename(filename)
        #     NNC.saveSearchResult_CSV(resultAll, filename)
        #     corpus_list = tm.load_corpus_from_csv("./data/" + input_filename, "description")

st.write("**설정**")

with st.form("my_form2"):
    # 빈도수 그래프 옵션
    checkbox_grf = st.checkbox("빈도수 그래프")
    slider_wordNumG = st.slider("단어 수", 10, 50, 20)

    # 워드클라우드 옵션
    checkbox_wordCloud = st.checkbox("워드클라우드")
    slider_wordNumC = st.slider("단어 수", 20, 500, 50)

    # 분석 버튼
    submitted2 = st.form_submit_button("분석 시작")
    if submitted2:
        # CSV 파일이 생성되었는지 확인
        if st.session_state["filename"] is None:
            st.error("파일이 생성되지 않았습니다. 첫 번째 폼에서 CSV를 저장하세요!")
        else:
            st.write("checkbox", checkbox_grf, "slider", slider_wordNumG,
                     "checkbox", checkbox_wordCloud, "slider", slider_wordNumC)

            if checkbox_grf:
                # 코퍼스 로딩
                # input_filename = os.path.basename(filename)
                input_filename = os.path.basename(st.session_state["filename"])
                corpus_list = tm.load_corpus_from_csv("./data/" + input_filename, "description")


                # 빈도수 추출
                my_tokenizer = Okt().pos
                my_tags = ['Noun', 'Adjective', 'Verb']
                my_stopwords = ['입니다', '의', '고', '그', '할', '이', '등', '것', '된', '하지', '전', '라며', '더', '며', '단',
                                '이어', '있다', '매우', '보여진다', '보인다', '했습니다', '있습니다', '이다', '된다', '이번', '통해',
                                '하는', '한', '해', '향', '저', '날', '수', '말', '했다', '출처', '오후', '바로', '모든', '는'
                                '불', '두', '한다', '합니다', '여전히', '도', '은', '때', '말라', '또', '개월', '겪은', '큰', '될'
                                '김', '제', '위', '해야', '그러면서']
                counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)

                # 그래프 출력
                chart = STV.visualize_barchart_st(counter, "키워드 분석", "빈도수", "키워드", slider_wordNumG)
                st.pyplot(chart)

            if checkbox_wordCloud:
                wordcloud = STV.visualize_wordcloud_st(counter, slider_wordNumC)
                st.pyplot(wordcloud)