from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

## input

target_url = 'https://pgy.xiaohongshu.com/'

account = "1179735040@qq.com"
password = "JinRun0016"
page_num = 441

for n in range(0, 500):
    ## main
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-software-rasterizer")
    # chrome_options.add_argument("blink-settings=imagesEnabled=false")

    wd = webdriver.Chrome(options=chrome_options)
    wd.implicitly_wait(3)
    wd.get(target_url)
    time.sleep(5)

    handles = wd.window_handles
    currenthandle = handles[0]
    # cookoes = wd.get_cookies()
    # wd.delete_all_cookies()
    # 登录
    ele = wd.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[2]/button[1]')
    ele.click()
    time.sleep(3)
    ele = wd.find_element(By.XPATH, "//*[contains(text(),'账号登录')]")
    ele.click()
    time.sleep(3)

    ele = wd.find_element(By.CSS_SELECTOR,
                          "body > div.d-modal-mask > div > div.d-modal-content > div.login-box > div > div > div.css-6oq7i4 > div:nth-child(2) > div:nth-child(1) > input")
    ele.send_keys(account)
    time.sleep(0.5)
    ele = wd.find_element(By.CSS_SELECTOR,
                          "body > div.d-modal-mask > div > div.d-modal-content > div.login-box > div > div > div.css-6oq7i4 > div:nth-child(2) > div:nth-child(2) > input")
    ele.send_keys(password)
    time.sleep(0.5)
    ele = wd.find_element(By.CSS_SELECTOR,
                          'body > div.d-modal-mask > div > div.d-modal-content > div.login-box > div > div > button > span')
    ele.click()
    time.sleep(3)
    # 寻找博主
    ele = wd.find_element(By.XPATH,
                          '/html/body/div[1]/div/div/div[1]/header/div[1]/div/div[1]/div[3]/div[1]/div[2]/div/div')
    ele.click()
    time.sleep(3)
    # # 筛选美食
    # ele = wd.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[7]/div')
    # ele.click()
    # time.sleep(3)
    # 筛选运动健身
    ele = wd.find_element(By.XPATH,
                          '/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[10]/div')
    ele.click()
    time.sleep(3)
    # 粉丝倒序
    ele = wd.find_element(By.XPATH,
                          '/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div/span/img')
    ele.click()
    time.sleep(3)

    # 手动到指定页面
    ele = wd.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div[1]/a[2]')
    wd.execute_script("arguments[0].scrollIntoView(false)", ele)
    ele = wd.find_element(By.XPATH,
                          f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/div/div[2]/div[2]/input')
    ele.send_keys(Keys.CONTROL, "a")
    ele.send_keys(page_num, Keys.ENTER)
    time.sleep(3)
    ele = wd.find_element(By.XPATH,
                          f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/div/div[2]/div[1]')
    ele_selecteds = ele.find_elements(By.CSS_SELECTOR, ".--selected")
    page_end = ""
    for val in ele_selecteds:
        page_end += val.text
    page_start = int(page_end) - 4
    output_name = f"小红书运动健身{page_start}-{page_end}.csv"
    raw_data_list = []
    for j in range(0, 5):

        ele = wd.find_element(By.XPATH,
                              f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]')
        rows = ele.find_elements(By.CLASS_NAME, "content-row")
        rows_len = len(rows)
        for i in range(rows_len, 0, -1):
            # i = 19
            ele = wd.find_element(By.XPATH,
                                  f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/div[{i}]/div[2]/button/span/span')
            wd.execute_script("arguments[0].scrollIntoView(false)", ele)
            ele = wd.find_element(By.XPATH,
                                  f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[{i}]/div/div[2]/div[1]/div[1]/div/span')
            # wd.execute_script('window.scrollBy(0,-200)')
            ele.click()
            time.sleep(3)
            print(i, 1)
            handles = wd.window_handles
            wd.switch_to.window(handles[-1])

            ele = wd.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div')
            raw_data = ele.text.split("\n")
            raw_data_list.append(raw_data)
            print(i, 2)
            wd.close()
            wd.switch_to.window(currenthandle)
            print(i, 3)

        ele = wd.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div[2]')
        wd.execute_script("arguments[0].scrollIntoView(false)", ele)
        time.sleep(0.1)
        ele = wd.find_element(By.XPATH,
                              f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/div/div[2]/div[1]/span[1]')
        ele.click()
        time.sleep(3)

    pd.DataFrame(raw_data_list).to_csv(output_name, encoding="GB18030")
    # wd.delete_all_cookies()
    # wd.refresh()
    wd.quit()
    page_num = page_start - 1
    time.sleep(3)
