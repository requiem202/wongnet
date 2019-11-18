import os
import csv
import math
from bs4 import BeautifulSoup
import requests
import pandas as pd

s = requests.Session()
s.headers.update({
    'Host': 'www.wongnai.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': '__cfduid=d2f721c08e77b092eddd82bf7496cb0db1570190163; _wna_id.wn.2b35=e13093df-cfd9-4c43-9a27-32933f134685.1570190166.9.1573965754.1573965754.; _gcl_au=1.1.1268204751.1570190167; __utma=40974884.409063918.1570190168.1573959893.1573965754.10; __utmz=40974884.1573959893.9.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.2.409063918.1570190168; _uid14884=43A07DD0.10; G_ENABLED_IDPS=google; _fbp=fb.1.1570190173523.2083213867; _wna_ref.wn.2b35=%5B%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C1573965754%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; OB-USER-TOKEN=3bf218a3-7fc1-40d6-be52-96cb8afe1b1c; __cfduid=d2f721c08e77b092eddd82bf7496cb0db1570190163; ws=eyJhbGciOiJIUzUxMiJ9.eyJfaSI6IjFyYmhiZGw2NzU5aXI5ZnZjODQ2NWtvdGhmIiwiX3QiOjE1NzM5NjU3NTU0NjIsIl9lIjoxNTczOTY2OTU1NDYyLCJsIjoidGgifQ.13ceMTi_AvnACJ1kYPN6Bwy1OrE1WOSuC7Sks1QzxunI-87ADcyShZ7mIUuilsvnE_QBl6Fq6VTFCPoWWIcy6Q; _cbclose=1; _cbclose14884=1; verify=test; _gid=GA1.2.768478447.1573959893; __utmc=40974884; _wna_ses.wn.2b35=1; _ctout14884=1; __utmb=40974884.1.10.1573965754; visit_time=2998',
    'Upgrade-Insecure-Requests': '1',
    'If-None-Match': 'W/"ae-FHQSRL2wimzAI11zncvNrXfIWpM"',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers'
})


def scrape_leaderboard():
    # there are robot prevention in this link
    url = 'https://www.wongnai.com/cooking/leaderboards'
    resp = requests.get(url)
    doc = BeautifulSoup(resp.text, 'html.parser')
    links = doc.find_all('a', class_='sc-1cl38do-1')
    names = doc.find_all('p', class_='sc-1cl38do-4')
    entries = doc.find_all('div', class_='sc-1xeooeb-0')
    result = []
    for name, link, entry in zip(names, links, entries):
        result.append((name.text, link['href'].split('/')[-1], entry.text))

    # with open(f'data/leaderboard.csv', 'w', encoding='utf-8') as f:
    #     writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    #     for row in result:
    #         writer.writerow(row)
    return result


# def find_out_total_page(user):
#     url = f'https://www.wongnai.com/_api/v1.6/cooking/users/{user}/recipes?_v=5.096&locale=th&page.number={page_no}&page.size=10&state=published'
#     # https://www.wongnai.com/_api/v1.6/cooking/users/e36b3db03b584af389a7ebb612a91a3e/recipes?_v=5.096&locale=th&page.number=3&page.size=10&state=published
#     resp = s.get(url)
#     data = resp.json()
#     return data['totalNumberOfPages'], data['totalNumberOfEntities']


def scrape_recipe_page(user, page_no):
    url = f'https://www.wongnai.com/_api/v1.6/cooking/users/{user}/recipes?_v=5.096&locale=th&page.number={page_no}&page.size=10&state=published'
    # https://www.wongnai.com/_api/v1.6/cooking/users/e36b3db03b584af389a7ebb612a91a3e/recipes?_v=5.096&locale=th&page.number=3&page.size=10&state=published
    resp = s.get(url)
    if not os.path.exists('data/' + user):
        os.mkdir('data/' + user)
    print(resp.json())
    with open(f'data/{user}/{page_no}.json', 'w', encoding='utf-8') as f:
        f.write(resp.text)


if __name__ == '__main__':

    if not os.path.exists('data'):
        os.mkdir('data')

    # new scrape
    # leaderboard = scrape_leaderboard()
    #
    # df = pd.DataFrame(leaderboard)
    # df.to_csv('data/leaderboard.csv')

    df = pd.read_csv('data/leaderboard.csv', index_col=0) #, names=['name', 'link', 'entries'])

    for _, row in df.iterrows():
        pages = math.ceil(row['entries'] / 10)
        for i in range(1, pages):
            scrape_recipe_page(row['link'], i)
        # scrape_recipe_page('e36b3db03b584af389a7ebb612a91a3e', 1)

    s.close()
