import os.path

from splinter.browser import Browser


class DVTTVedicConverter(object):
    def __init__(self):
        # We presume that you've installed chrome driver as per https://splinter.readthedocs.io/en/latest/drivers/chrome.html .
        self.browser = Browser('chrome', headless=True)
        self.browser.visit('file://' + os.path.join(os.path.dirname(__file__), "data", 'DV-TTVedicNormal ==_ यूनिकोड परिवर्तित्र.html'))
        
    def convert(self, text):
        input_box = self.browser.find_by_id("legacy_text")
        convert_button = self.browser.find_by_name("converter")
        input_box.fill(text)
        convert_button.click()
        output_box = self.browser.find_by_id("unicode_text")
        return output_box.value

