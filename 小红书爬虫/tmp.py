from selenium import webdriver
from selenium.webdriver.common.by import By  # 导入 By 模块
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = ChromeService(executable_path="D:/tools/chromeDriver/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 打开百度首页
    driver.get("https://www.bilibili.com/")
    
    # 找到用户名和密码输入框，并填写信息
    username_input = driver.find_element(By.ID, "username")  # 这里的 ID 需要根据实际网页修改
    password_input = driver.find_element(By.ID, "password")  # 同上

    username_input.send_keys("18024752541")  # 填写你的用户名
    password_input.send_keys("xsmm20031106")  # 填写你的密码

    # 点击登录按钮
    login_button = driver.find_element(By.ID, "login-button")  # 按钮的 ID 也需要根据实际情况修改
    login_button.click()

    # 等待页面加载完成
    driver.implicitly_wait(5)

    # 查找搜索框元素
    search_box = driver.find_element(By.ID, "search-input")

    # 输入搜索内容
    search_box.send_keys("假肢")

    # 提交搜索表单
    search_box.send_keys(Keys.RETURN)

    # 等待页面加载（可以用显式等待代替）
    time.sleep(5)

    # 查找搜索结果标题元素
    titles = driver.find_elements(By.XPATH, '//h3[contains(@class, "t")]/a')
    
    # 打印每个搜索结果的标题
    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title.text}")
        print(f"链接: {title.get_attribute('href')}")

finally:
    # 关闭浏览器
    driver.quit()