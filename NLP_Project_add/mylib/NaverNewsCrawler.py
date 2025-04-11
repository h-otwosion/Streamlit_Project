import urllib.request
import json

def setNewsSearchKeyword():
    keyword = input("검색어 : ").strip()
    return keyword
#
def searchNaverNews(keyword, start, display):
    client_id = "fectRRiU4hHDSgWp0PYL"
    client_secret = "CRcxk6VH6p"

    # 한글 검색어 안전하게 변환
    encText = urllib.parse.quote(keyword)

    # url + query 생성
    url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과

    # request message 구성
    new_url = url + f"&start={start}&display={display}"
    request = urllib.request.Request(new_url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    resultJSON = None
    try:
        # request ->response 받아오기
        response = urllib.request.urlopen(request)

        #받아온 결과가 정상인지 확인
        rescode = response.getcode()
        if(rescode==200):
            #정상이면 데이터 읽어오기
            response_body = response.read()
            #한글이 있으면 Utf-8 decoding
            resultJSON = json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code: " + rescode)
    except Exception as e:
        print(e)
        print(f"Error : {new_url}")

    return resultJSON

def setNewsSearchResult(resultAll, resultJSON):
    for result in resultJSON['items']:
        resultAll.append(result)

def saveSearchResult_CSV(json_list, filename):
    import pandas as pd
    data_df = pd.DataFrame(json_list)
    data_df.to_csv(filename)
    print(f"{filename} SAVED")
