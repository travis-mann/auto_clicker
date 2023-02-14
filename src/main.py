#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main.py: main script for autoclicker"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


# --- glob vars ---
chrome_driver_exe = r'..\chromedriver.exe'
period = 5  # seconds

# init driver
service = Service(executable_path=chrome_driver_exe)
driver = webdriver.Chrome(service=service)

# maximize window
driver.maximize_window()


# --- func ---
def click_loop(search_method: By, search_key: str, period: int) -> None:
    """
    purpose: initiate repeated delayed loop on an object
    :param search_method: selenium By statement for element search method
    :param search_key: string to search HTML for with given search method
    :param period: period between clicks, seconds
    """
    click_failed = False
    # continue looping as long as clicks are successful
    while not click_failed:
        try:
            # find element
            element_to_click = driver.find_element(search_method, search_key)
            # initiate click
            element_to_click.click()
            # wait between clicks
            sleep(period)
        except Exception as e:
            print(f'exiting click loop due to {type(e)}: {e}')
            click_failed = True


def find_element_loop(func: callable, *args) -> None:
    """
    purpose: prompt user for an element and run a function on it
    :param func: function to run with search method & search key as 1st 2 args
    :param args: additional args for func to run on given element
    """
    # allow user to get to page
    input('Please navigate to a page and press enter to continue.')

    # prompt user for an element search string
    is_valid_element = False
    while not is_valid_element:
        given_search_key = input('XPATH for element to click: ')
        search_method = By.XPATH
        is_valid_element = validate_element(search_method, given_search_key)
        if not is_valid_element:
            print('failed to find element on page, please try again.')

    # initiate click loop on element
    func(search_method, given_search_key, *args)


def validate_element(search_method: By, search_key: str) -> bool:
    """
    purpose: validate element exists on current page
    :param search_method: selenium By statement for element search method
    :param search_key: string to search HTML for with given search method
    :return element found: bool if element is on the given page
    """
    try:
        driver.find_element(search_method, search_key)
        return True
    except Exception as e:
        print(f'failed to find element due to {type(e)}: {e}')
        return False


# --- main logic ---
if __name__ == "__main__":
    find_element_loop(click_loop, period)
