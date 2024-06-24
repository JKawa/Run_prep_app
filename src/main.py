from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd


class weatherPrep:
    def __init__(self, day, city):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        try:
            self.driver = webdriver.Remote(
                command_executor="http://chrome:4444/wd/hub", options=self.options
            )
        except Exception:
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=self.options)

        # self.driver = webdriver.Remote(
        #    command_executor='http://selenium-hub:4444/wd/hub',
        #    options=self.options
        # )
        # self.date_to_url = date.today().strftime("%Y-%m-%d")
        self.date_to_url = day
        self.city = city
        self.url = f"https://www.wunderground.com/hourly/pl/{self.city}/date/{self.date_to_url}"
        self.driver.get(self.url)
        print(self.driver.title)

    def _get_temperature(self):
        df_prepT = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-temperature mat-column-temperature ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]'
                ).text
                degree = round((int(prep) - 32) * 5 / 9)
                # append new row to table
                df_prepT = df_prepT._append(
                    pd.DataFrame({"Temp": [degree]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prepT

    def _get_time(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-timeHour mat-column-timeHour ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="ng-star-inserted"]'
                ).text
                df_prep = df_prep._append(
                    pd.DataFrame({"Time": [prep]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep

    def _get_wind(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-wind mat-column-wind ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]'
                ).text
                df_prep = df_prep._append(
                    pd.DataFrame({"Wind": [prep]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep

    def _get_cloudCover(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-cloudCover mat-column-cloudCover ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]'
                ).text
                df_prep = df_prep._append(
                    pd.DataFrame({"Cloud cover": [prep]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep

    def _get_rprecip(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-precipitation mat-column-precipitation ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]'
                ).text
                df_prep = df_prep._append(
                    pd.DataFrame({"Rain precip": [prep]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep

    def _get_rainamount(self):
        df_prep = pd.DataFrame()
        try:
            rows = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        '//td[@class="mat-cell cdk-cell cdk-column-liquidPrecipitation mat-column-liquidPrecipitation ng-star-inserted"]',
                    )
                )
            )
            for row in rows:
                prep = row.find_element(
                    by=By.XPATH, value='.//span[@class="wu-value wu-value-to"]'
                ).text
                df_prep = df_prep._append(
                    pd.DataFrame({"Rain amount": [prep]}), ignore_index=True
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        return df_prep

    def create_dataframe(self):
        df1 = self._get_time()
        df2 = self._get_temperature()
        df3 = self._get_wind()
        df4 = self._get_cloudCover()
        df5 = self._get_rprecip()
        df6 = self._get_rainamount()
        return pd.concat([df1, df2, df3, df4, df5, df6], axis=1)

    def run(self):
        self.result = self.create_dataframe()
        self.result.drop(index=self.result.index[0], axis=0, inplace=True)
        self.driver.quit()
