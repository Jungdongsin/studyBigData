from asyncore import read
import os
import re
import sys
from turtle import hideturtle
import urllib.request
import urllib.parse
import datetime
import time
import json
from xml.etree.ElementPath import _SelectorContext

#네이버 개발자 애플리케이션 ID,Secret
client_id = "JJLJeMkKYWKG3IW4fcPD"
client_secret = "jRTJd32ESR"

#url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url) #request객체 만들기
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:    #예외처리 try: except ~
        res = urllib.request.urlopen(req)   #url접속과 검색 요청하기
        if res.getcode() == 200: #200:OK, 400:Error, 500:ServerError
            print(f"[{datetime.datetime.now()}] Url Request success")
            return res.read().decode("utf-8")
    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None
        
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = f"/{node}.json"
    text = urllib.parse.quote(srcText)  # url주소에 맞춰서 파싱(parsing) -> srcText 인코딩
    params = f"?query={text}&start={start}&display={display}"

    url = base+node+params  #url 구성하기
    resDecode = getRequestUrl(url)

    if resDecode == None:
        return None
    else:
        return json.loads(resDecode) #요청 결과를 응답(json파일로) 받기

def getPostData(post, jsonResult, cnt):
    title = post["title"]
    description = post["description"]
    originallink = post["originallink"]
    link = post["link"]

    pubDate = datetime.datetime.strptime(post["pubDate"], "%a, %d %b %Y %H:%M:%S +0900")
    pubDate = pubDate.strftime("%Y-%m-%d %H:%M:%S") #2022-08-02 15:56:34

    jsonResult.append({"cnt" : cnt, "title" : title, "description" : description,
                        "originallink" : originallink, "link" : link, "pubDate" : pubDate})


# 실행 최초 함수
def main():
    node = "news"
    srcText = input("검색어를 입력하세요 : ")
    cnt = 0
    jsonResult = []

    jsonRes = getNaverSearch(node, srcText, 1, 50)
    #print(jsonRes)
    total = jsonRes["total"] #검색된 뉴스 개수

    while ((jsonRes != None) and (jsonRes["display"] != 0)):
        for post in jsonRes["items"]:
            cnt += 1
            getPostData(post, jsonResult, cnt)
        start = jsonRes["start"] + jsonRes["display"] # 1(스타트) + 50(display) = 51개부터 계속
        jsonRes = getNaverSearch(node, srcText, start, 50)
    print(f"전체 검색 : {total} 건")


#file output
    with open(f"./{srcText}_naver_{node}.json", mode="w", encoding="utf-8") as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        #.dumps(): 한번에 넣는 함수 # indent : 들여쓰기, sort : 정렬, ensure_ascii : 안쓰고 utf-8사용
        #.dump(): 하나씩 넣는
        outfile.write(jsonFile)

    print(f"가져온 데이터 : {cnt}건")
    print(f"{srcText}_naver_{node}.json SAVED")

if __name__=="__main__": #메인 엔트리 포인트을 나타내주는거(내장변수)
    main()

