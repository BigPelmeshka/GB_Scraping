import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from tqdm import tqdm
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def set_up():
    driver_path = "chromedriver.exe"
    return webdriver.Chrome(executable_path=driver_path)


def scroll_till_the_end(driver, xpath):
    size = 0
    while True:
        only_selected_by_search_posts = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath)
            )
        )
        if size == len(only_selected_by_search_posts):
            break
        else:
            size = len(only_selected_by_search_posts)
        driver.execute_script("arguments[0].scrollIntoView(true);",
                                     only_selected_by_search_posts[len(only_selected_by_search_posts) - 1])
        time.sleep(2)
        close_pop_up(driver)


def close_pop_up(driver):
    try:
        banner = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@class = 'UnauthActionBox UnauthActionBox--rich']")
            )
        )
        if banner is not None:
            driver.find_element_by_xpath("//a[contains(text(), 'Не сейчас')]").click()
    except Exception as e:
        print(e)


def find_all_posts_data(driver):
    all_data = []
    posts_elements = driver.find_elements_by_xpath(only_selected_posts_xpath)
    for item in tqdm(posts_elements):
        info = {}
        driver.execute_script("arguments[0].scrollIntoView(true);", item)
        link_post = item.find_element_by_xpath(".//a[@class = 'post_link']").href
        date = link_post.find_element_by_xpath("./span[@class = 'rel_date']").text
        text = item.find_element_by_xpath(".//*[@class = 'wall_post_text']").text
        link_image = text.find_element_by_xpath("./a").href
        likes = item.find_element_by_xpath(".//*[@class = 'post_info']/*[contains(@class, 'like_wrap')]//*[@title = "
                                           "'Нравится']/*[@class = 'like_button_count']").text
        share = item.find_element_by_xpath(".//*[@class = 'post_info']/*[contains(@class, 'like_wrap')]//*[@title = "
                                           "'Поделиться']/*[@class = 'like_button_count']").text
        views = item.find_element_by_xpath(".//*[@class = 'post_info']/*[contains(@class, 'like_wrap')]//*[@class = "
                                           "'like_views _views']").text
        info["link_post"] = link_post
        info["date"] = date
        info["text"] = text
        info["link_image"] = link_image
        info["likes"] = likes
        info["share"] = share
        info["views"] = views
        all_data.append(info)
    return all_data


def send_text(driver, message):
    while True:
        try:
            search_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@class = 'ui_tab_plain ui_tab_search']")
                )
            )
            search_button.click()
            break
        except Exception as e:
            print(e)

    search_input = driver.find_element_by_id("wall_search")
    search_input.send_keys(message)
    search_input.send_keys(Keys.ENTER)


url = "https://vk.com/tokyofashion"
search_text = "20 лет"
MONGO_URI = "localhost:27017"
MONGO_DB = "vk_posts"

only_selected_posts_xpath = "//div[@class = '_post post page_block post--with-likes closed_comments deep_active']"

driver = set_up()
driver.get(url)
actions = ActionChains(driver)

send_text(driver, search_text)
scroll_till_the_end(driver, only_selected_posts_xpath)

info_posts = find_all_posts_data(driver)
driver.quit()

with MongoClient(MONGO_URI) as client:
    vk_posts_db = client[MONGO_DB]
    tokio_posts_db = vk_posts_db["tokio_posts"]
    tokio_posts_db.insert_one(info_posts)
