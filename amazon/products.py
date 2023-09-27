import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException, NoSuchElementException


class AmazonProduct():
    def __init__(self) -> None:
        chrome_service = Service()

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        # chrome_options.add_argument('--no-startup-window')

        self.driver = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

    def get_product_details(self, url: str):
        try:
            self.driver.get(url)
        except InvalidSessionIdException:
            return {
                'status': 'error',
                'error': 'InvalidSessionIdException',
            }
        except TimeoutException:
            return {
                'status': 'error',
                'error': 'TimeoutException',
            }

        # create dictionary to store data
        product = dict()

        try:
            # product title
            title = self.driver.find_element(
                By.ID, 'productTitle'
            ).text.strip()
            product['title'] = title

        except NoSuchElementException:
            return {
                'status': 'error',
                'error': 'NoSuchElementException[title]',
            }

        X_PATHS = [
            '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[2]/span[2]',
            '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]',
            '//*[@id="corePrice_desktop"]/div/table/tbody/tr[2]/td[2]/span[1]/span[2]',
        ]

        price__not_found: bool = True

        for x_path in X_PATHS:
            try:
                price__not_found = False
                price = self.driver.find_element(By.XPATH, x_path).text.strip()
                product['price'] = float(re.sub('[^0-9]', '', price))
                break
            except NoSuchElementException:
                price__not_found = True
                continue

        if price__not_found:
            return {
                'status': 'error',
                'error': 'NoSuchElementException[price]',
            }

        try:
            # product image url
            image_url = WebDriverWait(self.driver, 30).until(
                expected_conditions.visibility_of_element_located((
                    By.ID, 'landingImage'))).get_attribute("src")
            product['image_url'] = image_url

        except NoSuchElementException:
            return {
                'status': 'error',
                'error': 'NoSuchElementException[image_url]',
            }

        return {
            'status': 'success',
            'data': product
        }

    def close(self):
        self.driver.close()
