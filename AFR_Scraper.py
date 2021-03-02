from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from datetime import datetime


class Scraper:
    def __init__(self, site):
        self.site = site
        self.df = pd.DataFrame(columns=['Category', 'Title', 'Summary', 'URL', 'Date'])

    def scrape(self):
        response = urllib.request.urlopen(self.site)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        date = datetime.today().strftime('%d-%m-%Y')

        for tag in soup.find_all('div', '_28DtM'):
            for block in tag.main.find_all('section', attrs={'data-contentunit-id': True}):
                for story in block.find_all(attrs={'data-testid':'StoryTileBase'}):
                    category = story.a.text
                    title = story.h3.text
                    article_summary = story.p.text
                    article_url = 'www.afr.com' + story.find_all('a')[1]['href']
                    row = {
                        'Category' : category,
                        'Title' : title,
                        'Summary' : article_summary,
                        'URL' : article_url,
                        'Date' : date
                    }
                    self.df = self.df.append(row, ignore_index=True)
        return self.df

url = 'https://www.afr.com/'
scrape = Scraper(url).scrape()
print(scrape)




