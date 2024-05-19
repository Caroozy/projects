import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


url = 'http://jenkins-app:8989'

opts = webdriver.ChromeOptions()
opts.add_argument("--headless=True")
# opts.add_argument('--window-size=800,600')
opts.add_argument("--no-sandbox")
# opts.add_argument("--disable-dev-shm-usage")
# opts.page_load_strategy = 'normal'



class TestUrl(unittest.TestCase):

    def test_reach(self):
        response = requests.head(url)
        if response.status_code != 200:
            print(f"site unreachable status: {response.status_code}")
        assert response.status_code == 200

    def test_reach_selenium(self):
        driver = webdriver.Chrome(options=opts)
        driver.implicitly_wait(4)
        driver.get(url)
        element = driver.find_element(By.ID, 'location')
        word = 'tel aviv'
        element.send_keys(word)
        element.submit()
        val = False
        try:
            element = driver.find_element(By.ID, 'loc')
            if word in element.text:
                val = True
        except Exception as exc:
            print(f"error when searching for {word}")
        driver.quit()
        assert val is True

    def test_unreachable_selenium(self):
        driver = webdriver.Chrome(options=opts)
        driver.implicitly_wait(4)
        driver.get(url)
        element = driver.find_element(By.ID, 'location')
        word = 'sadasdasdasd'
        element.send_keys(word)
        element.submit()
        val = False
        try:
            element = driver.find_element(By.ID, 'loc')
            if word in element.text:
                val = True
        except Exception as exc:
            pass
        driver.quit()
        assert val is False


if __name__ == '__main__':
    unittest.main().runTests()
