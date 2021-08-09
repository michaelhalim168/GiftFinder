import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from collections import OrderedDict

def get_item_list(url, category):
    
    path = '/Users/michaelhalim/Desktop/Development/chromedriver'
    driver = webdriver.Chrome(path)
    
    driver.get(url)
    delay = 300
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-binding')))
    
    headings = driver.find_elements_by_xpath("//h3[@class='ng-binding']")
    heading_list = [heading.text for heading in headings if heading.text != '']
    
    descriptions = driver.find_elements_by_xpath("//div[@ng-bind-html='renderHtml(product.content)']")
    desc_list = [description.text for description in descriptions if description.text != '']
    
    links = driver.find_elements_by_xpath("//a[@ng-click='listicle_click(product);']")
    link_list = [link.get_attribute('href') for link in links]
    link_list = list(OrderedDict.fromkeys(link_list))
    
    df = pd.DataFrame({'category': category, 'item':heading_list[3:], 'description':desc_list, 'links':link_list})
    return df


def get_reviews(url, header):   
    
    num = 1
    new_url = 'https://www.amazon.com' + url + "&pageNumber=" + str(num)
    
    ratings = []
    review_title = []
    review_body = []
    
    for i in range(2):
        
        r = requests.get(new_url, headers=header)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        rating = soup.find_all('i', {'data-hook': 'review-star-rating'})
        title = soup.find_all('a', {'data-hook':'review-title'})
        reviews = soup.find_all('span', {'data-hook': 'review-body'})
        
        for i in range(len(rating)):
            ratings.append(rating[i].text)
            review_title.append(title[i].text)
            review_body.append(reviews[i].text)
        
        num += 1
    
    df = pd.DataFrame({'review_rating': ratings, 'review_title': review_title, 'review_body': review_body})
    return df

def get_product_details(url, header):
    
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    product_name = soup.find_all('span', {'id': 'productTitle'})[0].text
    star_rating = soup.find_all('span', {'class': 'a-icon-alt'})[0].text
    product_desc = [desc.text for desc in soup.find('ul', {'class': 'a-unordered-list a-vertical a-spacing-mini'}).findAll('li')]
    reviews_link = soup.find_all('a', {'data-hook': 'see-all-reviews-link-foot'})[1]['href']
    
    df = get_reviews(reviews_link, header)
    df['product_name'] = product_name
    df['product_rating'] = star_rating
    df['product_desc'] = ' '.join(product_desc)
    df['review_link'] = reviews_link
    
    column_order = ['product_name', 'product_rating', 'product_desc', 'review_link', 'review_rating', 'review_title', 'review_body']
    df = df[column_order]
    
    return df