# 부산 갓맷길 정보 API 크롤링

import os
from pydoc import isdata
from pyexpat import native_encoding
import re
from sqlite3 import paramstyle
import sys
from tkinter import NE
from tkinter.messagebox import RETRY
from tkinter.ttk import Notebook
from unittest import result
import urllib.request
import datetime
import time
import json
import pandas as pd
import pymysql


serviceKey = "F0m%2B1YLdDR4l%2BPBtOGpiakML5a8jmHBZs7o9aDch6aYU%2FHK2AWeB9rGYvZ1N32SUC957ljuuTilYBxb0ucvaVQ%3D%3D"

def getRequestUrl(url):
    """
    URL 접속 요청 후 응답함수
    -------------------------
    parameter : url -> OpenAPI 전체 URL
    """
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


def getGalmatgilInfo():
    service_url = "http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo"
    params = f"?serviceKey={serviceKey}"
    params += "&numOfRows=10"
    params += "&pageNo=1"
    params += "&resultType=json"

    url = service_url + params

    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)


def getGalmatgilService():
    result = []

    jsonData = getGalmatgilInfo()
    #print(jsonData)
    if jsonData["getgmgcourseinfo"]["header"]["code"] == "00":
        if jsonData["getgmgcourseinfo"]["item"] == "":
            print("서비스 오류")
        else:
            for item in jsonData["getgmgcourseinfo"]["item"]:
                #print(item)
                seq = item["seq"]
                course_nm = item["course_nm"]
                gugan_nm = item["gugan_nm"]
                gm_range = item["gm_range"]
                gm_degree = item["gm_degree"]
                start_pls = item["start_pls"]
                start_addr = item["start_addr"]
                middle_pls = item["middle_pls"]
                middle_adr = item["middle_adr"]
                end_pls = item["end_pls"]
                end_addr = item["end_addr"]
                gm_course = item["gm_course"]
                gm_text = item["gm_text"]

                result.append([seq,course_nm,gugan_nm,gm_range,gm_degree,start_pls,start_addr,middle_pls,middle_adr,end_pls,end_addr,gm_course,gm_text])

    return result

def main():
    result = []

    print("부산 갈맷길코스를 조회합니다.")
    result = getGalmatgilService()

    if len(result) > 0:
        # csv파일 저장
        columns = ["seq","course_nm","gugan_nm","gm_range","gm_degree","start_pls","start_addr","middle_pls","middle_adr","end_pls","end_addr","gm_course","gm_text"]

        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv(f"./부산갈맷길정보.csv", index=False, encoding = "utf-8") #csv파일명

        print("csv파일 저장완료")

        # DB저장
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            db="crawling_data"
            )
        
        cursor = connection.cursor() #커서 객체가 있어야 실행 가능

        # 컬럼명 동적으로 만들기
        cols = "`,`".join([str(i) for i in result_df.columns.tolist()])
        #colums의 컬럼 이름을 리스트로 쭉 만듦
        
        for i, row in result_df.iterrows():
            #.iterrows() : 반복으로 돌면서 값들을 하나씩 만들어주는거
            sql = "INSERT INTO `galmatgil_info` (`" + cols + "`) VALUES(" + "%s,"*(len(row)-1) +"%s)"
            cursor.execute(sql, tuple(row))

        connection.commit()
        connection.close()

        print("DB저장 완료")


if __name__ == "__main__":
    main()