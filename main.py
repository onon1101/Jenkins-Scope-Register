import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

ALL_USERS = []
jenkins_account = ""
jenkins_password = ""

# 指定 Edge WebDriver 的路徑
edge_driver_path = "./msedgedriver.exe"
service = Service(edge_driver_path)

# 初始化 Edge WebDriver
driver = webdriver.Edge(service=service)

# 打開 Twitter 網站
driver.get("https://jenkins.is1ab.com/login")

# 等待頁面加載
time.sleep(1)

email_input = driver.find_element(
    By.NAME,
    "j_username",
)
email_input.send_keys(jenkins_account)

password_input = driver.find_element(
    By.NAME,
    "j_password",
)
password_input.send_keys(jenkins_password)

sign_in_button = driver.find_element(
    By.XPATH,
    '//button[@type="submit" and @name="Submit" and contains(@class, "jenkins-button--primary")]',
)
sign_in_button.click()

# 等待頁面加載
time.sleep(1)

name_link = driver.find_element(
    By.XPATH, '//a[@class="sortheader" and contains(text(), "Name")]'
)
name_link.click()
name_link.click()

# 獲取所有 tr 元素
tr_elements = driver.find_elements(By.XPATH, "//tr")

for tr in tr_elements:
    ALL_USERS.append(tr.text.split("\n")[0])


success_user = []
for user in ALL_USERS:

    # user = ALL_USERS[21]
    print(user)
    if user[:3] == "OOP":
        # print(user[:-3])
        driver.get("https://jenkins.is1ab.com/job/" + user + "/")

        # 獲取特定 a 元素的文本
        tr_elements = driver.find_elements(
            By.XPATH,
            '//tr[contains(@class, "build-row")]',
        )

        result = []
        for idx, tr in enumerate(tr_elements):

            build_time = tr.find_elements(
                By.XPATH, '//a[@class="model-link inside build-link"]'
            )
            build_status = tr.find_elements(
                By.XPATH,
                '//div[@class="build-icon"]/a[@class="build-status-link"]',
            )

            result.append(
                {
                    "time": build_time[idx].text,
                    "status": build_status[idx].get_attribute("title"),
                }
            )

        for item in result:
            split_time = re.split("[\s\,]", item["time"])
            month = split_time[0]
            date = split_time[1]
            # print(split_time)
            if (
                (month == "Oct" and 21 <= int(date) <= 31)
                or (month == "Nov" and int(date) == 1)
            ) and item["status"] == "Success > Console Output":
                success_user.append({"user_info": user, "build_info": item})
                break

        time.sleep(0.8)

for user in success_user:
    print(f"\tUser: {user['user_info']}")
    print(f"\tBuild: {user['build_info']}")
# print(success_user)
# # 關閉瀏覽器
# driver.quit()

temp = ""
for user_search in success_user:

    if temp == user_search["user_info"][:-3]:
        continue
    for user in success_user:
        if user_search["user_info"] == user["user_info"]:
            continue
        if user_search["user_info"][:-3] == user["user_info"][:-3]:
            print(f"Success user: {user_search['user_info']}")
        temp = user_search["user_info"][:-3]


try:
    while True:
        pass
except KeyboardInterrupt:
    driver.quit()
