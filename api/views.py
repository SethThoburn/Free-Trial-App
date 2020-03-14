from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from .models import Trial, TrialInstance

import os
import random
import re
import requests
import string
import time
import urllib


def email(request):
    if request.method == 'POST':
        email = request.POST['to']
        body = request.POST['text']

        match = re.findall(r'<p class=3D"otp">\d+</p>', body)[0]
        otp = match.split('>', 1)[1].split('<', 1)[0]

        trial = TrialInstance.objects.filter(email=email).first()
        print(email)

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--enable-file-cookies")
        capabilities = options.to_capabilities()

        driver = webdriver.Remote(command_executor=trial.executor_url, desired_capabilities=capabilities)
        driver.session_id = trial.session_id

        driver.find_element_by_css_selector('input[name="code"]').send_keys(otp)
        driver.find_element_by_css_selector('input[type="submit"').click()

        TRIAL_URL = 'https://www.amazon.com/hp/wlp/pipeline/membersignup?_encoding=UTF8&%2AVersion%2A=1&%2Aentries%2A=0'
        NAME = 'John Smith'
        CARD = '4242424242424242'
        MONTH = '12'
        YEAR = '2030'

        driver.get(TRIAL_URL)
        month = webdriver.support.ui.Select(driver.find_element_by_css_selector('select[name="ppw-expirationDate_month"]'))
        year = webdriver.support.ui.Select(driver.find_element_by_css_selector('select[name="ppw-expirationDate_year"]'))
        
        driver.find_element_by_css_selector('input[name="ppw-accountHolderName"]').send_keys(NAME)
        driver.find_element_by_css_selector('input[name="addCreditCardNumber"]').send_keys(CARD)
        month.select_by_visible_text(MONTH)
        year.select_by_visible_text(YEAR)
        driver.find_element_by_css_selector('input[name="ppw-widgetEvent:AddCreditCardEvent"]').click()

        driver.execute_script('alert("")')

        print(otp)

    return HttpResponse()

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--disable-infobars')
    driver = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH, chrome_options=chrome_options, port=9515)
    return driver

def cancel_hulu_trial(request):
    driver = get_driver()

    email = request.POST['email']
    password = request.POST['password']

    LOGIN_URL = 'https://auth.hulu.com/web/login?next=https://secure.hulu.com/account/cancel'
    # CANCEL_URL = 'https://secure.hulu.com/account/cancel'
    driver.get(LOGIN_URL)
    driver.find_element_by_id('email_id').send_keys(email)
    driver.find_element_by_id('password_id').send_keys(password)
    driver.find_element_by_css_selector('.login-button.jsx-1761454348').click()
    driver.implicitly_wait(10)
    # driver.get(CANCEL_URL)
    driver.find_element_by_css_selector('.Button--cta').click()
    driver.find_element_by_css_selector('label[for="survey-other"]').click()
    driver.find_element_by_css_selector('.Button--cta').click()
    # driver.find_element_by_xpath("//*[contains(text(), 'Cancel Subscription')]").click()

    return HttpResponse()

def amazon_trial(request):
    URL = 'https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_newcust'
    password = 'password'
    name = 'Jerry Smith'
    random_letters = ''.join(random.choice(string.ascii_letters) for i in range(8))
    # email = f'{random_letters}@parse.free-trials-app-backend.herokuapp.com'
    email = f'rr0893862+{random_letters}@gmail.com'

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--disable-infobars')
    driver = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH, chrome_options=chrome_options, port=9515)

    driver.get(URL)
    driver.find_element_by_css_selector('input[name="customerName"]').send_keys(name)
    driver.find_element_by_css_selector('input[name="email"]').send_keys(email)
    driver.find_element_by_css_selector('input[name="password"]').send_keys(password)
    driver.find_element_by_css_selector('input[name="passwordCheck"]').send_keys(password)
    driver.find_element_by_id('continue').click()

    ext = ''
    try:
        captcha = driver.find_element_by_css_selector('img[alt="captcha"]')
        ext = 'jpg'
    except NoSuchElementException:

        try:
            captcha = driver.find_element_by_css_selector('#auth-captcha-image')
            ext = 'gif'
        except NoSuchElementException:
            pass

    executor_url = driver.command_executor._url
    session_id = driver.session_id

    TrialInstance.objects.create(
        trial = Trial.objects.get(pk=1),
        email = email,
        session_id = session_id,
        executor_url = executor_url,
        password = password,
    )

    webdriver.support.ui.WebDriverWait(driver, 120).until(EC.alert_is_present())

    if ext:
        source = captcha.get_attribute('src')
        print(source)
        result = urllib.request.urlopen(source)
        name = default_storage.save(f'captcha.{ext}', result)

        return JsonResponse({
            'email': email,
            'captcha': f'127.0.0.1:8000/media/{name}',
            'captcha_type': 0 if ext == 'gif' else 1,
        })


    return JsonResponse({
        'email': email,
        'password': password,
    })

def captcha(request):
    email = request.POST['email']
    solution = request.POST['solution']
    captcha_type = request.POST['captcha_type']
    trial = TrialInstance.objects.filter(email=email).first()

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")
    capabilities = options.to_capabilities()

    driver = webdriver.Remote(command_executor=trial.executor_url, desired_capabilities=capabilities)
    driver.session_id = trial.session_id

    if captcha_type == '0':
        driver.find_element_by_css_selector('input[name="password"]').send_keys(trial.password)
        driver.find_element_by_css_selector('input[name="passwordCheck"]').send_keys(trial.password)
        driver.find_element_by_css_selector('input[name="guess"]').send_keys(solution)
        driver.find_element_by_id('continue').click()
    elif captcha_type == '1':
        driver.find_element_by_css_selector('input[name="cvf_captcha_input"]').send_keys(solution)
        driver.find_element_by_css_selector('input[name="cvf_captcha_captcha_action"]').click()

    return HttpResponse()
