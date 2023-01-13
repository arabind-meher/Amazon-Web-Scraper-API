import re
from os.path import join

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException


class AmazonProduct:
    def __init__(self) -> None:
        driver_path = join('driver', '108', 'chromedriver.exe')
        self.driver = Chrome(executable_path=driver_path)

    def get_product_details(self, url: str) -> dict:
        try:
            self.driver.get(url)
        except InvalidSessionIdException:
            return {
                'status': 'error',
                'error': 'InvalidSessionIdException',
                'msg': InvalidSessionIdException
            }
        except TimeoutException:
            return {
                'status': 'error',
                'error': 'TimeoutException',
                'msg': TimeoutException
            }

        product = dict()

        # product title
        title = self.driver.find_element(
            By.XPATH,
            '//*[@id="productTitle"]'
        ).text.strip()
        product['title'] = title

        # product price
        rupees = self.driver.find_element(
            By.XPATH,
            '//*[@id="corePrice_feature_div"]/div/span[1]/span[2]/span[2]'
        ).text.strip()
        paise = self.driver.find_element(
            By.XPATH,
            '//*[@id="corePrice_feature_div"]/div/span[1]/span[2]/span[3]'
        ).text.strip()
        current_price = float(re.sub("[^0-9]", "", rupees) + '.' + re.sub("[^0-9]", "", paise))
        product['current_price'] = current_price

        # product image url
        image_url = WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((
                By.XPATH,
                '//*[@id="landingImage"]')
            )).get_attribute("src")
        product['image_url'] = image_url

        return product

    def close_driver(self):
        self.driver.close()
