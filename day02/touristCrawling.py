## 데이터포털 API 크롤링

import os
from pydoc import isdata
from pyexpat import native_encoding
import re
from sqlite3 import paramstyle
import sys
from tkinter import NE
from tkinter.messagebox import RETRY
from tkinter.ttk import Notebook
import urllib.request
import datetime
import time
import json
import pandas as pd


ServiceKey = "Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D"


#url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url) #request객체 만들기

    try:    #예외처리 try: except ~
        res = urllib.request.urlopen(req)   #요청받은 url 접속해서 열어주기
        if res.getcode() == 200: #200번대:OK, 400번대:Error, 500번대:ServerError
            print(f"[{datetime.datetime.now()}] Url Request success") #datetime.datetime.now() 타임스탬프
            return res.read().decode("utf-8")
    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None


def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    #연월, 국가코드, 출입국코드(E/D)
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    #공공데이터포털에서 미리보기하면 나오는 사이트
    params = f"?_type=json&serviceKey={ServiceKey}" #인증키
    #parameters, get parameter->나중에 url과 함께 한번에 넘겨줌
    #처음 시작할때는 ?로 시작, 그 후부터는 &로 구분, 키={value}
    params += f"&YM={yyyymm}"
    params += f"&NAT_CD={nat_cd}"
    params += f"&ED_CD={ed_cd}"
    url = service_url + params

    #print(url)
    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ""
    dataEnd = f"{nEndYear}{12:0>2}"
    isDataEnd = False #데이터 끝 확인용 flag

    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if isDataEnd == True:
                break
            
            yyyymm = f"{year}{month:0>2}"
            #month가 두 자리가 안되면 앞에 0넣어줌
            #2022 1월->202201로 만들어줌/안하면 20221로 나옴
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            if jsonData["response"]["header"]["resultMsg"] == "OK":
                if jsonData["response"]["body"]["items"] == "":  #데이터가 없는 경우라면 서비스 종료
                    isDataEnd =True
                    dataEnd = f"{year}{month-1:0>2}"
                    print(f"제공되는 데이터는 {year}년 {month-1}월까지 입니다.")
                    break
            print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
            natName = jsonData["response"]["body"]["items"]["natKorNm"]
            natName = natName.replace(" ", "") # 중  국 -> 중국 (여백 제거)
            num = jsonData["response"]["body"]["items"]["num"]
            ed = jsonData["response"]["body"]["items"]["ed"]

            jsonResult.append(
                {"nat_name" : natName},
                {"nat_cd" : nat_cd},
                {"yyyymm": yyyymm},
                {"visit_cnt": num},
            )
            result.append([natName, nat_cd, yyyymm, num])
    
    return (jsonResult, result, natName, ed, dataEnd)

          


def main():
    jsonResult = []
    result = []
    natName = ""
    ed = ""
    dataEnd = ""
    print("<< 국내 입국한 외국인 통계데이터를 수집합니다 >>")
    nat_cd = input("국가코드 입력(중국 : 112 / 일본 : 130 / 필리핀 : 155) :> ")
    nStartYear = int(input("데이터를 몇년부터 수집할까요?"))
    nEndYear = int(input("데이터를 몇년까지 수집할까요?"))
    ed_cd = "E" # D:한국인 외래 관광객 / E:방한외국인

    #getTourismStatsItem(nEndYear, nat_cd, ed_cd)
    (jsonResult, result, natName,ed, dataEnd) = \
        getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)
    
    if natName == "":
        print("데이터 전달 실패. 공공데이터포털 서비스 확인요망")
    else:
        """
        with open("./%s_%s_%d_%s.json" % (natwName, ed, nStartYear, dataEnd), "w", encoding = "utf-8") as outfile
        """
    

if __name__ == "__main__":
    main()

