import requests
import os
from bs4 import BeautifulSoup
import time
from urllib import robotparser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import numpy as np
import pandas as pd

"""If you get a depricated error use this"""
s = Service('C:/Users/Caelan Osman/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(executable_path="C:/Users/Caelan Osman/Downloads/chromedriver_win32/chromedriver.exe")
'''Otherwise use this'''
# driver = webdriver.Chrome(executable_path="C:/Users/Caelan Osman/Downloads/chromedriver_win32/chromedriver.exe")


columns = ["Time", "Temp", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust", "Pressure", "Precip", "Condition"]
enddata = pd.DataFrame(columns=columns)



month_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]
try:
    for j in range(10,13):
        for k in range(1,month_lengths[j]+1):
            total_array = []
            driver.get(f'https://www.wunderground.com/history/daily/us/ca/burbank/KBUR/date/2018-{j}-{k}')
            time.sleep(1)
            tables = driver.find_elements(By.TAG_NAME, 'table')
            for table in tables:
                attribute = table.get_attribute("class")
                if attribute == "mat-table cdk-table mat-sort ng-star-inserted":
                    tbody = table.find_element(By.TAG_NAME, 'tbody')
                    rows = table.find_elements(By.TAG_NAME, 'tr')
                    for row in rows:
                        table_datas = row.find_elements(By.TAG_NAME, 'td')
                        table_row = []
                        for data in table_datas:
                            table_row.append(str(data.get_attribute("innerText").replace(u'\xa0', u' ')))
                        total_array.append(np.array(table_row))
            enddata.loc[len(enddata.index)] = [f"Month {j} Day {k}"]*10
            enddata = enddata.append(pd.DataFrame(total_array[1:-10], columns=columns))
except:
    print("Tell Bryce if this prints")
finally:
    driver.close()
    enddata.to_csv("LA_data4.csv")