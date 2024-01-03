# website_functions.py

import unittest
from selenium import webdriver
import os

class WebsiteFunctions:
    def initializeUI(self):
        # Code to initialize the user interface
        pass

    def addTextField(self):
        # Code to add a new text field
        pass

class TestWebsiteFunctions(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_initializeUI(self):
        self.driver.get("file://" + os.path.abspath("index.html"))
        initial_text_field = self.driver.find_element_by_id("initial-text-field")
        add_button = self.driver.find_element_by_id("add-button")
        self.assertIsNotNone(initial_text_field)
        self.assertIsNotNone(add_button)

    def test_addTextField(self):
        self.driver.get("file://" + os.path.abspath("index.html"))
        add_button = self.driver.find_element_by_id("add-button")
        initial_text_field = self.driver.find_element_by_id("initial-text-field")
        add_button.click()
        new_text_field = self.driver.find_element_by_class_name("added-text-field")
        self.assertIsNotNone(new_text_field)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
