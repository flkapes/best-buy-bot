import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from random import randint
from time import sleep
from discord import Webhook, RequestsWebhookAdapter
import json

# Loads config file
json = json.load(open('config.json', 'r'))

webhook = Webhook.from_url(
    json['discord_webook'],
    adapter=RequestsWebhookAdapter())  # Creates webhook using discord url
driver = webdriver.Firefox(
    executable_path=json['executable_path'])  # Creates WebDriver instance

url = "https://www.bestbuy.com"
timeout = 3  # Timeout for element loaded checks
purchased = open('purchased.txt', 'r').read()


def navigate_to_bb():
    """
    * Navigates to the URL supplied, by default this is BestBuy.com
    """
    driver.get(url)
    print("navigated to bestbuy")


def navigate_to_product():
    """
    * Navigates to the URL supplied + the product URL
    """
    driver.get(url + json['url'])


def check_if_in_stock():
    """
    This function tries to find the Add To Cart button, if it does not find it, it means it is out
    of stock currently and it throws a NoSuchElementException.
    :return: Returns True for in stock and False for not in stock
    :rtype: None Type
    """
    try:
        not_sold_out = driver.find_element_by_css_selector(
            'button.btn-primary:nth-child(1)')
    except NoSuchElementException:
        return False
    return True


def add_to_cart():
    """
    This function finds the Add to Cart button, and then adds the product to cart
    :rtype: object
    """
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button.btn-primary:nth-child(1)'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    add_to_cart_button = driver.find_element_by_css_selector(
        "button.btn-primary:nth-child(1)")
    add_to_cart_button.click()
    print("added to cart")


def navigate_to_cart():
    """
    This function navigates to the BestBuy cart page
    """
    driver.get(url + "/cart")
    print("navigated to cart")
    return driver.title


def change_zip_code_and_select_shipping():
    """
    This function first selects the ZipCode element on the cart page, then types the correct
    zip code for shipping, and then clicks update location.
    :rtype: object

    """
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.change-zipcode-link'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    zip_code_click = driver.find_element_by_css_selector(
        ".change-zipcode-link")
    zip_code_click.send_keys(Keys.ENTER)
    print("clicked on zip code")

    zip_code_change = driver.find_element_by_css_selector(
        "#location")
    zip_code_change.send_keys(json['zip_code'])

    update = driver.find_element_by_css_selector(
        '#item-availability-links > button:nth-child(3)')
    update.click()
    print("changed zip code")


def click_checkout_key():
    """
    This function clicks the checkout button on the BestBuy cart page
    :rtype: object

    """
    checkout_button = driver.find_element_by_css_selector(
        ".btn-lg")
    checkout_button.click()
    print("checkout started")


def select_guest_checkout():
    """
    This function selects the Checkout as Guest option on the page following the BestBuy cart
    :rtype: object

    """
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.cia-guest-content__continue'))
        WebDriverWait(driver, 9).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    guest = driver.find_element_by_css_selector('.cia-guest-content__continue')
    guest.click()


def sign_in_and_click_button():
    """
    This function types the supplied email and password and then clicks the Sign In button.
    :rtype: object
    """
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '.cia-form__controls__submit'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    email = driver.find_element_by_id("fld-e")
    email.send_keys(json['email'])
    print("email typed")

    password = driver.find_element_by_id("fld-p1")
    password.send_keys(json['password'])
    print("password typed")

    button = driver.find_element_by_css_selector(
        '.cia-form__controls__submit')
    button.click()
    print("signed in")


def check_if_verify():
    """
    This function checks if the account has been flagged for manual user verification
    :rtype: object
    """
    try:
        verify = driver.find_element_by_css_selector(
            'h1.cia-section-title').text
        if "Verify Your Account" in verify:
            return False
        else:
            return True
    except NoSuchElementException:
        return False
    # return True


def check_if_shipping_info_needed():
    """
    This function checks to see if the bot needs to input the shipping information if the user has been
    signed in using the previous functions

    :rtype: object
    """
    try:
        element_present = EC.presence_of_element_located(
            (By.ID, 'consolidatedAddresses.ui_address_2.firstName'))
        WebDriverWait(driver, 3).until(element_present)
    except BaseException:
        return False
    return True


