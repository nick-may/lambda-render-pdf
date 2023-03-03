from asyncio.log import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tempfile import mkdtemp
from faker import Faker
import base64


# Function that setup the browser parameters and return browser object.


def lambda_handler(event, context):

    fake_user_agent = Faker()

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-first-run')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-client-side-phishing-detection')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--user-agent=' + fake_user_agent.user_agent())
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    driver.get('https://www.google.com/')
    source = driver.page_source

    params = {
        'landscape': False,
        # 'paperWidth': 8.27,
        # 'paperHeight': 11.69
    }
    data = driver.execute_cdp_cmd("Page.printToPDF", params)

    return {
        "data": data
    }
