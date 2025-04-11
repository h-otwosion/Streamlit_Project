import streamlit as st
import pandas as pd
import os
import mylib.myTextMining as tm
import mylib.NaverNewsCrawler as NNC
import mylib.STVisualizer as STV
from konlpy.tag import Okt

# 페이지 설정: 와이드 레이아웃
st.set_page_config(layout="wide")

# 상태 초기화
if "filename" not in st.session_state:
    st.session_state["filename"] = None

# 옵션 선택 (사이드바)
st.sidebar.write("**작업 옵션 선택**")
option = st.sidebar.selectbox("옵션을 선택하세요", ["키워드 입력", "CSV 파일 업로드"])

# "키워드 입력" 폼
if option == "키워드 입력":
    with st.sidebar.form("keyword_form"):
        st.write("**한글키워드 검색**")
        keyword = st.text_input("키워드 입력")
        checkbox_CSV = st.checkbox("CSV 저장하기")
        submitted_keyword = st.form_submit_button("검색")

        if submitted_keyword:
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

# "CSV 파일 업로드" 폼
elif option == "CSV 파일 업로드":
    with st.sidebar.form("upload_form"):
        st.write("**CSV 파일 업로드**")
        uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
        submitted_upload = st.form_submit_button("업로드")

        if submitted_upload:
            if uploaded_file:
                try:
                    # CSV 파일 읽기
                    df = pd.read_csv(uploaded_file)
                    st.session_state["filename"] = f"./data/{uploaded_file.name}"
                    st.success("파일이 성공적으로 업로드되었습니다!")
                    st.write("업로드된 CSV 내용:")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"파일 업로드에 문제가 발생했습니다: {e}")
            else:
                st.error("파일이 업로드되지 않았습니다!")

# 설정 폼 (사이드바)
with st.sidebar.form("settings_form"):
    st.write("**설정**")
    checkbox_grf = st.checkbox("빈도수 그래프")
    slider_wordNumG = st.slider("단어 수 (그래프)", 10, 50, 20)
    checkbox_wordCloud = st.checkbox("워드클라우드")
    slider_wordNumC = st.slider("단어 수 (워드클라우드)", 20, 500, 50)
    submitted_settings = st.form_submit_button("분석 시작")

# 탭 구성 (메인 화면)
if submitted_settings and st.session_state["filename"] is not None:
    tab1, tab2, tab3 = st.tabs(["단어 빈도수 그래프", "워드클라우드", "기사 내용 요약"])

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
    counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords) #불용어 제거 머신러닝 옵션

    # 단어 빈도수 그래프 출력 (Tab 1)
    with tab1:
        st.header("단어 빈도수 그래프")
        if checkbox_grf:
            chart = STV.visualize_barchart_st(counter, "키워드 분석", "빈도수", "키워드", slider_wordNumG)
            st.pyplot(chart)

    # 워드클라우드 출력 (Tab 2)
    with tab2:
        st.header("워드클라우드")
        if checkbox_wordCloud:
            wordcloud = STV.visualize_wordcloud_st(counter, slider_wordNumC)
            st.pyplot(wordcloud)

    # 기사 내용 요약 (Tab 3)
    with tab3:
        st.header("기사 내용 요약")
        st.write("여기에 기사 요약 내용을 추가할 수 있습니다.")