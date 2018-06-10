from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import unittest


class TestWebApp(unittest.TestCase):

    def checkSortedHighest(sortedHighest):
        file_result_sort_highest = open('sort_highest.txt', 'r+')
        data = file_result_sort_highest.readlines()
        file_result_sort_highest.close()
        if len(data) != len(sortedHighest):
            return True
        for i in range(0, len(sortedHighest)):
            if data[i].split(',')[0] != sortedHighest[i].text:
                return True
        return False

    '''def checkSortedLowest(self):
        file_result_sort_lowest = open('sort_lowest.txt', 'r+')
        data = file_result_sort_lowest.readlines()
        file_result_sort_lowest.close()
        if len(data) != len(self.products_sort_lowest):
            return True
        for i in range(0, len(self.products_sort_lowest)):
            if data[i].split(',')[0] != self.products_sort_lowest[i].text:
                return True
        return False'''

    def setUp(self):
        # create a new Firefox session
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        self.driver.get('http://automationpractice.com/index.php')


        search_field = self.driver.find_element_by_name('search_query')
        search_field.clear()

        search_field.send_keys('dress')
        search_field.submit()

        # find elements with dress key
        element = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[7]'))

        products = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[*]/div/div[2]/h5/*')

        file_result_search = open('search_result.txt', 'w')

        for product in products:
            file_result_search.write("%s\n" % product.text)
        file_result_search.close()

        #products sorted by lowest price

        sortPriceASC = Select(self.driver.find_element_by_id('selectProductSort'))
        sortPriceASC.select_by_visible_text('Price: Lowest first')

        print('Products sorted by price (lower first): ')

        self.element = WebDriverWait(self.driver, 8).until(
            lambda x: x.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[7]'))

        self.products_sort_lowest = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[*]/div/div[2]/h5/*')
        self.products_prices_lowest = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[*]/div/div[2]/div/span[@class="price product-price"]')

        for product in self.products_sort_lowest:
            print(product.text)

        sortPriceDSC = Select(self.driver.find_element_by_id('selectProductSort'))
        sortPriceDSC.select_by_visible_text('Price: Highest first')

        self.element = WebDriverWait(self.driver, 8).until(
            lambda x: x.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[7]'))
        print('Products sorted by price (higher first): ')

        self.products_sort_highest = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[*]/div/div[2]/h5/*')
        self.products_prices_highest = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/ul/li[*]/div/div[2]/div/span[@class="price product-price"]')

    '''def test_detectChangesInSortedLowest(self):
        self.assertFalse(TestWebApp.checkSortedLowest(self.products_sort_lowest))'''

    def test_detectChangesInSortedHighest(self):
        self.assertFalse(TestWebApp.checkSortedHighest(self.products_sort_highest))


    def driverClose(self):
        self.driver.quit()

if __name__ == '__main__':
        unittest.main()