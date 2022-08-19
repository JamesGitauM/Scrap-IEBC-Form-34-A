from ast import pattern
from logging import exception
from math import radians
from multiprocessing.sharedctypes import Value
from posixpath import split
from re import search
import time
from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # Very important to import this
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os 


PATH="C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

# Wait till everything is loaded
# driver.implicitly_wait(700)

URL="https://forms.iebc.or.ke/#/"
COUNTY_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/a"""
COUNTY_REPORTED_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/span"""
CONST_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/a"""
CONST_REPORTED_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/span"""

WARD_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/a"""
WARD_REPORTED_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/span"""

POLL_CENTRE_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/a"""
POLL_CENTRE_REPORTED_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/span"""

POLL_STATION_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/span"""
POLL_STATION_STATUS_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/div/div/span"""
POLL_STATION_FORM_LNK_XPATH="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[3]/a"""




def get_results():
    directory=''
    df_counties_data=pd.DataFrame()
    try:
        # driver.implicitly_wait(15) #wait 15 seconds
        driver.get(URL)
        time.sleep(5)
        counties=WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,COUNTY_XPATH))
        )
        # counties=(driver.find_elements(by=By.XPATH,value=COUNTY_XPATH))
        county_reported_figures=WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,COUNTY_REPORTED_XPATH))
        )
        county_level_data=[]
        
        print(len(counties))
        for county in  range (len(counties)):
            county_data={'County':counties[county].text,
                        'Report': county_reported_figures[county].text,}
            directory=create_directory(counties[county].text)
            if not os.path.exists(counties[county].text):
                os.makedirs(counties[county].text)
            else:
                pass
            # cd to the current county folder
            os.chdir(directory)
            # get conts data
            county_link=driver.find_element(by=By.LINK_TEXT,value=counties[county].text)
            print('-----**')
            print(county_link)
            county_link.click()
            # time.sleep(2)
            get_constituency_data()
            print(driver.current_url)

                
            county_level_data.append(county_data)

        df_counties_data=pd.DataFrame(county_level_data)
        df_counties_data.to_excel('CountyLevelResults.xlsx',index=False)
     
    finally:
        # driver.quit()
        return df_counties_data

def get_constituency_data():
    df_const_data=pd.DataFrame()
    const_level_data=[]
    try:
        # driver.get(URL)
        # time.sleep(5)
        const=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,CONST_XPATH))
            )
        const_report_figures=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,CONST_REPORTED_XPATH))
            )
        for cons in range (len(const)):
            print(const[cons].text)
            const_data={'Constituency':const[cons].text,
                        'Report': const_report_figures[cons].text }
            directory=create_directory(const[cons].text)
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                pass
            # cd to the current county folder
            os.chdir(directory)
            const_link=driver.find_element(by=By.LINK_TEXT,value=const[cons].text)
            const_link.click()
            # get ward data
            get_ward_data()
            const_level_data.append(const_data)
        df_const_data=pd.DataFrame(const_level_data)
        df_const_data.to_excel('ConstituencyLevelResults.xlsx',index=False)
  
        
    finally:
        return df_const_data



        

def get_ward_data():
    df_ward_data=pd.DataFrame()
    ward_level_data=[]
    try:
        # driver.get(URL)
        # time.sleep(5)
        wards=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,WARD_XPATH))
            )
        ward_report_figures=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,WARD_REPORTED_XPATH))
            )
        for ward in range (len(wards)):
            print(wards[ward].text)
            ward_data={'Ward':wards[ward].text,
                        'Report': ward_report_figures[ward].text }
            directory=create_directory(wards[ward].text)
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
               pass
             # cd to the current wardfolder
            os.chdir(directory)
            ward_link=driver.find_element(by=By.LINK_TEXT,value=wards[ward].text)
            print(">>>>>>>>>>>>>>>>>>>>>>WARD")
            print(ward_link)
            ward_link.click()
            get_poll_centre_data()
                # get centre data
            ward_level_data.append(ward_data)
        df_ward_data=pd.DataFrame(ward_level_data)
        df_ward_data.to_excel('WardLevelResults.xlsx',index=False)
  
        
    finally:
        return df_ward_data


