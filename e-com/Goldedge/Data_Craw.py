# -*- coding:utf-8 -*-
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Def_dea import Daemon


def Get_Page():
    Browser = webdriver.PhantomJS()
    Browser.get('http://www.icbc.com.cn/ICBCDynamicSite/Charts/GoldTendencyPicture.aspx')
    Soup_page = BeautifulSoup(Browser.page_source, "lxml")
    #return Soup_page
    S_index = Soup_page.text.split().index('人民币账户黄金')
    E_index = Soup_page.text.split().index('代理实物贵金属递延行情')
    print(Soup_page.text.split()[S_index:E_index])


