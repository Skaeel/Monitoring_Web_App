import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


class GetProductInfo():

    @staticmethod
    def get_source_code(url):
        headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "\
                "(KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36"
        }
        req = requests.get(url, headers=headers)
        src = req.text

        return src

    @staticmethod
    def get_product_name(url):
        src = GetProductInfo.get_source_code(url)
        soup = BeautifulSoup(src, 'lxml')
        product_name = soup.find(class_='snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography-Primary__base__1xop0e snow-ali-kit_Typography__strong__1shggo snow-ali-kit_Typography__sizeHeadingL__1shggo HazeProductDescription_HazeProductDescription__name__5b9kv').text

        return product_name

    @staticmethod
    def get_product_price(url):
        src = GetProductInfo.get_source_code(url)
        soup = BeautifulSoup(src, 'lxml')
        product_price = soup.find(class_='snow-price_SnowPrice__mainS__jlh6el').text

        return product_price

    @staticmethod
    def get_product_rating(url):
        src = GetProductInfo.get_source_code(url)
        soup = BeautifulSoup(src, 'lxml')
        product_rating = soup.find(class_='snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography__sizeTextM__1shggo').text

        return product_rating

# url = 'https://aliexpress.ru/item/1005002843022095.html?sku_id=12000032430579006&spm=a2g2w.productlist.search_results.0.7acc4aa6eDQLRT'

# print(GetProductInfo.get_product_name(url))
# print(GetProductInfo.get_product_price(url))
# print(GetProductInfo.get_product_rating(url))
