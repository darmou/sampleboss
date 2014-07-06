"""
Testing to make sure we can make searches using the BOSS Api
"""


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class NoDbTestCase(LiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(120)


    def _post_teardown(self):
        """ Stop db at post teardown """""
        pass

    def test_can_search_the_web_using_boss(self):
        self.browser.get(self.live_server_url + '/search/')

        text_input = self.browser.find_element_by_name('q')
        text_input.send_keys("test")
        search_btn = self.browser.find_element_by_id('sendbutton')
        search_btn.click()
        try:
            #timeout at 2 minutes
            element = WebDriverWait(self.browser, 120).until(
            EC.presence_of_element_located((By.ID, "resultstable")))
            assert element.tag_name == 'table'
        finally:
            self.browser.quit()



