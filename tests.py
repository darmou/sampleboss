"""
Testing to make sure we can make searches using the BOSS Api
"""

import ipdb
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SamplebossTest(LiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5000000000000000)

    def tearDown(self):
        #self.browser.quit()
        print "finished"

    def test_can_search_the_web_using_boss(self):
        # Gertrude opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/search/')

        text_input = self.browser.find_element_by_name('q')
        text_input.send_keys("test")
        search_btn = self.browser.find_element_by_id('sendbutton')
        search_btn.click()
        try:
            element = WebDriverWait(self.browser, 5000000000000000).until(
            EC.presence_of_element_located((By.ID, "resultstable")))
            assert element.tag_name == 'table'
        finally:
            self.browser.quit()



