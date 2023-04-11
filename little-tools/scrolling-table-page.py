# 🙋 需要安装 BeautifulSoup、selenium 和 chromedriver；

import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 使用无头模式来避免实际打开浏览器
options = webdriver.ChromeOptions()
options.add_argument('headless')

# 初始化webdriver，确保您的chromedriver.exe放置在适当的路径（注意路径）
driver = webdriver.Chrome(executable_path='/opt/homebrew/Caskroom/chromedriver/112.0.5615.49/chromedriver', options=options)

# 访问网页，请替换成自己的 url
url = 'https://discuss.nebula-graph.com.cn/c/blog/8'
driver.get(url)

# 定义一个函数，模拟滚动到页面底部
def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 滚动到底部，直到所有内容加载完成
scroll_to_bottom(driver)

# 提取页面HTML源码
html_content = driver.page_source

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 寻找tbody
tbody = soup.find("tbody", {"class": "topic-list-body"})

def has_num_views(css_class):
    return css_class and 'num views' in css_class

for tr in tbody.find_all("tr"):
    td_with_views_list = tr.find_all("td", class_=has_num_views)  # 提取包含 "num views" 的 td
    # 被注释掉的这条语句主要用来调试是否抓取了你想要的 td 数据；在 macOS 下选中命令用 command + / 即可取消注释；
    # print(td_with_views_list)

    for td_with_views in td_with_views_list:
            # 这个也是用来调试的打印程序；
            # print(td_with_views)

            if td_with_views:
                # 通过标题属性抓取浏览量
                views_title = td_with_views.find("span", {"class": "number"})["title"]

                # 使用正则表达式提取数字
                views_num = int(re.sub("[^0-9]", "", views_title))

                print(views_num)
            else:
                print("无法找到包含'num views'的td")

# 关闭webdriver
driver.quit()