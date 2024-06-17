from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import date, timedelta

# Configure Selenium to use the remote WebDriver
class weatherPrep():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless') 
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        try:
            print("-------------------------start")
            self.driver = webdriver.Remote(
                command_executor="http://chrome:4444/wd/hub", options=self.options
            )
            print("done")
        except Exception:
            print("-------------------load driver")
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=self.options)



        #self.driver = webdriver.Remote(
        #    command_executor='http://selenium-hub:4444/wd/hub',
        #    options=self.options
        #)
        self.dateToUrl = date.today().strftime("%Y-%m-%d")
        self.city="Wrocław"
        self.url=f"https://www.wunderground.com/hourly/pl/{self.city}/date/{self.dateToUrl}"
        print(f"+++++++++++++++++++++++++++: {self.url}")

        self.driver.get(self.url)
        print(self.driver.title)
        print("----------------------------")
    def _getTemperature(self):
        df_prepT = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-temperature mat-column-temperature ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]').text
                degree=round((int(prep)-32)*5/9)
                # append new row to table
                df_prepT = df_prepT._append(pd.DataFrame({'Temp':[degree]}),ignore_index = True)
            #print(f"The temperature for tomorrow at 6 am is: {degree}")
            #print(df_prep.head(100))
        except Exception as e:
            print(f"An error occurred: {e}")

        print("--------------------------------------------")
        return df_prepT
    def _getTime(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-timeHour mat-column-timeHour ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="ng-star-inserted"]').text
                df_prep = df_prep._append(pd.DataFrame({'Time':[prep]}),ignore_index = True)
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep
    def _getWind(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-wind mat-column-wind ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]').text
                df_prep = df_prep._append(pd.DataFrame({'Wind':[prep]}),ignore_index = True)
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep
    def _getCloudCover(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-cloudCover mat-column-cloudCover ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]').text
                df_prep = df_prep._append(pd.DataFrame({'Cloud cover':[prep]}),ignore_index = True)
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep
    def _getRPrecip(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-precipitation mat-column-precipitation ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]').text
                df_prep = df_prep._append(pd.DataFrame({'Rain precip':[prep]}),ignore_index = True)
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep
    def _getRainamount(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-liquidPrecipitation mat-column-liquidPrecipitation ng-star-inserted"]')))
            for row in rows:
                prep = row.find_element(by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]').text
                df_prep = df_prep._append(pd.DataFrame({'Rain amount':[prep]}),ignore_index = True)
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep
    def createDataframe(self):
        df1=self._getTime()
        print(df1.head(3))
        df2=self._getTemperature()
        print(df2.head(3))
        df3=self._getWind()
        print(df3.head(2))
        df4=self._getCloudCover()
        print(df4.head(2))
        df5=self._getRPrecip()
        print(df5.head(2))
        df6=self._getRainamount()
        print(df6.head(2))
        return pd.concat([df1,df2,df3,df4,df5,df6], axis=1)
    
    def run(self):
        self.result = self.createDataframe()
        print("***********************")
        print(self.result.head(100))
        self.driver.quit()
        print("*******************************")

# Create an instance of the App class and run the script
#app = Weather_prep()
#app.run()