def input_shipping_information():
    """
    This function inputs the shipping information that the user provides if they have been logged in with
    previous functions
    :rtype: object
    """
    try:
        element_present = EC.presence_of_element_located(
            (By.ID, 'consolidatedAddresses.ui_address_2.firstName'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    fname = driver.find_element_by_id(
        "consolidatedAddresses.ui_address_2.firstName")
    fname.send_keys(json['first_name'])
    print("fname typed")

    lname = driver.find_element_by_id(
        "consolidatedAddresses.ui_address_2.lastName")
    lname.send_keys(json["last_name"])
    print("lname typed")

    suggestions = driver.find_element_by_css_selector(".autocomplete__toggle")
    if "Hide Suggestions" in suggestions.text:
        suggestions.click()
        print("suggestions removed")

    address = driver.find_element_by_id(
        "consolidatedAddresses.ui_address_2.street")
    address.send_keys(json['address'])
    print("street address typed")

    city = driver.find_element_by_id("consolidatedAddresses.ui_address_2.city")
    city.send_keys(json['city'])
    print("city typed")

    select = Select(driver.find_element_by_id(
        'consolidatedAddresses.ui_address_2.state'))
    select.select_by_visible_text(json['state'])
    print("state selected")

    zip_code = driver.find_element_by_id(
        'consolidatedAddresses.ui_address_2.zipcode')
    zip_code.send_keys(json['zip_code'])
    print("zip code address section typed")


def input_shipping_info_guest():
    """
    This function inputs the shipping information that the user provides if they have selected to checkout
    as a guest
    :rtype: object
    """
    fname = driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[1]/label[1]/div[1]/input[1]")
    for i in range(len(json['first_name'])):
        fname.send_keys(json['first_name'][i])
    print(json['first_name'] + " typed")

    lname = driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[2]/label[1]/div[1]/input[1]")
    for i in range(len(json['last_name'])):
        lname.send_keys(json["last_name"][i])
    print("lname typed")

    suggestions = driver.find_element_by_css_selector(".autocomplete__toggle")
    if "Hide Suggestions" in suggestions.text:
        suggestions.click()
        print("suggestions removed")

    address = driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[3]/label[1]/div[2]/div[1]/div[1]/input[1]")
    for i in range(len(json['address'])):
        address.send_keys(json['address'][i])
    print("street address typed")

    city = driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[5]/div[1]/div[1]/label[1]/div[1]/input[1]")
    for i in range(len(json['city'])):
        city.send_keys(json['city'][i])
    print("city typed")

    select = Select(driver.find_element_by_xpath(
        '/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[5]/div[1]/div[2]/label[1]/div[1]/div[1]/select[1]'))
    select.select_by_visible_text(json['state'])
    print("state selected")

    zip_code = driver.find_element_by_xpath(
        '/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[2]/form[1]/section[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[2]/div[1]/section[1]/section[1]/div[6]/div[1]/div[1]/label[1]/div[1]/input[1]')
    for i in range(len(json['zip_code'])):
        zip_code.send_keys(json['zip_code'][i])
    print("zip code address section typed")


def input_phone_and_email():
    """
    This function inputs the phone number and email that the user has provided if they are checking out
    as a guest
    :rtype: object
    """
    email = driver.find_element_by_id('user.emailAddress')
    email.send_keys(json['email'])
    phone = driver.find_element_by_id('user.phone')
    phone.send_keys(json['phone'])


def check_if_payment_info_on_page():
    """
    This function checks if the bot must enter payment information on the current page
    :rtype: object
    """
    try:
        cvv = driver.find_element_by_id('credit-card-cvv')
    except NoSuchElementException:
        return False
    return True


def click_continue_to_payment_info():
    """
    This function clicks the continue to payment information if the previous function returns False
    :rtype: object
    """
    button = driver.find_element_by_css_selector(
        '.btn-lg')
    button.click()


def input_payment_info():
    """
    This function inputs the CVV if the user has been logged in during a previous function and has a card saved
    :rtype: object
    """
    cvv = driver.find_element_by_id('credit-card-cvv')
    cvv.send_keys(json['cvv'])
    print("CVV added")


def input_payment_info_guest():
    """
    This function inputs the payment information of the user if they have selected Guest checkout
    :rtype: object
    """
    try:
        element_present = EC.presence_of_element_located(
            (By.ID, 'optimized-cc-card-number'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    cc_number = driver.find_element_by_id(
        'optimized-cc-card-number')
    cc_number.send_keys(json['cc_number'])

    select = Select(driver.find_element_by_name(
        'expiration-month'))
    select.select_by_visible_text(json['month'])
    print("month selected")

    select = Select(driver.find_element_by_name(
        'expiration-year'))
    select.select_by_visible_text(json['year'])
    print("year selected")

    cvv = driver.find_element_by_css_selector('#credit-card-cvv')
    cvv.send_keys(json['cvv'])
    print("CVV typed")


def place_order():
    """
    This function places the order by clicking the final button
    :rtype: object
    """
    button = driver.find_element_by_css_selector(
        '.btn-lg')
    button.click()


def main(guest_or_sign_in):
    time_start = 0
    time_end = 0
    if purchased.strip() == "0":
        in_stock = 0
        while in_stock == 0:
            navigate_to_product()
            driver.implicitly_wait(0.3)
            y = check_if_in_stock()
            if not y:
                in_stock = 0
                randinteger = randint(1, 5)
                print(
                    "Sleeping for " +
                    str(randinteger) +
                    " seconds due to product not being in stock")
                sleep(randinteger)
            else:
                #print("Stock found - running script")
                #webhook.send("@everyone Stock Found")
                #webhook.send(url + json['url'])
                time_start = time.time()
                add_to_cart()
                in_stock = 1
        navigate_to_cart()
        change_zip_code_and_select_shipping()
        click_checkout_key()
        if guest_or_sign_in == "sign-in":
            sign_in_and_click_button()
            if not check_if_verify():
                quit(0)
            if check_if_shipping_info_needed() is True:
                input_shipping_information()
                if check_if_payment_info_on_page() is False:
                    click_continue_to_payment_info()
                    input_payment_info()
                    # place_order()
                    time_end = time.time()
                    time_diff = time_end - time_start
                    webhook.send(
                        "@everyone Purchased, Time elapsed: " +
                        str(time_diff) +
                        " Seconds")
                    json2 = open('purchased.txt', 'w')
                    json2.write('1')
                    json2.close()
                else:
                    input_payment_info()
                    # place_order
                    time_end = time.time()
                    time_diff = time_end - time_start
                    webhook.send(
                        "@everyone Purchased, Time elapsed: " +
                        str(time_diff) +
                        " Seconds")
                    json2 = open('purchased.txt', 'w')
                    json2.write('1')
                    json2.close()
            else:
                if check_if_payment_info_on_page() is False:
                    click_continue_to_payment_info()
                    input_payment_info()
                    # place_order()
                    time_end = time.time()
                    time_diff = time_end - time_start
                    webhook.send(
                        "@everyone Purchased, Time elapsed: " +
                        str(time_diff) +
                        " Seconds")
                    json2 = open('purchased.txt', 'w')
                    json2.write('1')
                    json2.close()
                else:
                    input_payment_info()
                    # place_order
                    time_end = time.time()
                    time_diff = time_end - time_start
                    webhook.send(
                        "@everyone Purchased, Time elapsed: " +
                        str(time_diff) +
                        " Seconds")
                    json2 = open('purchased.txt', 'w')
                    json2.write('1')
                    json2.close()
        elif guest_or_sign_in == "guest":
            select_guest_checkout()
            # driver.refresh()
            input_shipping_info_guest()
            input_phone_and_email()
            click_continue_to_payment_info()
            input_payment_info_guest()
            # place_order()
            time_end = time.time()
            time_diff = time_end - time_start
            webhook.send(
                "@everyone Purchased, Time elapsed: " +
                str(time_diff) +
                " Seconds")
            json2 = open('purchased.txt', 'w')
            json2.write('1')
            json2.close()
    else:
        webhook.send(
            "@everyone Not purchased as item has already been bought. "
            "To reset this please open purchased.txt and replace the 0 with a 1")
        quit(0)


main(guest_or_sign_in=json['bot_usage_case'])
