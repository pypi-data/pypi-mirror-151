# -*- coding: utf-8 -*-
from selenium.webdriver.edge.webdriver import WebDriver

c = WebDriver(executable_path="/Users/liuzhuo/code/Python3/crawl_chrome/crawler_chrome/chromedriver")

c.get("www.baidu.com")
