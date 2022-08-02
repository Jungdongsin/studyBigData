from asyncore import read
import os
import re
from socket import TCP_NODELAY
import sys
from turtle import hideturtle
import urllib.request
import urllib.parse
import datetime
import time
import json
from xml.etree.ElementPath import _SelectorContext

#네이버 개발자 애플리케이션 ID,Secret 가져오기
client_id = "JJLJeMkKYWKG3IW4fcPD"
client_secret = "jRTJd32ESR"

#url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url) #request객체 만들기
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:    #예외처리 try: except ~
        res = urllib.request.urlopen(req)   #요청받은 url 접속해서 열어주기
        if res.getcode() == 200: #200번대:OK, 400번대:Error, 500번대:ServerError
            print(f"[{datetime.datetime.now()}] Url Request success") #datetime.datetime.now() 타임스탬프
            return res.read().decode("utf-8")
    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search" 
    #base:검색url의 기본 주소
    node = f"/{node}.json"
    #node:검색 대상에 따른 json파일 이름
    text = urllib.parse.quote(srcText)  # url주소에 맞춰서 파싱(parsing) -> srcText 인코딩
    params = f"?query={text}&start={start}&display={display}"
    #parameter:url에 추가할 검색어와 검색 시작 위치, 출력 건수 등의 매개변수

    url = base+node+params  #url 구성하기
    resDecode = getRequestUrl(url)

    if resDecode == None:
        return None
    else:
        return json.loads(resDecode) #요청 결과를 응답(json파일로) 받기


"""
json형식의 응답 데이터를 필요한 항목만 정리하여 
딕셔너리 리스트인 jsonResult를 구성하고 반환
"""
#getPostData() : 검색 결과 한 개를 처리
def getPostData(post, jsonResult, cnt):
    #post : 응답으로 받은 검색 결과 대아토 중에서 결과 한 개를 저장한 객체
    #jsonResult : 필요한 부분만 저장하여 반환할 리스트 객체
    title = post["title"]
    description = post["description"]
    originallink = post["originallink"]
    link = post["link"]

    pubDate = datetime.datetime.strptime(post["pubDate"], "%a, %d %b %Y %H:%M:%S +0900")
    #datetime.datetime.strptime() : 문자열을 날짜 객체 형식으로 변환
    pubDate = pubDate.strftime("%Y-%m-%d %H:%M:%S") #2022-08-02 15:56:34
    #pubDate.strftime() : 날짜 객체의 표시 형식을 지정
    jsonResult.append({"cnt" : cnt, "title" : title, "description" : description,
                        "originallink" : originallink, "link" : link, "pubDate" : pubDate})
    #jsonResult.append() : 리스트 객체인 jsonResult에 원소 추가
    #{"키":값}으로 구성


# 실행 최초 함수
def main():
    node = "news" #검색할 대상 노드
    srcText = input("검색어를 입력하세요 : ") #검색어
    cnt = 0
    jsonResult = [] #search 후 json형태를 list로 받기

    jsonRes = getNaverSearch(node, srcText, 1, 50) #1부터 50개의 검색결과 처리
    #print(jsonRes)
    total = jsonRes["total"] #검색된 총 뉴스 개수

    while ((jsonRes != None) and (jsonRes["display"] != 0)):
        for post in jsonRes["items"]:
            cnt += 1
            getPostData(post, jsonResult, cnt)
        start = jsonRes["start"] + jsonRes["display"] 
        # 1(스타트) + 50(display) = 51 / 한번 반복 후 다음 시작은 51부터 계속
        jsonRes = getNaverSearch(node, srcText, start, 50) #반복
    print(f"전체 검색 : {total} 건")


#file output
    with open(f"./{srcText}_naver_{node}.json", mode="w", encoding="utf-8") as outfile:
        #mode="w" : 입출력 모드는 writing, encoding은 utf-8로
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        #json.dumps() : 객체를 json형식으로 한번에 저장
        #.dumps(): 한번에 넣는 함수 # indent : 들여쓰기, sort : 정렬, ensure_ascii : ascii안쓰고 utf-8사용
        #.dump(): 하나씩 넣는
        outfile.write(jsonFile)

    print(f"가져온 데이터 : {cnt}건")
    print(f"{srcText}_naver_{node}.json SAVED") #파일 저장

if __name__ == "__main__": #메인 엔트리 포인트을 나타내주는거(내장변수)
    main()
 