def get_poll_centre_data():
    print("POLING SHIET!")
    df_centre_data=pd.DataFrame()
    centre_level_data=[]
    try:
        # driver.get(URL)
        # time.sleep(5)
        poll_centres=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,POLL_CENTRE_XPATH))
            )
        poll_centre_report_figures=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,POLL_CENTRE_REPORTED_XPATH))
            )
        for centre in range (len(poll_centres)):
            print(poll_centres[centre].text)
            centre_data={'Polling Centre':poll_centres[centre].text,
                        'Report': poll_centre_report_figures[centre].text }
            directory=create_directory(poll_centres[centre].text)

            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                pass
            # cd to the current wardfolder
            os.chdir(directory)
            centre_link=driver.find_element(by=By.LINK_TEXT,value=poll_centres[centre].text)
            centre_link.click()
            get_poll_station_data()
                # get centre data
            centre_level_data.append(centre_data)
        df_centre_data=pd.DataFrame(centre_level_data)
        df_centre_data.to_excel('PollingCentreLevelResults.xlsx',index=False)
  
        
    finally:
        return df_centre_data



def get_poll_station_data():
    df_station_data=pd.DataFrame()
    station_level_data=[]
    try:
        # driver.get(URL)
        # time.sleep(5)
        poll_stations=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,POLL_STATION_XPATH))
            )
        poll_station_status=WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.XPATH,POLL_STATION_STATUS_XPATH))
            )
        pdf_links=WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,POLL_STATION_FORM_LNK_XPATH))
        )
        for station in range (len(poll_stations)):
            station_data={'Polling Station':poll_stations[station].text,
                        'Status': poll_station_status[station].text
                        }
            directory=poll_stations[station].text
            station_link=WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,POLL_STATION_FORM_LNK_XPATH))).click()
           
           
            station_level_data.append(station_data)
        df_station_data=pd.DataFrame(station_level_data)
        df_station_data.to_excel('PollingStationLevelResults.xlsx',index=False)
  
        
    finally:
        return df_station_data

def create_directory(directory):
    directory=directory.split('/')
    if len(directory)>=2:
        directory=directory[0]+'-'+directory[1]
    else:
         directory=directory[0]

    return directory

get_results()





















# URL="https://www.geeksforgeeks.org/find_element_by_link_text-driver-method-selenium-python/"

# def get_results_portal():
#     df_counties_data=pd.DataFrame()
#     try:
#         # driver.implicitly_wait(15) #wait 15 seconds
#         driver.get(URL)
#         time.sleep(5)
#         # rows=WebDriverWait(driver,6).until(
#         #     EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr"))
#         # )
#         counties=(driver.find_elements(by=By.XPATH,value="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[1]/a"""))
#         county_reported_figures=driver.find_elements(by=By.XPATH,value="""//*[@id="app"]/div/div/div/div/div[5]/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr/td[2]/span""")
#         actions=ActionChains(driver,)
#         county_level_data=[]
        
#         for i in  range (len(counties)):
#             print(">>>>")
#             county_data={'County':counties[i].text,
#                         'Report': county_reported_figures[i].text,}
#             county_level_data.append(county_data)

#         df_counties_data=pd.DataFrame(county_level_data)
        

#         # for r in county_reported_figures:
#         #     print("---------------")
#         #     print(r.text)

#         # for county in counties:
#         #     print("---------------")
#         #     print(county.text)
#         #     # get link by link text
#         #     county_link=driver.find_element(by=By.LINK_TEXT,value=county.text)
#         #     actions.click(county_link)
#         #     driver.back()
#         #     actions.perform()
          
#         #     print("--------county link--------")
#         #     print(county_link)
       

#         # Obtain the number of columns in table
#         # cols = len(driver.find_elements(by=By.XPATH,value="/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr[1]/td"))
        
       

#         # print(rows)
#         # print(cols)
#         # # Printing the table headers
#         # print("Locators           "+"             Description")
#         # for r in range(2, rows+1):
#         #     for p in range(1, cols+1):
#         #         # obtaining the text from each column of the table
#         #         value=driver.find_element(by=By.XPATH,value="/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
#         #         print(value,end='       ')
#         #     print()

#         # element=WebDriverWait(driver,10).until(
#         #     EC.presence_of_element_located((By.LINK_TEXT,"Python Programming"))
#         # )
#         # element.click()
#         # # going back
#         # driver.back()
#         # # a loop neeeds to be registered for number of clicks ro be used to go back
#         # driver.forward()
#     finally:
#         # driver.quit()
#         return df_counties_data

    
# def get_county_level_results():
#     pass
# def create_parent_directory():
#     pass
# def navigate():
#     pass
# def save_results_file():
#     pass

# get_results_portal()