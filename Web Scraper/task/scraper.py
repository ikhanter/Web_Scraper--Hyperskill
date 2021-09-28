import string
import os
import requests
from bs4 import BeautifulSoup


def getting_souped_page(number):
    pagelink = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={number}'
    page_numbered = BeautifulSoup(requests.get(pagelink).content, 'html.parser')
    return page_numbered


def creating_folders(number):
    for i in range(number):
        os.mkdir(f'Page_{i+1}')


def parsing_articles(souped_page, chosen_genre, N):
    main_dir = os.getcwd()
    for article in souped_page.find_all('article'):
        genre = article.find('span', {'class': 'c-meta__type'}).text
        print('genre is', chosen_genre)
        if genre == chosen_genre:
            title = article.find('h3').text.strip()
            title_temp = ''
            for char in title:
                if char == ' ':
                    char = '_'
                elif char in string.punctuation:
                    char = ''
                title_temp += char
            title = title_temp
            print(title)
            internal_link = 'https://www.nature.com' + article.find('a', {'class': 'c-card__link u-link-inherit'}).get(
                'href')
            print('internal link status code is', requests.get(internal_link).status_code)
            article_page = BeautifulSoup(requests.get(internal_link).content, 'html.parser')
            article_text_raw = article_page.find('div', {'class': 'c-article-body u-clearfix'})
            article_text = ''
            for content in article_text_raw.find_all(['p', 'h2']):
                print(content)
                if content.find('div', {'class': 'recommended pull pull--left u-sans-serif'}) == None:
                    article_text += content.text
            os.chdir(os.path.join(main_dir, f'Page_{N}'))
            f = open(f'{title}.txt', 'wb')
            f.write(bytes(article_text, encoding='utf-8'))
            f.close()
        else:
            pass
    os.chdir(main_dir)


pages_number = int(input())
article_type = input()

creating_folders(pages_number)

for i in range(pages_number):
    page = getting_souped_page(i+1)
    parsing_articles(page, article_type, i+1)

