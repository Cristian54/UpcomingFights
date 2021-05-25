import requests
from bs4 import BeautifulSoup
from datetime import *

class WebScraper: 
    @staticmethod
    def getRankings():
        URL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        
        classContent = soup.find(id='mw-content-text')
        tables = classContent.find_all('table', attrs={'class':'wikitable'})
        
        TBRB, RING, WBA, WBC, IBF, WBO, BOXREC, colsHtml = [], [], [], [], [], [], [], []

        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            
            tempTBRB, tempRING, tempWBA, tempWBC, tempIBF, tempWBO, tempBR = [], [], [], [], [], [], []
            counter = 0
            
            for row in rows:
                cols = row.find_all('td')
                colsHtml.append(cols)
                cols = [ele.text.strip() for ele in cols]
                if len(cols) > 3:
                    tenthRanked = [cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[0]]
                    
                    if counter < 10:
                        if '(S)' in cols[3]:
                            param = cols[3].split("(S)", 1)
                            tempWBA.append(param[0])
                        else: 
                            tempWBA.append(cols[3])
                        
                        tempBR.append(cols[0])
                        tempTBRB.append(cols[1])
                        tempRING.append(cols[2])
                        tempWBC.append(cols[4])
                        tempIBF.append(cols[5])
                        tempWBO.append(cols[6])
                        counter += 1
                        
                    else:
                        counter = 0
                        
                        tempTBRB.append(tenthRanked[0])
                        TBRB.append(tempTBRB)
                        
                        tempRING.append(tenthRanked[1])
                        RING.append(tempRING)
                        
                        tempWBA.append(tenthRanked[2])
                        WBA.append(tempWBA)
                        
                        tempWBC.append(tenthRanked[3])
                        WBC.append(tempWBC)
                        
                        tempIBF.append(tenthRanked[4])
                        IBF.append(tempIBF)
                        
                        tempWBO.append(tenthRanked[5])
                        WBO.append(tempWBO)
                        
                        tempBR.append(tenthRanked[6])
                        BOXREC.append(tempBR)
        
        return [TBRB, RING, WBA, WBC, IBF, WBO, colsHtml, BOXREC]

    @staticmethod
    def getDistinctNames(rankings):
        namesSet = set()
        for company in rankings:
            for division in company:
                for name in division:
                    namesSet.add(name)
                            
        namesList = list(namesSet)
        return namesList        

    @staticmethod
    def getWikiLinks(tableRowsHtml, names):
        linksSet = set()
        for row in tableRowsHtml:
            for element in row:
                for link in element.find_all('a', href=True):
                    if link.get_text() in names and 'redlink=1' not in link['href']:
                        linksSet.add(link['href'])
        return list(linksSet) 
       
    @staticmethod
    def getOpponentsInfo(link):
        fighter_info = [] #[Name, Total fights, wins, KOs, losses, nickname, link, draws, height, reach]
        totalFights, wins, KOs, losses, nickname, draws, height, reach = '', '', '', '', '', '', '', ''
        
        URL = 'https://en.wikipedia.org' + link
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml') 
        
        nameHeading = soup.find('h1', id='firstHeading')
        nameText = nameHeading.get_text()
        if ' (American boxer)' in nameText:
            nameText = nameText.replace(' (American boxer)', '')
        elif ' (boxer)' in nameText:
            nameText = nameText.replace(' (boxer)', '')
        elif ' (Mexican boxer)' in nameText:
            nameText = nameText.replace(' (Mexican boxer)', '')
            
        classContent = soup.find(id='mw-content-text')
        fighterInfoTable = classContent.find('table', attrs={'class':'infobox vcard'})
        
        if fighterInfoTable == None: return [nameText, "Empty wiki page"]
        
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
            elif th.text.strip() == 'Draws':
                td = th.find_next('td')
                draws = td.text.strip()
            elif th.text.strip() == 'Height':
                td = th.find_next('td')
                height = td.text.strip()
            elif th.text.strip() == 'Reach':
                td = th.find_next('td')
                reach = td.text.strip()

        if draws != '': fighter_info.extend([nameText, totalFights, wins, KOs, losses, nickname, URL, draws, height, reach])
        else: fighter_info.extend([nameText, totalFights, wins, KOs, losses, nickname, URL, '0', height, reach])
            
        return fighter_info
        
    @staticmethod
    def getUpcomingFights(fightersLinks):
        fights = [] #[[A, B], [A, B]]
        
        for link in fightersLinks:
            fighterA_Info = [] #[Fight date, Name, Total fights, wins, KOs, losses, nickname, link, draws, date formatted, location, height, reach]
            fighterB_Info = [] 
            totalFights, wins, KOs, losses, nickname, draws, height, reach = '', '', '', '', '', '', '', ''
            
            URL = 'https://en.wikipedia.org' + link
            #print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'lxml')
                
            classContent = soup.find(id='mw-content-text')
            tables = classContent.find_all('table', attrs={'class':'wikitable'})
            
            if len(tables) <= 1:
                continue
            
            firstTable = tables[0].find('tbody')
            firstRow = firstTable.find_all('tr')[0]
            
            if link == '/wiki/Dillian_Whyte': 
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
            
            if fightDate.text.strip().startswith(('2018', '2019', '2020', 'TBA')):
                fightersLinks.remove(link)
                continue
            
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
                
            if datetime.today().date() <= fightDateFormatted.date():
                rowOneTDs = rowOne.find_all('td')
                opponentName = rowOneTDs[3]
                firstName = opponentName.text.strip().split(' ')[0]
                oppLinks = opponentName.find_all('a', href=True)
                
                for oppLink in oppLinks:
                    if oppLink['href'] in fightersLinks:
                        fightersLinks.remove(oppLink['href'])
                    if firstName in oppLink['href']:
                        fighterB_Info = WebScraper.getOpponentsInfo(oppLink['href'])
                        
                if not fighterB_Info: fighterB_Info.extend([opponentName.text.strip(), "No wiki page for opponent"])
                
                fightLocation = rowOneTDs[7].text.strip()
                
                nameHeading = soup.find('h1', id='firstHeading')
                nameText = nameHeading.get_text()
                if ' (American boxer)' in nameText:
                    nameText = nameText.replace(' (American boxer)', '')
                elif ' (boxer)' in nameText:
                    nameText = nameText.replace(' (boxer)', '')
                elif ' (Mexican boxer)' in nameText:
                    nameText = nameText.replace(' (Mexican boxer)', '')
                    
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
                    elif th.text.strip() == 'Draws':
                        td = th.find_next('td')
                        draws = td.text.strip()
                    elif th.text.strip() == 'Height':
                        td = th.find_next('td')
                        height = td.text.strip()
                    elif th.text.strip() == 'Reach':
                        td = th.find_next('td')
                        reach = td.text.strip()

                if draws != '': fighterA_Info.extend([fightDate.text.strip(), nameText, totalFights, wins, KOs, losses, nickname, URL, draws, fightDateFormatted.date(), fightLocation, height, reach])
                else: fighterA_Info.extend([fightDate.text.strip(), nameText, totalFights, wins, KOs, losses, nickname, URL, '0', fightDateFormatted.date(), fightLocation, height, reach])
                
                temp = []
                temp.append(fighterA_Info)
                temp.append(fighterB_Info)
                fights.append(temp)
                
            else: 
                continue
        
        names = []
        for fight in fights:
            if fight[0][1] in names or fight[1][0] in names: 
                fights.remove(fight)
                continue
            names.append(fight[0][1])
            names.append(fight[1][0])
         
        return fights
                
                
