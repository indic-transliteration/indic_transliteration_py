import logging
import os.path

from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")

opts = options.Options()
opts.headless = True


class DVTTVedicConverter(object):
    def __init__(self):
        # We presume that you've installed chrome driver as per https://splinter.readthedocs.io/en/latest/drivers/chrome.html .
        self.browser = webdriver.Chrome(options=opts)
        self.browser.get('file://' + os.path.join(os.path.dirname(__file__), "data", 'DV-TTVedicNormal ==_ यूनिकोड परिवर्तित्र.html'))

    def convert(self, text):
        input_box = self.browser.find_element_by_id("legacy_text")
        convert_button = self.browser.find_element_by_name("converter")
        input_box.send_keys(text)
        convert_button.click()
        output_box = self.browser.find_element_by_id("unicode_text")
        return output_box.get_attribute("value")

