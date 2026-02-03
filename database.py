import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time
from datetime import datetime

def fetch_job():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 啟動自動抓取任務...")
# 1. 抓取外部資料 (需要強制指定編碼)
    rss_url = "https://news.google.com/rss/search?q=i-dle&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
       
    try:
        response = requests.get(rss_url)
        response.encoding = 'utf-8'  # 強制指定編碼

        if response.status_code == 200:
            # 這裡就是你說的「強制指定」，因為資料是從外面(網路)進來的
             
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')[:3]

            # 2. 存入內部資料庫 (這裡不需要再指定，因為 Python 與 SQLite 已經有默契了)
            conn = sqlite3.connect('idle_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    news TEXT
                )
            ''')
            
            for item in items:
                # 直接存入，Python 會自動處理好
                cursor.execute("INSERT INTO members (name, news) VALUES (?, ?)", ("i-dle News", item.title.text))
            
            conn.commit()
            conn.close()
            print("任務完成：資料已成功存入資料庫。")
        else:
            print(f"抓取失敗，代碼：{response.status_code}")
            
    except Exception as e:
        print(f"發生錯誤：{e}")
