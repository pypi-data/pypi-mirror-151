# -*- coding: utf-8 -*-
from selenium.webdriver.webkitgtk import webdriver

driver = webdriver.PhantomJS("./phantomjs-2.1.1/bin/phantomjs")

# 访问登录页面
driver.get("https://passport.csdn.net/account/login?ref=toolbar")
# 保存登录页面截图
driver.save_screenshot("csdn1.png")

# 获取登录 用户输入框、密码输入框
u_name = driver.find_element_by_id("username").send_keys("damumoye")
p_word = driver.find_element_by_id("password").send_keys("********")

# 模拟点击登录
login_btn = driver.find_element_by_css_selector("#fm1 .logging")
login_btn.click()
# 保存登录后的截图
driver.save_screenshot("csdn2.png")

# 保存数据
with open("csdn.html", "w") as f:
    f.write(driver.page_source.encode("utf-8"))

# 退出浏览器
driver.quit()
