import ast
import json
import re
import requests
from config import JUSTASIANFOOD_BAKERY, MAIN_URL_JUSTASIANFOOD
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd

def get_justasianfood_bakery():
    try:
        response = requests.get(MAIN_URL_JUSTASIANFOOD + JUSTASIANFOOD_BAKERY)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # find ul tag with id "products-grid"
            ul_tag = soup.find("ul", {"id": "product-grid"})
            # find all li tags
            li_tags = ul_tag.find_all("li")
            # create empty product array
            product_array = []
            # loop through li tags
            for li_tag in li_tags:
                # create empty product object
                product = {}
                img_tag = li_tag.find("img")
                div_tag = li_tag.find("div", {"class": "card__information"})
                if img_tag:
                    img_url = "https:" + img_tag["src"]
                    product["img_url"] = img_url
                if div_tag:
                    price_tag = div_tag.find("span", {"class": "price-item price-item--regular 1"})
                    if price_tag:
                        price = price_tag.text
                        # remove currency symbol from price
                        price = price.replace("$", "")
                        # remove all space and \n from price
                        price = price.replace(" ", "").replace("\n", "")
                        product["price"] = price
                    a_tag = div_tag.find("a")
                    if a_tag:
                        title = a_tag["title"]
                        href = a_tag["href"]
                        product["title"] = title
                        product["href"] = href

                # append product object to product array
                product_array.append(product)
            
            # print product array as json
            print(json.dumps(product_array, indent=4))\
            # convert product array to Json to DataFrame
            df = pd.DataFrame(product_array)
            print(df)
            # write product array to file spreadsheet table
            df.to_excel("justasianfood_bakery.xlsx", index=False)


                

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    get_justasianfood_bakery()

if __name__ == '__main__':
    main()