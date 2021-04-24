from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

class ScrapingJob():

    def hh(vacancy,page):

        url = f'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={vacancy}&page={page}'

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        vacancies_name = []
        salary = []
        links = []
        source = []

        vacancies_name.append([my_elem.text for my_elem in WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "resume-search-item__name")))])

        for i in range(len(vacancies_name[0])):
            try:
                salary.append([my_elem.text for my_elem in WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.XPATH, f"//*[@id=\"HH-React-Root\"]/div/div/div[2]/div[2]/div/div[3]/div/div[{i+1}]/div[2]/div[2]/span")))])
            except TimeoutException:
                salary.append(['Нет данных'])

        for i in range(len(vacancies_name[0])):
            for a in driver.find_elements_by_xpath(f'/html/body/div[6]/div/div[1]/div[3]/div/div/div[2]/div[2]/div/div[3]/div/div[6]/div[2]/div[1]/span/span/span/a'):
                links.append([a.get_attribute('href')])

        salary_for_df = []
        links_for_df = []
        vacancies_name_for_df = []
        site = []

        for i in range(len(salary)):
            salary_for_df.append(salary[i][0])
            links_for_df.append(links[i][0])
            vacancies_name_for_df.append(vacancies_name[0][i])
            site.append('hh.ru')

        df_hh = pd.DataFrame({'name':vacancies_name_for_df, 'salary':salary_for_df, 'link':links_for_df, 'site': site})

        #df_hh.to_csv('Вакансии c HH-RU.csv')

        return df_hh
        


    def sj(vacancy,page):
        url = f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}&geo%5Bt%5D%5B0%5D=4&page={page}'

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        v = []
        salary = []
        links = []
        source = []


        for i in range(30):
            if i == 0:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[{i+1}]/div/div/div/div/div[3]/div/div[1]/div/a'):
                    links.append([a.get_attribute('href')])
            else:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[{i+1}]/div[2]/div/div/div/div[3]/div/div[1]/div/a'):
                    links.append([a.get_attribute('href')])



        for i in range(30):
            if i == 0:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[{i+1}]/div/div/div/div/div[3]/div/div[1]/div/a'):
                    v.append([a.text])
            else:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[{i+1}]/div[2]/div/div/div/div[3]/div/div[1]/div/a'):
                    v.append([a.text])


        for i in range(30):
            if i == 0:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[{i+1}]/div/div/div/div/div[3]/div/div[1]/span'):
                    salary.append([a.text])
            else:
                for a in driver.find_elements_by_xpath(f'/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[{i+1}]/div[2]/div/div/div/div[3]/div/div[1]/span'):
                    salary.append([a.text])


        salary_for_df = []
        links_for_df = []
        vacancies_name_for_df = []
        site = []

        for i in range(len(salary)):
            salary_for_df.append(salary[i][0])
            links_for_df.append(links[i][0])
            vacancies_name_for_df.append(v[i][0])
            site.append('superjob.ru')

        df_sj = pd.DataFrame({'name':vacancies_name_for_df, 'salary':salary_for_df, 'link':links_for_df, 'site': site})

        #df_sj.to_csv('Вакансии c SUPERJOB.csv')
        return df_sj

