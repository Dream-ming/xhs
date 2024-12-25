from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd

target_url = 'https://www.xiaohongshu.com/explore'

output_name_user = rf"./xiaohongshu_data/search/search_user.csv"
simple_biji = 1
repeate_n = 20
# search_list = ["美食制作","美食自制","减脂餐","饮品制作","西餐美式制作","食品测评","精致咖啡配件分享","减脂健身餐","美食种草"]
search_list = ["咖啡", ]
# 打开浏览器
# start "C:\Program Files\Google\Chrome\Application" chrome.exe --remote-debugging-port=6001 --user-data-dir="D:\Chrome2"
os.system(
    "start \"C:\\Program Files\\Google\\Chrome\\Application\" chrome.exe --remote-debugging-port=6001 --user-data-dir=\"D:\\Chrome2\" ")

# selenium接管浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:6001")
chrome_options.add_argument('--ignore-certificate-errors')

wd = webdriver.Chrome(
    service=Service(r'C:\Users\Zealen-1\Desktop\小红书爬虫\chromedriver-win64_121.0.6167.85\chromedriver.exe'),
    options=chrome_options)
wd.implicitly_wait(10)
wd.get(target_url)
time.sleep(3)

handles = wd.window_handles
currenthandle = handles[0]

# 手动登录
# 手动登录一次之后就记住了 不用一直手动操作
# 不断点击美食
for vv in range(119, 200):
    # vv = 0
    output_name = rf"./xiaohongshu_data/search/search_美食{vv}.csv"
    ele = wd.find_element(By.CSS_SELECTOR, "div.channel-container :nth-child(3)")
    ele.click()
    time.sleep(3)
    # 搜索内容
    # for search_data in search_list:
    # output_name = rf"./search/search_{search_data}.csv"
    # ele = wd.find_element(By.CSS_SELECTOR,'#search-input')
    # ele.send_keys(Keys.CONTROL+"a")
    # ele.send_keys(search_data,Keys.ENTER)
    # time.sleep(3)

    # 将爬过的达人昵称录入避开重复爬取
    user_csv = pd.read_csv(output_name_user, index_col=0, encoding="GB18030")
    user_name = user_csv.iloc[:, user_csv.shape[1] - 1].to_list()
    # 依次点击用户
    raw_data_list = []
    no_new_user_n = 0
    while 1:
        eles = wd.find_elements(By.CSS_SELECTOR, "span.name")  # len(eles)
        user_add = 0
        for ele in eles:
            # ele = eles[16].text
            # len(eles)
            try:
                name_i = ele.text
            except:
                print(name_i)
                break
            if name_i in user_name:
                continue
            user_name.append(name_i)
            user_add += 1
            wd.execute_script("arguments[0].scrollIntoView(false)", ele)
            wd.execute_script("window.scrollBy(0,50)")
            time.sleep(1)
            ele.click()
            time.sleep(3)
            handles = wd.window_handles
            wd.switch_to.window(handles[-1])

            # 筛选
            # ele = wd.find_element(By.CSS_SELECTOR,"#userPageContainer > div.user > div > div.info-part > div.info > div.data-info > div > div:nth-child(2) > span.count")
            # ele.text
            # 抓数据
            # 个人信息
            try:
                ele = wd.find_element(By.CSS_SELECTOR, "#userPageContainer > div.user > div > div.info-part > div.info")
            except:
                time.sleep(3)
                wd.refresh()
                time.sleep(3)
                ele = wd.find_element(By.CSS_SELECTOR, "#userPageContainer > div.user > div > div.info-part > div.info")
            raw_data = ele.text.split("\n")
            time.sleep(0.5)
            # 笔记标题
            data_content = []
            data_love = []
            data_link = []
            while 1:
                eles_data_content = wd.find_elements(By.CSS_SELECTOR, "#userPostedFeeds > section> div > div > a")
                eles_data_love = wd.find_elements(By.CSS_SELECTOR,
                                                  "#userPostedFeeds > section> div > div > div > span > span.count")
                n_add = 0
                for i in range(0, len(eles_data_content)):
                    if eles_data_content[i].text in data_content:
                        continue

                    data_content.append(eles_data_content[i].text)
                    data_link.append(eles_data_content[i].get_attribute("href"))
                    data_love.append(eles_data_love[i].text)
                    n_add += 1
                if simple_biji == 1:
                    break
                wd.execute_script("arguments[0].scrollIntoView()", eles_data_love[-1])
                time.sleep(0.5)
                if n_add == 0:
                    break
            wd.close()
            wd.switch_to.window(currenthandle)

            t_content = ""
            for i in range(0, len(data_content)):
                t_content += data_content[i] + ",.," + data_love[i] + ",.," + data_link[i] + ";.;"
            raw_data.append(t_content)

            raw_data_list.append(raw_data)

        if user_add == 0:
            no_new_user_n += 1
            wd.execute_script("window.scrollBy(0,1000)")
            time.sleep(0.5)
        else:
            no_new_user_n = 0
        if no_new_user_n > repeate_n:
            break
        # wd.execute_script("arguments[0].scrollIntoView()",eles[-1])
        # time.sleep(2)

    pd.DataFrame({"name": user_name}).to_csv(output_name_user, encoding="GB18030")
    pd.DataFrame(raw_data_list).to_csv(output_name, encoding="GB18030")

    time.sleep(0.5)

wd.close()
