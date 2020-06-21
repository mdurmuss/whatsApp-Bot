#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa@hummingdrone.co]

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time


PATH_TO_DRIVER = "./chromedriver"
PATH_TO_PAGE = "https://web.whatsapp.com/"


def send_message(browser, message):
    """Put the given message to the message box and send.

    Args:
        browser {selenium.driver}: selenium driver
        message {str}: message to send
    """

    # get the input box and sending the text!
    inp_xpath = '//div[@class="_3FRCZ copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
    input_box = browser.find_element_by_xpath(inp_xpath)
    time.sleep(1)
    input_box.send_keys(message + Keys.ENTER)
    time.sleep(2)

    # find the button.
    send_button = browser.find_element_by_class_name("_1U1xa")
    send_button.click()
    time.sleep(2)

    print("Message has sent.")


def read_json_file():
    """Scan the file and send back related variables.

    Returns:
        {tuple}: message to send and contact name.
    """
    with open('information.json') as json_file:
        data = json.load(json_file)

        response_text = data['response_text']
        contact = data['contact']

    return response_text, contact


def find_contact(browser, contact):
    """Click the chat search button and find the contact and open the chat page of it.

    Args:
        browser {selenium.driver}: selenium driver.
        contact {str}: contact to send message.

    Returns:
        {bool}: True if the contact exits.
    """
    # click to the new chat button.
    new_chat_button = browser.find_elements_by_class_name("PVMjB")[1]
    new_chat_button.click()
    time.sleep(1)

    # get the input box for searching given contact.
    inp_xpath = '//div[@class="_3FRCZ copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]'
    input_box = browser.find_element_by_xpath(inp_xpath)
    time.sleep(1)

    input_box.send_keys(contact)
    time.sleep(1)
    contact_button = browser.find_element_by_class_name("_2kHpK")
    try:
        contact_button.click()
    except NoSuchElementException:
        print("No contact found. Check the information file again. Process is killing.")
        return False
    print("Contact is selected.")

    return True


def main():

    # get the informations from json file.
    response_text, contact = read_json_file()

    # get the driver.
    browser = webdriver.Chrome(PATH_TO_DRIVER)
    browser.get(PATH_TO_PAGE)
    browser.maximize_window()

    # wait until the QR code is scanned.
    if input("Please read the QR Code and then press any button."):
        print("{}\nWe are in.".format("-" * 50))
    time.sleep(2)

    if not find_contact(browser=browser, contact=contact):
        return
    time.sleep(2)

    send_message(browser=browser, message=response_text)
    time.sleep(2)

    # after all close the browser.
    browser.close()


if __name__ == '__main__': main()
