from webscrapper import WebScraper
import time

rankings = WebScraper.getRankings()
counter = 0
for company in rankings:
    if counter == 6: continue
    counter += 1
    print(company, "\n")
rankingss = [rankings[1], rankings[7]]
""" distinctNames = WebScraper.getDistinctNames(rankingss)

if 'Alexei Papin' in distinctNames: distinctNames.remove('Alexei Papin')
if 'Manny Pacquiao' in distinctNames: distinctNames.remove('Manny Pacquiao')
if 'Mateusz Masternak' in distinctNames: distinctNames.remove('Mateusz Masternak')

fightersLinks = WebScraper.getWikiLinks(rankings[6], distinctNames)

start = time.time()
fights = WebScraper.getUpcomingFights(fightersLinks)
end = time.time()
print(end - start) """

""" 
for link in fightersLinks:
    fight = WebScraper.getUpcomingFightsV2(link, fightersLinks)
    if fight:
        fights.append(fight)
        oppLink = fight[1][4]
        if oppLink in fightersLinks: fightersLinks.remove(oppLink)
    else: continue """

""" fightsNames = [] 
for f in fights:
    if len(f[0]) == 5:
        if f[0][4] not in fightsNames and f[1][1] not in fightsNames:
            fightsNames.append(f[0][4])
            fightsNames.append(f[1][1])
        else: fights.remove(f) 
    else: 
        if f[0][5] not in fightsNames and f[1][1] not in fightsNames:
            fightsNames.append(f[0][5])
            fightsNames.append(f[1][1])
        else: fights.remove(f)
    
#print(fightsNames)

for f in fights: print(f)
print(len(fights)) """


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







    