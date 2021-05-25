from webscrapper import WebScraper
from datetime import *

rankings = WebScraper.getRankings()
rankingss = [rankings[1], rankings[7]]
distinctNames = WebScraper.getDistinctNames(rankingss)

if 'Alexei Papin' in distinctNames: distinctNames.remove('Alexei Papin')
if 'Manny Pacquiao' in distinctNames: distinctNames.remove('Manny Pacquiao')
if 'Mateusz Masternak' in distinctNames: distinctNames.remove('Mateusz Masternak')
if 'George Kambosos Jr.' in distinctNames: distinctNames.remove('George Kambosos Jr.')

fightersLinks = WebScraper.getWikiLinks(rankings[6], distinctNames)

fights = WebScraper.getUpcomingFights(fightersLinks)

for fight in fights: print(fight, "\n")
print(len(fights))


""" import requests
from bs4 import BeautifulSoup
from datetime import *


URL = 'https://en.wikipedia.org/wiki/Brandon_Figueroa'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')
classContent = soup.find(id='mw-content-text') """

""" tables = classContent.find_all('table', attrs={'class':'wikitable'})

firstTable = tables[0].find('tbody')
firstRow = firstTable.find_all('tr')[0]

if URL == '/wiki/Dillian_Whyte': 
    fightsTable = tables[3].find('tbody')
    rowZero = fightsTable.find_all('tr')[0]
    rowOne = fightsTable.find_all('tr')[1]
    
elif len(firstRow) == 6:
    fightsTable = tables[1].find('tbody')
    rowZero = fightsTable.find_all('tr')[0]
    rowOne = fightsTable.find_all('tr')[1]
    
elif len(firstRow) > 6 or len(firstRow) < 6:
    fightsTable = tables[2].find('tbody')
    rowZero = fightsTable.find_all('tr')[0]
    rowOne = fightsTable.find_all('tr')[1]


if len(rowZero.find_all('th')) == 8:
    fightDate = rowOne.find_all('td')[5]
else: fightDate = rowOne.find_all('td')[6]


#Formats so far: (Apr 12, 2020) (12 Apr 2020) (12 April 2020) (2021-05-22)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
if fightDate.text.strip().startswith(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')):
    fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%b %d, %Y")
elif any(month in fightDate.text.strip() for month in months):
    fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %B %Y")
elif fightDate.text.strip().startswith('2021'):
    fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%Y-%m-%d")
else:
    fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %b %Y")
    

if datetime.today() <= fightDateFormatted + timedelta(days=1):
    rowOneTDs = rowOne.find_all('td')
    opponentName = rowOneTDs[3]
    firstName = opponentName.text.strip().split(' ')[0]
    oppLinks = opponentName.find_all('a', href=True)
    for oppLink in oppLinks:
        if firstName in oppLink['href']:
            print(oppLink['href'])
    
    fightLocation = rowOneTDs[7].text.strip()
    print(fightLocation) """

""" fighterA_Info = [] #[Name, Total fights, wins, KOs, losses, nickname, link, draws]
totalFights, wins, KOs, losses, nickname, draws = '', '', '', '', '', '' 

fighterInfoTable = classContent.find('table', attrs={'class':'infobox vcard'})
tableBody = fighterInfoTable.find('tbody')
ths = tableBody.find_all('th', attrs={'class':'infobox-label'})
for th in ths: 
    if th.text.strip() == 'Total fights':
        td = th.find_next('td')
        totalFights = td.text.strip()
    elif th.text.strip() == 'Wins':
        td = th.find_next('td')
        wins = td.text.strip()
    elif th.text.strip() == 'Wins by KO':
        td = th.find_next('td')
        KOs = td.text.strip()
    elif th.text.strip() == 'Losses':
        td = th.find_next('td')
        losses = td.text.strip()
    elif th.text.strip() == 'Nickname(s)':
        td = th.find_next('td')
        nickname = td.text.strip()
        print(nickname)
    elif th.text.strip() == 'Draws':
        td = th.find_next('td')
        draws = td.text.strip()

if draws != '': fighterA_Info.extend([totalFights, wins, KOs, losses, nickname, URL, draws])
else: fighterA_Info.extend([totalFights, wins, KOs, losses, nickname, URL, 0])
    
print(fighterA_Info) """ 







    