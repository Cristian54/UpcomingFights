from webscrapper import WebScraper
import time

rankings = WebScraper.getRankings()
rankingss = [rankings[0], rankings[1], rankings[7]]
distinctNames = WebScraper.getDistinctNames(rankingss)
if 'Alexei Papin' in distinctNames: distinctNames.remove('Alexei Papin')
if 'Manny Pacquiao' in distinctNames: distinctNames.remove('Manny Pacquiao')
if 'Mateusz Masternak' in distinctNames: distinctNames.remove('Mateusz Masternak')

#[fightersLinks, namesUpdated] = WebScraper.getWikiLinks(rankings[6], distinctNames)
fightersLinks = WebScraper.getWikiLinks(rankings[6], distinctNames)
#for link in fightersLinks: print(link)

start = time.time()
fights = WebScraper.getUpcomingFights(fightersLinks)
end = time.time()
print(end - start)

for f in fights: print(f)
print(len(fights))


""" import requests
from bs4 import BeautifulSoup


URL = 'https://en.wikipedia.org/wiki/Shakur_Stevenson'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')
classContent = soup.find(id='mw-content-text')

tables = classContent.find_all('table', attrs={'class':'wikitable'})
print(len(tables))

table = tables[1].find('tbody')
row = table.find_all('tr')[0] #returns 6, which is 2x the number it should be
print(len(row)) """

    
#for table in tables: print(table.get_text())







    