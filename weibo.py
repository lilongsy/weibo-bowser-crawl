# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from db import WeiboContent, WeiboUser, engine, session_scope, Base
from sqlalchemy.orm import sessionmaker
import time
import datetime


class Weibo(object):
    def __init__(self):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        # option.add_argument('--disable-dev-shm-usage')
        # D:/Python/test3/chromedriver.exe
        # C:/spider/chromedriver.exe
        # /root/chromedriver
        self.driver = webdriver.Chrome(executable_path="/root/chromedriver",
                                       chrome_options=option)

    def index(self, i, url):
        self.driver.get(url)
        print('开始抓取：%s' % url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card-wrap"]')))
        xpath = '//div[@class="weibo-text"]'
        elements_text = self.driver.find_elements_by_xpath(xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", elements_text[i])
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, -400)")
        self.driver.implicitly_wait(5)
        print('点击第%s条微博' % (i+1))
        ActionChains(self.driver).move_to_element_with_offset(elements_text[i], 120, 0).click().perform()
        time.sleep(5)
        current_url = self.driver.current_url
        print('用户详情页地址： %s' % current_url)
        if "https://m.weibo.cn/status" in current_url:
            weibo_text = self.driver.find_element_by_xpath('//article[@class="weibo-main"]//div[@class="weibo-text"]').text
            print('内容:%s' % weibo_text)
            return {'url': current_url, 'txt': weibo_text}
        else:
            return False

    def main(self):
        url = 'https://m.weibo.cn/u/2937210565'
        Base.metadata.create_all(engine)
        with session_scope(sessionmaker(bind=engine)) as s:
            records = s.query(WeiboUser).all()
            for record in records:
                for i in range(0, 5):
                    content = self.index(i, record.user_url)
                    if content and s.query(WeiboContent).filter_by(url=content['url']).one_or_none() is None:
                        s.add(WeiboContent(
                            cid1=0,
                            username=record.username,
                            url=content['url'],
                            content=content['txt'],
                            created_at=datetime.datetime.now(),
                            publish_at=datetime.datetime.now(),
                            isPublish=1
                        ))
                        s.commit()
        # self.driver.get_screenshot_as_file('/root/spider/1.png')
        self.driver.close()


# if __name__ == '__main__':
Weibo().main()
