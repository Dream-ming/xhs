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
page_num = 1355

for n in range(0, 500):
    ## main
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--window-size=1960,1080")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-software-rasterizer")
    # chrome_options.add_argument("blink-settings=imagesEnabled=false")

    wd = webdriver.Chrome(
        service=Service(r'C:\Users\Zealen-1\Desktop\小红书爬虫\chromedriver-win64_121.0.6167.85\chromedriver.exe'),
        options=chrome_options)
    wd.implicitly_wait(5)
    wd.get(target_url)
    time.sleep(3)

    handles = wd.window_handles
    currenthandle = handles[0]
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
    # 筛选美食
    ele = wd.find_element(By.XPATH,
                          '/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[7]/div')
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
    output_name = rf".\xiaohongshu_data\后台_美食\小红书美食合作笔记全{page_start}-{page_end}.csv"
    raw_data_list = []
    for j in range(0, 5):

        ele = wd.find_element(By.XPATH,
                              f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]')
        rows = ele.find_elements(By.CLASS_NAME, "content-row")
        rows_len = len(rows)
        for i in range(rows_len, 0, -1):
            # i = 11
            ele = wd.find_element(By.XPATH,
                                  f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/div[{i}]/div[2]/button/span/span')
            wd.execute_script("arguments[0].scrollIntoView(false)", ele)
            ele = wd.find_element(By.XPATH,
                                  f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[{i}]/div/div[2]/div[1]/div[1]/div/span')
            # wd.execute_script('window.scrollBy(0,-200)')
            try:
                ele.click()
            except:
                ele = wd.find_element(By.XPATH,
                                      f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/div[{i}]/div[2]/button/span/span')
                wd.execute_script("arguments[0].scrollIntoView(false)", ele)
                ele = wd.find_element(By.XPATH,
                                      f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[{i}]/div/div[2]/div[1]/div[1]/div/span')
                time.sleep(0.5)
                ele.click()
            time.sleep(3)
            print(i, 1)
            handles = wd.window_handles
            wd.switch_to.window(handles[-1])
            raw_data = []
            # 昵称
            try:
                ele = wd.find_element(By.CSS_SELECTOR, 'div.blogger-name')
            except:
                wd.refresh()
                time.sleep(3)
                ele = wd.find_element(By.CSS_SELECTOR, 'div.blogger-name')
            if ele.text == "":
                wd.refresh()
                time.sleep(3)
                ele = wd.find_element(By.CSS_SELECTOR, 'div.blogger-name')
            raw_data.append(ele.text)
            print(raw_data)
            # 小红书号
            ele = wd.find_element(By.CSS_SELECTOR, 'div.base-info-item.blogger-redid')
            raw_data.append(ele.text)
            # 粉丝点赞
            eles_data = wd.find_elements(By.CSS_SELECTOR, 'div.blogger-data__value.REDNumber')
            for e_i in eles_data:  # len(eles_data)
                raw_data.append(e_i.text)
            # 合作笔记
            ele = wd.find_element(By.XPATH,
                                  f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div/div/div/div[2]/div[2]/span[2]/div[2]/div[2]/div[1]/div/div[2]/span')
            wd.execute_script("arguments[0].scrollIntoView(false)", ele)
            time.sleep(0.2)
            try:
                ele.click()
            except:
                time.sleep(1)
                wd.refresh()
                time.sleep(3)
                ele = wd.find_element(By.XPATH,
                                      f'/html/body/div[1]/div/div/div[2]/div[1]/section/div/div/div/div/div/div[2]/div[2]/span[2]/div[2]/div[2]/div[1]/div/div[2]/span')
                wd.execute_script("arguments[0].scrollIntoView(false)", ele)
                time.sleep(0.2)
                ele.click()
            time.sleep(2)

            # 页数
            ele = wd.find_element(By.CSS_SELECTOR, 'div.d-pagination > div')
            hezuobiji = ""
            if ele.text:
                n_page = len(ele.text.split("\n"))
                for kk in range(0, n_page):
                    ele_bijis = wd.find_elements(By.CSS_SELECTOR, 'div.note-card__mask')
                    for bijis_i in ele_bijis:
                        # bijis_i = ele_bijis[0]
                        wd.execute_script("arguments[0].scrollIntoView(false)", bijis_i)
                        time.sleep(0.2)
                        bijis_i.click()
                        time.sleep(2)
                        ele = wd.find_element(By.CSS_SELECTOR, 'div.d-drawer-content')
                        hezuobiji += ele.get_attribute("innerHTML")
                        hezuobiji += ",.,.,."
                        ele = wd.find_element(By.CSS_SELECTOR,
                                              "div.d-space.d-space-horizontal.d-space-small.d-space-align-center.d-drawer-header > span > svg")
                        ele.click()
                        time.sleep(0.5)
                    if n_page == 1:  # 只有一页就不要点击下一页了
                        break
                    ele_next = wd.find_elements(By.CSS_SELECTOR, 'div.d-pagination > div > div > div > span > svg')
                    wd.execute_script("arguments[0].scrollIntoView(false)", ele_next[-1])
                    time.sleep(0.2)
                    ele_next[-1].click()
                    time.sleep(2)
            raw_data.append(hezuobiji)
            raw_data_list.append(raw_data)
            print(i, 2)
            wd.close()
            wd.switch_to.window(currenthandle)
            print(i, 3)

        ele = wd.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div[2]')
        wd.execute_script("arguments[0].scrollIntoView(false)", ele)
        time.sleep(0.2)
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
