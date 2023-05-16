import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import re
from bs4 import BeautifulSoup

# Create a new Chrome browser instance and navigate to website A
s = Service('/opt/homebrew/Caskroom/chromedriver/112.0.5615.49/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get("https://www.modb.pro/u/15144")

# Wait for the element associated with the tab B to become clickable
b_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/section/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div"))
)

# 切换到 tab，这里的 tab 是文章选卡
b_tab.click()
time.sleep(5)  

def scroll_to_bottom(driver, css_selector):
    # 如果数据加载不出来，调大 SCROLL_PAUSE_TIME，且 SCROLL_PAUSE_TIME 数值要比下面 WebDriverWait(driver, 60) 中的数值大
    SCROLL_PAUSE_TIME = 60

    last_loaded_count = 0
    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        print(f"Current loaded elements count: {len(elements)}")  # Debug info
        if len(elements) > last_loaded_count:
            last_loaded_count = len(elements)
            driver.execute_script("arguments[0].scrollIntoView();", elements[-1])
            time.sleep(SCROLL_PAUSE_TIME)
            # 如果数据加载不出来，调大下面的 60
            WebDriverWait(driver, 60).until(EC.visibility_of(elements[-1]))  # Add explicit wait for the last element to be visible
        else:
            break

# ... (the rest of the code remains the same)

# Scroll to the bottom, until all content is loaded
scroll_to_bottom(driver, ".b-border-item.font14.flex.between.knowledge-item.pdlr20.mt20")

# Extract the HTML source of the page
html_content = driver.page_source

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

modiv = soup.find("div", {"id": "actionH"})

read_num = 0

for span_with_views_list in modiv.find_all("span", class_="views font12"):
    # 被注释掉的这条语句主要用来调试是否抓取了你想要的 td 数据；在 macOS 下选中命令用 command + / 即可取消注释；
    # print(span_with_views_list)

    for span_with_views in span_with_views_list:
            # 这个也是用来调试的打印程序；
            # print(td_with_views)

            if span_with_views:
                # 通过标题属性抓取浏览量
                # views_title = td_with_views.find("span", {"class": "number"})["title"]

                # 使用正则表达式提取数字
                views_num = int(re.sub("[^0-9]", "", span_with_views.text))

                read_num = read_num + views_num

                # print(views_num)
            else:
                print("无法找到包含'num views'的td")

print("总阅读量是" + str(read_num))

# 关闭webdriver
driver.quit()